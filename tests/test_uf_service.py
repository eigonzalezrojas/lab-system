"""
Tests para el servicio de UF (UFService).
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import create_app
from src.services.uf_service import UFService


def test_uf_fetch():
    """Prueba obtener el valor de la UF desde la API."""
    print("\n=== TEST: Obtención de UF desde API ===\n")

    app = create_app()

    with app.app_context():
        print("Intentando obtener valor de UF...")

        valor = UFService.obtener_valor_uf()

        if valor:
            print(f"✅ PASS: Valor obtenido exitosamente: ${valor:,.2f}")
            assert valor > 0, "El valor de UF debe ser mayor a 0"
            assert isinstance(valor, float), "El valor debe ser un float"
            return True
        else:
            print("⚠️  WARN: No se pudo obtener el valor de la UF")
            print("Nota: Esto puede ser normal si la API está caída")
            return False


def test_cache_info():
    """Prueba obtener información del cache."""
    print("\n=== TEST: Información del Cache ===\n")

    app = create_app()

    with app.app_context():
        info = UFService.get_cache_info()

        if 'error' in info:
            print(f"❌ FAIL: Error al obtener info del cache: {info['error']}")
            return False

        print(f"Total de registros en cache: {info['total_registros']}")

        if info['valores']:
            print("\nValores almacenados:")
            for valor_info in info['valores']:
                print(f"  • Fecha: {valor_info['fecha']}")
                print(f"    Valor: ${valor_info['valor']:,.2f}")
                print(f"    Actualizado: {valor_info['actualizado']}\n")

            print(f"Último valor: ${info['ultimo_valor']:,.2f} ({info['ultima_fecha']})")
            print("✅ PASS: Cache tiene datos")
            return True
        else:
            print("⚠️  WARN: No hay valores en cache")
            return True  # No es un error, puede ser primera ejecución


def test_manual_update():
    """Prueba actualizar manualmente un valor de UF."""
    print("\n=== TEST: Actualización Manual ===\n")

    from datetime import date

    app = create_app()

    with app.app_context():
        test_fecha = date.today()
        test_valor = 37500.50

        print(f"Intentando guardar: {test_fecha} = ${test_valor:,.2f}")

        success = UFService.actualizar_uf_manual(test_fecha, test_valor)

        if success:
            print("✅ PASS: Valor actualizado correctamente")

            # Verificar que se guardó
            valor_guardado = UFService._get_from_cache(test_fecha)
            if valor_guardado == test_valor:
                print(f"✅ PASS: Verificación exitosa: ${valor_guardado:,.2f}")
                return True
            else:
                print(f"❌ FAIL: Valor guardado no coincide: esperado {test_valor}, obtenido {valor_guardado}")
                return False
        else:
            print("❌ FAIL: Error al actualizar el valor")
            return False


def test_cache_cleanup():
    """Prueba que la limpieza de cache funcione."""
    print("\n=== TEST: Limpieza de Cache ===\n")

    from datetime import date, timedelta

    app = create_app()

    with app.app_context():
        # Guardar un valor de hace 5 días
        fecha_antigua = date.today() - timedelta(days=5)
        valor_antiguo = 37000.00

        print(f"Guardando valor antiguo: {fecha_antigua} = ${valor_antiguo:,.2f}")
        UFService._save_to_cache(fecha_antigua, valor_antiguo)

        # Ejecutar limpieza
        print("Ejecutando limpieza de cache...")
        UFService._cleanup_old_cache()

        # Verificar que se eliminó
        valor_eliminado = UFService._get_from_cache(fecha_antigua)

        if valor_eliminado is None:
            print(f"✅ PASS: Registro antiguo eliminado correctamente")
            return True
        else:
            print(f"❌ FAIL: Registro antiguo no fue eliminado")
            return False


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "="*60)
    print("EJECUTANDO TESTS DE UF SERVICE")
    print("="*60)

    tests = [
        ("Cache Info", test_cache_info),
        ("Manual Update", test_manual_update),
        ("UF Fetch", test_uf_fetch),
        ("Cache Cleanup", test_cache_cleanup),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR en {test_name}: {e}")
            results.append((test_name, False))

    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests pasaron")
    print("="*60 + "\n")

    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
