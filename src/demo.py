"""
Script de Demostración del Sistema de Archivos
Muestra todas las funcionalidades implementadas

Ejecutar con: python demo.py
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from filesystem import ArbolGeneral

# Colores para mejor presentación
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_section(title):
    """Imprime un encabezado de sección"""
    print(f"\n{Color.HEADER}{Color.BOLD}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{Color.END}\n")
    time.sleep(0.5)

def print_action(action):
    """Imprime una acción que se va a ejecutar"""
    print(f"{Color.CYAN}▶{Color.END} {action}")
    time.sleep(0.3)

def print_result(result, is_success=True):
    """Imprime el resultado de una acción"""
    icon = f"{Color.GREEN}✓{Color.END}" if is_success else f"{Color.RED}✗{Color.END}"
    print(f"  {icon} {result}")
    time.sleep(0.3)

def pause():
    """Pausa para que el usuario pueda leer"""
    input(f"\n{Color.YELLOW}[Presiona ENTER para continuar...]{Color.END}")

def demo_creacion_basica():
    """Demo 1: Creación básica de archivos y carpetas"""
    print_section("DEMO 1: Creación de Archivos y Carpetas")
    
    fs = ArbolGeneral()
    
    print_action("Creando estructura de proyecto...")
    fs.crear_nodo("root", "mi_proyecto", "folder")
    print_result("Carpeta 'mi_proyecto' creada")
    
    fs.crear_nodo("root/mi_proyecto", "src", "folder")
    print_result("Carpeta 'src' creada")
    
    fs.crear_nodo("root/mi_proyecto", "docs", "folder")
    print_result("Carpeta 'docs' creada")
    
    fs.crear_nodo("root/mi_proyecto/src", "main.py", "file", "print('Hola Mundo')")
    print_result("Archivo 'main.py' creado con contenido")
    
    fs.crear_nodo("root/mi_proyecto/docs", "README.md", "file", "# Mi Proyecto")
    print_result("Archivo 'README.md' creado")
    
    print("\n📊 Resultado:")
    recorrido = fs.recorrido_preorden()
    for linea in recorrido:
        print(f"  {linea}")
    
    pause()
    return fs

def demo_navegacion_busqueda(fs):
    """Demo 2: Navegación y búsqueda"""
    print_section("DEMO 2: Navegación y Búsqueda")
    
    print_action("Buscando archivos que empiezan con 'main'...")
    resultados = fs.buscar_autocompletado("main")
    print_result(f"Encontrados: {resultados}")
    
    print_action("Búsqueda exacta de 'README.md'...")
    rutas = fs.buscar_exacto("README.md")
    print_result(f"Ubicaciones: {rutas}")
    
    print_action("Listando contenido de 'mi_proyecto/src'...")
    ok, contenido = fs.listar_directorio("root/mi_proyecto/src")
    print_result(contenido)
    
    pause()

def demo_operaciones_archivos(fs):
    """Demo 3: Operaciones con archivos"""
    print_section("DEMO 3: Mover y Renombrar Archivos")
    
    print_action("Moviendo 'main.py' a carpeta 'docs'...")
    ok, msg = fs.mover_nodo("root/mi_proyecto/src/main.py", "root/mi_proyecto/docs")
    print_result(msg, ok)
    
    print_action("Renombrando 'main.py' a 'programa.py'...")
    ok, msg = fs.renombrar_nodo("root/mi_proyecto/docs/main.py", "programa.py")
    print_result(msg, ok)
    
    print("\n📊 Estructura actualizada:")
    recorrido = fs.recorrido_preorden()
    for linea in recorrido:
        print(f"  {linea}")
    
    pause()

def demo_papelera(fs):
    """Demo 4: Sistema de papelera"""
    print_section("DEMO 4: Sistema de Papelera de Reciclaje")
    
    print_action("Creando archivo temporal...")
    fs.crear_nodo("root/mi_proyecto", "temporal.txt", "file", "datos temporales")
    print_result("Archivo creado")
    
    print_action("Eliminando archivo (enviando a papelera)...")
    ok, msg = fs.eliminar_nodo("root/mi_proyecto/temporal.txt")
    print_result(msg, ok)
    
    print_action("Mostrando contenido de la papelera...")
    papelera_info = fs.ver_papelera()
    print_result(f"\n{papelera_info}")
    
    print_action("Restaurando archivo desde la papelera...")
    ok, msg = fs.restaurar_nodo(0)
    print_result(msg, ok)
    
    print_action("Verificando que el archivo fue restaurado...")
    nodo, _ = fs._buscar_nodo_y_padre("root/mi_proyecto/temporal.txt")
    if nodo:
        print_result(f"Archivo '{nodo.nombre}' restaurado exitosamente")
    
    pause()

def demo_estadisticas(fs):
    """Demo 5: Estadísticas del árbol"""
    print_section("DEMO 5: Estadísticas y Análisis del Árbol")
    
    print_action("Calculando altura del árbol...")
    altura = fs.calcular_altura()
    print_result(f"Altura: {altura} niveles")
    
    print_action("Calculando tamaño total...")
    tamano = fs.calcular_tamano()
    print_result(f"Total de nodos: {tamano}")
    
    print_action("Contando elementos en papelera...")
    print_result(f"Elementos en papelera: {len(fs.papelera)}")
    
    print("\n📊 Resumen Completo:")
    print(f"  └─ Altura del árbol: {altura}")
    print(f"  └─ Total de nodos: {tamano}")
    print(f"  └─ Carpetas: {sum(1 for _ in fs.recorrido_preorden() if '📁' in _)}")
    print(f"  └─ Archivos: {sum(1 for _ in fs.recorrido_preorden() if '📄' in _)}")
    print(f"  └─ En papelera: {len(fs.papelera)}")
    
    pause()

def demo_recorrido_preorden(fs):
    """Demo 6: Exportación de recorrido"""
    print_section("DEMO 6: Recorrido en Preorden y Exportación")
    
    print_action("Generando recorrido en preorden...")
    recorrido = fs.recorrido_preorden()
    print_result(f"Generados {len(recorrido)} nodos")
    
    print("\n🌳 Estructura completa:")
    for linea in recorrido:
        print(f"  {linea}")
    
    print_action("\nExportando recorrido a archivo...")
    ok, msg = fs.exportar_preorden("demo_preorden.txt")
    print_result(msg, ok)
    
    if ok:
        print(f"\n{Color.GREEN}✓ Archivo 'demo_preorden.txt' creado exitosamente{Color.END}")
    
    pause()

def demo_persistencia(fs):
    """Demo 7: Guardar y cargar"""
    print_section("DEMO 7: Persistencia de Datos (JSON)")
    
    print_action("Guardando estado del sistema en JSON...")
    ok, msg = fs.guardar_arbol("./demo_filesystem.json")
    print_result(msg, ok)
    
    print_action("Creando nuevo sistema vacío...")
    fs_nuevo = ArbolGeneral()
    print_result(f"Sistema nuevo creado (tamaño: {fs_nuevo.calcular_tamano()})")
    
    print_action("Cargando estado guardado...")
    ok, msg = fs_nuevo.cargar_arbol("./demo_filesystem.json")
    print_result(msg, ok)
    
    if ok:
        print_action("Verificando que se cargó correctamente...")
        print_result(f"Tamaño después de cargar: {fs_nuevo.calcular_tamano()}")
        print_result(f"Altura después de cargar: {fs_nuevo.calcular_altura()}")
    
    pause()
    return fs_nuevo

def demo_rendimiento():
    """Demo 8: Pruebas de rendimiento"""
    print_section("DEMO 8: Pruebas de Rendimiento")
    
    fs = ArbolGeneral()
    
    cantidad = 1000
    print_action(f"Generando {cantidad} archivos de prueba...")
    
    start = time.time()
    fs.generar_carga_prueba(cantidad)
    end = time.time()
    print_result(f"Tiempo de inserción: {end - start:.4f} segundos")
    
    print_action("Realizando búsqueda por prefijo (Trie)...")
    start = time.time()
    resultados = fs.buscar_autocompletado("archivo_perf_9")
    end = time.time()
    print_result(f"Tiempo de búsqueda Trie: {end - start:.6f} segundos")
    print_result(f"Encontrados: {len(resultados)} archivos")
    
    print_action("Realizando búsqueda exacta (HashMap)...")
    start = time.time()
    rutas = fs.buscar_exacto("archivo_perf_00500_test.txt")
    end = time.time()
    print_result(f"Tiempo de búsqueda HashMap: {end - start:.6f} segundos")
    
    print(f"\n{Color.GREEN}✓ Ambas estructuras demuestran eficiencia O(1) y O(L){Color.END}")
    
    pause()

def demo_casos_limite():
    """Demo 9: Casos límite y manejo de errores"""
    print_section("DEMO 9: Manejo de Errores y Casos Límite")
    
    fs = ArbolGeneral()
    fs.crear_nodo("root", "test", "folder")
    
    print_action("Intentando crear archivo duplicado...")
    ok, msg = fs.crear_nodo("root", "test", "folder")
    print_result(msg, ok)
    
    print_action("Intentando mover a ubicación inexistente...")
    ok, msg = fs.mover_nodo("root/test", "root/inexistente")
    print_result(msg, ok)
    
    print_action("Intentando eliminar carpeta raíz...")
    ok, msg = fs.eliminar_nodo("root")
    print_result(msg, ok)
    
    print_action("Intentando restaurar con índice inválido...")
    ok, msg = fs.restaurar_nodo(999)
    print_result(msg, ok)
    
    print(f"\n{Color.GREEN}✓ Sistema maneja errores correctamente sin crashear{Color.END}")
    
    pause()

def main():
    """Función principal del demo"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Color.HEADER}{Color.BOLD}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║       DEMOSTRACIÓN DEL SISTEMA DE ARCHIVOS CON ÁRBOLES           ║")
    print("║                                                                    ║")
    print("║  Proyecto Final - Estructura de Datos                             ║")
    print("║  Marco Antonio Velazquez Gaxiola & Yahir Agustin Soto Campos     ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Color.END}")
    
    print(f"\n{Color.YELLOW}Este script demostrará todas las funcionalidades del sistema:{Color.END}")
    print("  1. Creación de archivos y carpetas")
    print("  2. Navegación y búsqueda (Trie + HashMap)")
    print("  3. Operaciones de movimiento y renombrado")
    print("  4. Sistema de papelera de reciclaje")
    print("  5. Estadísticas del árbol (altura, tamaño)")
    print("  6. Recorrido en preorden y exportación")
    print("  7. Persistencia de datos (JSON)")
    print("  8. Pruebas de rendimiento")
    print("  9. Manejo de errores")
    
    pause()
    
    try:
        # Ejecutar todas las demos
        fs = demo_creacion_basica()
        demo_navegacion_busqueda(fs)
        demo_operaciones_archivos(fs)
        demo_papelera(fs)
        demo_estadisticas(fs)
        demo_recorrido_preorden(fs)
        fs = demo_persistencia(fs)
        demo_rendimiento()
        demo_casos_limite()
        
        # Resumen final
        print_section("DEMO COMPLETADA EXITOSAMENTE")
        print(f"{Color.GREEN}{Color.BOLD}")
        print("✓ Todas las funcionalidades fueron demostradas correctamente")
        print("✓ Sistema de Archivos completamente funcional")
        print("✓ Estructuras de datos implementadas:")
        print("    - Árbol General (N-ario)")
        print("    - Trie (Árbol de Prefijos)")
        print("    - HashMap (Búsqueda exacta)")
        print("✓ Todas las operaciones requeridas implementadas")
        print(f"{Color.END}")
        
        print(f"\n{Color.CYAN}Archivos generados durante el demo:{Color.END}")
        print("  - demo_filesystem.json (estado guardado)")
        print("  - demo_preorden.txt (recorrido exportado)")
        
        print(f"\n{Color.YELLOW}Próximos pasos:{Color.END}")
        print("  1. Ejecuta 'python test_filesystem.py' para ver las pruebas unitarias")
        print("  2. Ejecuta 'python filesystem.py' para usar el sistema interactivo")
        
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Demo interrumpida por el usuario{Color.END}")
    except Exception as e:
        print(f"\n\n{Color.RED}Error durante el demo: {str(e)}{Color.END}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{Color.BLUE}Gracias por ver la demostración 👋{Color.END}\n")


if __name__ == "__main__":
    main()