"""
Servicio para obtener y cachear el valor de la UF.
Implementa reintentos, cache en MySQL y fallback a último valor conocido.
"""

from datetime import date, datetime, timedelta
from typing import Optional
import time
import requests
from src import db
from src.models.uf_cache import UFCache
import logging

logger = logging.getLogger(__name__)


class UFService:
    """Servicio para gestionar el valor de la UF con cache y resiliencia."""

    API_URL = 'https://mindicador.cl/api/uf'
    MAX_RETRIES = 3
    TIMEOUT = 15
    CACHE_DAYS = 2  # Mantener solo últimos 2 días

    @classmethod
    def obtener_valor_uf(cls) -> Optional[float]:
        """
        Obtiene el valor de la UF con la siguiente estrategia:
        1. Busca en cache del día actual
        2. Si no existe o está desactualizado, consulta API con reintentos
        3. Si API falla, usa último valor conocido como fallback

        Returns:
            float: Valor de la UF o None si no se pudo obtener
        """
        hoy = date.today()

        # 1. Intentar obtener desde cache
        cached_value = cls._get_from_cache(hoy)
        if cached_value:
            logger.info(f"UF obtenida desde cache: {cached_value} (fecha: {hoy})")
            return cached_value

        # 2. Intentar obtener desde API con reintentos
        api_value = cls._fetch_from_api_with_retry()
        if api_value:
            cls._save_to_cache(hoy, api_value)
            cls._cleanup_old_cache()
            logger.info(f"UF obtenida desde API y guardada en cache: {api_value}")
            return api_value

        # 3. Fallback: usar último valor conocido
        fallback_value = cls._get_latest_cached_value()
        if fallback_value:
            logger.warning(
                f"API de UF no disponible. Usando último valor conocido: {fallback_value}"
            )
            return fallback_value

        # 4. No hay ningún valor disponible
        logger.error("No se pudo obtener valor de UF: API falló y no hay cache disponible")
        return None

    @classmethod
    def _get_from_cache(cls, fecha: date) -> Optional[float]:
        """Obtiene el valor de la UF desde cache para una fecha específica."""
        try:
            uf_cache = UFCache.query.filter_by(fecha=fecha).first()
            if uf_cache:
                return float(uf_cache.valor)
        except Exception as e:
            logger.error(f"Error al leer cache de UF: {e}")
        return None

    @classmethod
    def _get_latest_cached_value(cls) -> Optional[float]:
        """Obtiene el último valor de UF disponible en cache."""
        try:
            latest = UFCache.query.order_by(UFCache.fecha.desc()).first()
            if latest:
                logger.info(f"Usando UF del {latest.fecha} como fallback")
                return float(latest.valor)
        except Exception as e:
            logger.error(f"Error al obtener último valor de cache: {e}")
        return None

    @classmethod
    def _fetch_from_api_with_retry(cls) -> Optional[float]:
        """
        Intenta obtener el valor de la UF desde la API con reintentos exponenciales.

        Returns:
            float: Valor de la UF o None si falló
        """
        for intento in range(1, cls.MAX_RETRIES + 1):
            try:
                logger.info(f"Consultando API de UF (intento {intento}/{cls.MAX_RETRIES})")

                response = requests.get(cls.API_URL, timeout=cls.TIMEOUT)

                if response.status_code == 200:
                    data = response.json()

                    if "serie" in data and len(data["serie"]) > 0:
                        valor_uf = data["serie"][0]["valor"]
                        logger.info(f"Valor UF obtenido exitosamente: {valor_uf}")
                        return valor_uf
                    else:
                        logger.warning("Respuesta de API no contiene serie de valores")

                else:
                    logger.warning(f"API respondió con status {response.status_code}")

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout en intento {intento}/{cls.MAX_RETRIES}")

            except requests.exceptions.RequestException as e:
                logger.warning(f"Error en intento {intento}/{cls.MAX_RETRIES}: {e}")

            except Exception as e:
                logger.error(f"Error inesperado en intento {intento}: {e}")

            # Backoff exponencial: esperar 1s, 2s, 4s entre reintentos
            if intento < cls.MAX_RETRIES:
                sleep_time = 2 ** (intento - 1)
                logger.info(f"Esperando {sleep_time}s antes del próximo intento")
                time.sleep(sleep_time)

        logger.error(f"Falló obtener UF después de {cls.MAX_RETRIES} intentos")
        return None

    @classmethod
    def _save_to_cache(cls, fecha: date, valor: float) -> bool:
        """
        Guarda el valor de la UF en cache.

        Args:
            fecha: Fecha del valor
            valor: Valor de la UF

        Returns:
            bool: True si se guardó correctamente
        """
        try:
            # Verificar si ya existe
            existing = UFCache.query.filter_by(fecha=fecha).first()

            if existing:
                # Actualizar valor existente
                existing.valor = valor
                existing.updated_at = datetime.utcnow()
                logger.info(f"Cache actualizado para {fecha}: {valor}")
            else:
                # Crear nuevo registro
                new_cache = UFCache(
                    fecha=fecha,
                    valor=valor,
                    updated_at=datetime.utcnow()
                )
                db.session.add(new_cache)
                logger.info(f"Nuevo cache creado para {fecha}: {valor}")

            db.session.commit()
            return True

        except Exception as e:
            logger.error(f"Error al guardar en cache: {e}")
            db.session.rollback()
            return False

    @classmethod
    def _cleanup_old_cache(cls):
        """Elimina registros de cache más antiguos que CACHE_DAYS días."""
        try:
            fecha_limite = date.today() - timedelta(days=cls.CACHE_DAYS)
            deleted = UFCache.query.filter(UFCache.fecha < fecha_limite).delete()

            if deleted > 0:
                db.session.commit()
                logger.info(f"Limpieza de cache: {deleted} registros antiguos eliminados")

        except Exception as e:
            logger.error(f"Error al limpiar cache: {e}")
            db.session.rollback()

    @classmethod
    def actualizar_uf_manual(cls, fecha: date, valor: float) -> bool:
        """
        Permite actualizar manualmente el valor de la UF.
        Útil para recuperación manual en caso de falla prolongada de la API.

        Args:
            fecha: Fecha del valor
            valor: Valor de la UF

        Returns:
            bool: True si se actualizó correctamente
        """
        logger.info(f"Actualización manual de UF: fecha={fecha}, valor={valor}")
        return cls._save_to_cache(fecha, valor)

    @classmethod
    def get_cache_info(cls) -> dict:
        """
        Obtiene información del estado del cache.
        Útil para monitoreo y diagnóstico.

        Returns:
            dict: Información del cache
        """
        try:
            all_cached = UFCache.query.order_by(UFCache.fecha.desc()).all()

            return {
                'total_registros': len(all_cached),
                'valores': [
                    {
                        'fecha': str(uf.fecha),
                        'valor': float(uf.valor),
                        'actualizado': str(uf.updated_at)
                    }
                    for uf in all_cached
                ],
                'ultimo_valor': float(all_cached[0].valor) if all_cached else None,
                'ultima_fecha': str(all_cached[0].fecha) if all_cached else None
            }
        except Exception as e:
            logger.error(f"Error al obtener info de cache: {e}")
            return {'error': str(e)}
