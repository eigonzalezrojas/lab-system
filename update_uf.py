#!/usr/bin/env python3
"""
Script para actualizar manualmente el valor de la UF.
Útil en caso de falla prolongada de la API de mindicador.cl

Uso:
    python update_uf.py <valor>                    # Actualiza con fecha de hoy
    python update_uf.py <valor> <fecha>            # Actualiza con fecha específica (YYYY-MM-DD)
    python update_uf.py --info                     # Muestra info del cache
    python update_uf.py --test                     # Prueba la obtención de UF

Ejemplos:
    python update_uf.py 37500.50
    python update_uf.py 37500.50 2026-02-01
    python update_uf.py --info
"""

import sys
import os
from datetime import datetime, date

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import create_app
from src.services.uf_service import UFService


def print_help():
    """Muestra ayuda de uso."""
    print(__doc__)


def show_cache_info():
    """Muestra información del cache actual."""
    print("\n=== INFORMACIÓN DEL CACHE DE UF ===\n")

    info = UFService.get_cache_info()

    if 'error' in info:
        print(f"❌ Error: {info['error']}")
        return

    print(f"Total de registros en cache: {info['total_registros']}")

    if info['valores']:
        print("\nValores almacenados:")
        for valor_info in info['valores']:
            print(f"  • Fecha: {valor_info['fecha']}")
            print(f"    Valor: ${valor_info['valor']:,.2f}")
            print(f"    Actualizado: {valor_info['actualizado']}\n")

        print(f"Último valor: ${info['ultimo_valor']:,.2f} ({info['ultima_fecha']})")
    else:
        print("⚠️  No hay valores en cache")


def test_uf_fetch():
    """Prueba obtener el valor de la UF."""
    print("\n=== PRUEBA DE OBTENCIÓN DE UF ===\n")
    print("Intentando obtener valor de UF...")

    valor = UFService.obtener_valor_uf()

    if valor:
        print(f"✅ Valor obtenido exitosamente: ${valor:,.2f}")
    else:
        print("❌ No se pudo obtener el valor de la UF")


def update_uf_manual(valor: float, fecha: date):
    """
    Actualiza manualmente el valor de la UF.

    Args:
        valor: Valor de la UF
        fecha: Fecha del valor
    """
    print(f"\n=== ACTUALIZACIÓN MANUAL DE UF ===\n")
    print(f"Fecha: {fecha}")
    print(f"Valor: ${valor:,.2f}")

    confirmacion = input("\n¿Confirmar actualización? (s/n): ")

    if confirmacion.lower() != 's':
        print("❌ Actualización cancelada")
        return

    success = UFService.actualizar_uf_manual(fecha, valor)

    if success:
        print("✅ Valor de UF actualizado correctamente")
    else:
        print("❌ Error al actualizar el valor de UF")


def main():
    """Función principal."""
    app = create_app()

    with app.app_context():
        # Sin argumentos o --help
        if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
            print_help()
            return

        # --info: mostrar información del cache
        if '--info' in sys.argv:
            show_cache_info()
            return

        # --test: probar obtención de UF
        if '--test' in sys.argv:
            test_uf_fetch()
            return

        # Actualización manual
        try:
            valor = float(sys.argv[1])

            # Fecha específica o fecha de hoy
            if len(sys.argv) >= 3:
                fecha_str = sys.argv[2]
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            else:
                fecha = date.today()

            update_uf_manual(valor, fecha)

        except ValueError as e:
            print(f"❌ Error: Valor inválido. Debe ser un número.")
            print(f"   Ejemplo: python update_uf.py 37500.50")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
