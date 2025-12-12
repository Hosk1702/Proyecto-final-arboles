"""
Pruebas Unitarias para el Sistema de Archivos
Estructura de Datos - Proyecto Final

Ejecutar con: python test_filesystem.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from filesystem import ArbolGeneral, Nodo, Trie

# Colores para output
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class TestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0

    def assert_true(self, condition, test_name):
        """Verifica que una condición sea verdadera."""
        self.tests_total += 1
        if condition:
            self.tests_passed += 1
            print(f"{Color.GREEN}✓{Color.END} {test_name}")
            return True
        else:
            self.tests_failed += 1
            print(f"{Color.RED}✗{Color.END} {test_name}")
            return False

    def assert_equal(self, actual, expected, test_name):
        """Verifica que dos valores sean iguales."""
        self.tests_total += 1
        if actual == expected:
            self.tests_passed += 1
            print(f"{Color.GREEN}✓{Color.END} {test_name}")
            return True
        else:
            self.tests_failed += 1
            print(f"{Color.RED}✗{Color.END} {test_name} - Esperado: {expected}, Obtenido: {actual}")
            return False

    def print_results(self):
        """Imprime el resumen de las pruebas."""
        print("\n" + "=" * 60)
        print(f"{Color.BLUE}RESUMEN DE PRUEBAS{Color.END}")
        print("=" * 60)
        print(f"Total de pruebas: {self.tests_total}")
        print(f"{Color.GREEN}Pruebas exitosas: {self.tests_passed}{Color.END}")
        print(f"{Color.RED}Pruebas fallidas: {self.tests_failed}{Color.END}")
        
        percentage = (self.tests_passed / self.tests_total * 100) if self.tests_total > 0 else 0
        print(f"Porcentaje de éxito: {percentage:.1f}%")
        print("=" * 60)


def test_creacion_nodos(suite):
    """Prueba 1: Creación de Nodos"""
    print(f"\n{Color.YELLOW}[PRUEBA 1] Creación de Nodos{Color.END}")
    
    fs = ArbolGeneral()
    
    # Crear carpeta
    ok, msg = fs.crear_nodo("root", "documentos", "folder")
    suite.assert_true(ok, "Crear carpeta 'documentos'")
    
    # Crear archivo
    ok, msg = fs.crear_nodo("root", "archivo.txt", "file", "contenido de prueba")
    suite.assert_true(ok, "Crear archivo 'archivo.txt'")
    
    # Intentar crear duplicado (debe fallar)
    ok, msg = fs.crear_nodo("root", "archivo.txt", "file")
    suite.assert_true(not ok, "Rechazar creación de archivo duplicado")
    
    # Verificar que existen
    suite.assert_equal(len(fs.root.hijos), 2, "Verificar 2 hijos en root")


def test_navegacion_busqueda(suite):
    """Prueba 2: Navegación y Búsqueda de Nodos"""
    print(f"\n{Color.YELLOW}[PRUEBA 2] Navegación y Búsqueda{Color.END}")
    
    fs = ArbolGeneral()
    fs.crear_nodo("root", "fotos", "folder")
    fs.crear_nodo("root/fotos", "vacaciones.jpg", "file")
    
    # Buscar nodo existente
    nodo, padre = fs._buscar_nodo_y_padre("root/fotos")
    suite.assert_true(nodo is not None, "Buscar carpeta 'fotos'")
    suite.assert_equal(nodo.nombre, "fotos", "Verificar nombre de carpeta")
    
    # Buscar archivo dentro de carpeta
    nodo, padre = fs._buscar_nodo_y_padre("root/fotos/vacaciones.jpg")
    suite.assert_true(nodo is not None, "Buscar archivo en subcarpeta")
    
    # Buscar nodo inexistente
    nodo, padre = fs._buscar_nodo_y_padre("root/inexistente")
    suite.assert_true(nodo is None, "Rechazar búsqueda de ruta inexistente")


def test_operaciones_movimiento(suite):
    """Prueba 3: Mover y Renombrar"""
    print(f"\n{Color.YELLOW}[PRUEBA 3] Operaciones de Movimiento{Color.END}")
    
    fs = ArbolGeneral()
    fs.crear_nodo("root", "docs", "folder")
    fs.crear_nodo("root", "backup", "folder")
    fs.crear_nodo("root/docs", "reporte.txt", "file", "contenido")
    
    # Mover archivo
    ok, msg = fs.mover_nodo("root/docs/reporte.txt", "root/backup")
    suite.assert_true(ok, "Mover archivo a otra carpeta")
    
    # Verificar que se movió
    nodo, _ = fs._buscar_nodo_y_padre("root/backup/reporte.txt")
    suite.assert_true(nodo is not None, "Verificar archivo en nueva ubicación")
    
    # Verificar que ya no está en la ubicación original
    nodo, _ = fs._buscar_nodo_y_padre("root/docs/reporte.txt")
    suite.assert_true(nodo is None, "Verificar que archivo no está en ubicación original")
    
    # Renombrar
    ok, msg = fs.renombrar_nodo("root/backup/reporte.txt", "informe.txt")
    suite.assert_true(ok, "Renombrar archivo")
    
    nodo, _ = fs._buscar_nodo_y_padre("root/backup/informe.txt")
    suite.assert_equal(nodo.nombre if nodo else None, "informe.txt", "Verificar nuevo nombre")


def test_papelera(suite):
    """Prueba 4: Sistema de Papelera"""
    print(f"\n{Color.YELLOW}[PRUEBA 4] Sistema de Papelera{Color.END}")
    
    fs = ArbolGeneral()
    fs.crear_nodo("root", "temporal.txt", "file")
    
    # Eliminar archivo
    ok, msg = fs.eliminar_nodo("root/temporal.txt")
    suite.assert_true(ok, "Eliminar archivo (enviar a papelera)")
    
    # Verificar que está en la papelera
    suite.assert_equal(len(fs.papelera), 1, "Verificar 1 elemento en papelera")
    
    # Verificar que ya no está en el árbol
    nodo, _ = fs._buscar_nodo_y_padre("root/temporal.txt")
    suite.assert_true(nodo is None, "Verificar que archivo no está en árbol")
    
    # Restaurar
    ok, msg = fs.restaurar_nodo(0)
    suite.assert_true(ok, "Restaurar archivo de papelera")
    
    # Verificar que volvió
    nodo, _ = fs._buscar_nodo_y_padre("root/temporal.txt")
    suite.assert_true(nodo is not None, "Verificar archivo restaurado en árbol")
    
    # Verificar papelera vacía
    suite.assert_equal(len(fs.papelera), 0, "Verificar papelera vacía después de restaurar")


def test_trie_autocompletado(suite):
    """Prueba 5: Trie y Autocompletado"""
    print(f"\n{Color.YELLOW}[PRUEBA 5] Trie y Autocompletado{Color.END}")
    
    trie = Trie()
    
    # Insertar palabras
    trie.insertar("foto")
    trie.insertar("fotografia")
    trie.insertar("folder")
    trie.insertar("formulario")
    
    # Buscar con prefijo "fo"
    resultados = trie.buscar_por_prefijo("fo")
    suite.assert_equal(len(resultados), 4, "Buscar 4 palabras con prefijo 'fo'")
    
    # Buscar con prefijo "fot"
    resultados = trie.buscar_por_prefijo("fot")
    suite.assert_equal(len(resultados), 2, "Buscar 2 palabras con prefijo 'fot'")
    
    # Eliminar palabra
    trie.eliminar("foto")
    resultados = trie.buscar_por_prefijo("fot")
    suite.assert_equal(len(resultados), 1, "Verificar eliminación de palabra del Trie")
    
    # Buscar con prefijo inexistente
    resultados = trie.buscar_por_prefijo("xyz")
    suite.assert_equal(len(resultados), 0, "Buscar con prefijo inexistente")


def test_hashmap_busqueda_exacta(suite):
    """Prueba 6: HashMap para Búsqueda Exacta"""
    print(f"\n{Color.YELLOW}[PRUEBA 6] HashMap - Búsqueda Exacta{Color.END}")
    
    fs = ArbolGeneral()
    fs.crear_nodo("root", "datos", "folder")
    fs.crear_nodo("root/datos", "reporte.txt", "file")
    fs.crear_nodo("root", "reporte.txt", "file")  # Mismo nombre, diferente ubicación
    
    # Buscar nombre exacto
    rutas = fs.buscar_exacto("reporte.txt")
    suite.assert_equal(len(rutas), 2, "Encontrar 2 archivos con nombre 'reporte.txt'")
    
    # Verificar que las rutas son correctas
    suite.assert_true("root/reporte.txt" in rutas, "Verificar ruta 1 en resultados")
    suite.assert_true("root/datos/reporte.txt" in rutas, "Verificar ruta 2 en resultados")
    
    # Buscar nombre inexistente
    rutas = fs.buscar_exacto("inexistente.txt")
    suite.assert_equal(len(rutas), 0, "Buscar nombre inexistente retorna lista vacía")


def test_altura_y_tamano(suite):
    """Prueba 7: Cálculo de Altura y Tamaño"""
    print(f"\n{Color.YELLOW}[PRUEBA 7] Altura y Tamaño del Árbol{Color.END}")
    
    fs = ArbolGeneral()
    
    # Árbol con altura 0 (solo root)
    suite.assert_equal(fs.calcular_altura(), 0, "Altura de árbol vacío = 0")
    suite.assert_equal(fs.calcular_tamano(), 1, "Tamaño de árbol vacío = 1 (root)")
    
    # Agregar un nivel
    fs.crear_nodo("root", "docs", "folder")
    fs.crear_nodo("root", "archivo.txt", "file")
    
    suite.assert_equal(fs.calcular_altura(), 1, "Altura con 1 nivel = 1")
    suite.assert_equal(fs.calcular_tamano(), 3, "Tamaño con 3 nodos = 3")
    
    # Agregar más niveles
    fs.crear_nodo("root/docs", "informes", "folder")
    fs.crear_nodo("root/docs/informes", "q1.txt", "file")
    
    suite.assert_equal(fs.calcular_altura(), 3, "Altura con 3 niveles = 3")
    suite.assert_equal(fs.calcular_tamano(), 5, "Tamaño con 5 nodos = 5")


def test_preorden(suite):
    """Prueba 8: Recorrido en Preorden"""
    print(f"\n{Color.YELLOW}[PRUEBA 8] Recorrido en Preorden{Color.END}")
    
    fs = ArbolGeneral()
    fs.crear_nodo("root", "A", "folder")
    fs.crear_nodo("root", "B", "file")
    fs.crear_nodo("root/A", "C", "file")
    
    recorrido = fs.recorrido_preorden()
    
    # Verificar longitud (4 nodos: root, A, B, C)
    suite.assert_equal(len(recorrido), 4, "Recorrido incluye 4 nodos")
    
    # Verificar orden (preorden: root -> A -> C -> B)
    suite.assert_true("root" in recorrido[0], "Primer elemento es root")
    suite.assert_true("A" in recorrido[1], "Segundo elemento es A")
    suite.assert_true("C" in recorrido[2], "Tercer elemento es C (hijo de A)")
    suite.assert_true("B" in recorrido[3], "Cuarto elemento es B")


def test_persistencia(suite):
    """Prueba 9: Guardar y Cargar desde JSON"""
    print(f"\n{Color.YELLOW}[PRUEBA 9] Persistencia (JSON){Color.END}")
    
    fs1 = ArbolGeneral()
    fs1.crear_nodo("root", "test_persistencia", "folder")
    fs1.crear_nodo("root/test_persistencia", "dato.txt", "file", "contenido de prueba")
    
    # Guardar
    archivo_prueba = "./test_temp.json"
    ok, msg = fs1.guardar_arbol(archivo_prueba)
    suite.assert_true(ok, "Guardar árbol en archivo JSON")
    
    # Cargar en nuevo árbol
    fs2 = ArbolGeneral()
    ok, msg = fs2.cargar_arbol(archivo_prueba)
    suite.assert_true(ok, "Cargar árbol desde archivo JSON")
    
    # Verificar que se cargó correctamente
    nodo, _ = fs2._buscar_nodo_y_padre("root/test_persistencia/dato.txt")
    suite.assert_true(nodo is not None, "Verificar nodo cargado existe")
    suite.assert_equal(nodo.contenido, "contenido de prueba", "Verificar contenido del nodo")
    
    # Limpiar archivo de prueba
    if os.path.exists(archivo_prueba):
        os.remove(archivo_prueba)


def test_consistencia_despues_operaciones(suite):
    """Prueba 10: Consistencia del Árbol después de Múltiples Operaciones"""
    print(f"\n{Color.YELLOW}[PRUEBA 10] Consistencia Integral{Color.END}")
    
    fs = ArbolGeneral()
    
    # Serie de operaciones complejas
    fs.crear_nodo("root", "proyecto", "folder")
    fs.crear_nodo("root/proyecto", "src", "folder")
    fs.crear_nodo("root/proyecto/src", "main.py", "file", "codigo")
    fs.crear_nodo("root/proyecto", "docs", "folder")
    
    # Mover archivo
    fs.mover_nodo("root/proyecto/src/main.py", "root/proyecto/docs")
    
    # Renombrar
    fs.renombrar_nodo("root/proyecto/docs/main.py", "principal.py")
    
    # Verificar estructura final
    nodo, _ = fs._buscar_nodo_y_padre("root/proyecto/docs/principal.py")
    suite.assert_true(nodo is not None, "Archivo existe en nueva ubicación con nuevo nombre")
    
    # Verificar búsqueda por prefijo
    resultados = fs.buscar_autocompletado("princ")
    suite.assert_true("principal.py" in resultados, "Trie actualizado correctamente")
    
    # Verificar búsqueda exacta
    rutas = fs.buscar_exacto("principal.py")
    suite.assert_equal(len(rutas), 1, "HashMap actualizado correctamente")
    
    # Verificar altura y tamaño
    altura = fs.calcular_altura()
    tamano = fs.calcular_tamano()
    suite.assert_equal(altura, 3, "Altura correcta después de operaciones")
    suite.assert_equal(tamano, 5, "Tamaño correcto después de operaciones")


def run_all_tests():
    """Ejecuta todas las pruebas"""
    suite = TestSuite()
    
    print("\n" + "=" * 60)
    print(f"{Color.BLUE}INICIANDO SUITE DE PRUEBAS UNITARIAS{Color.END}")
    print("=" * 60)
    
    test_creacion_nodos(suite)
    test_navegacion_busqueda(suite)
    test_operaciones_movimiento(suite)
    test_papelera(suite)
    test_trie_autocompletado(suite)
    test_hashmap_busqueda_exacta(suite)
    test_altura_y_tamano(suite)
    test_preorden(suite)
    test_persistencia(suite)
    test_consistencia_despues_operaciones(suite)
    
    suite.print_results()
    
    return suite.tests_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)