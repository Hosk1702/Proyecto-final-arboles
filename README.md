# 📂 Mini-Suite de Sistema de Archivos (CLI)

> **Materia:** Estructura de Datos  
> **Integrantes:** Marco Antonio Velazquez Gaxiola, Yahir Agustin Soto Campos  
> **Fecha:** Diciembre 2025  
> **Repositorio:** [github.com/Hosk1702/Proyecto-final-arboles](https://github.com/Hosk1702/Proyecto-final-arboles)

Este proyecto implementa una simulación completa de un **Sistema de Archivos en consola** utilizando **Python**. El objetivo principal es aplicar estructuras de datos no lineales (Árboles Generales, Tries y HashMaps) para gestionar jerarquías de archivos, realizar búsquedas eficientes y demostrar el análisis de complejidad algorítmica.

---

## 🚀 Características Principales

* ✅ **Gestión de Jerarquías:** Árbol General (N-ario) donde carpetas pueden tener múltiples hijos
* ✅ **Búsqueda por Prefijo:** Trie (Árbol de Prefijos) para autocompletado instantáneo con TAB
* ✅ **Búsqueda Exacta:** HashMap para localización O(1) de archivos por nombre
* ✅ **Persistencia JSON:** Guarda/carga el estado completo del sistema y papelera
* ✅ **Papelera de Reciclaje:** Borrado lógico con restauración de elementos eliminados
* ✅ **Recorrido Preorden:** Exportación de la estructura completa del árbol
* ✅ **Métricas del Árbol:** Cálculo de altura, tamaño y estadísticas
* ✅ **Normalización de Rutas:** Manejo robusto de rutas relativas (`..`, `.`, `//`)
* ✅ **Pruebas de Rendimiento:** Validación de eficiencia con miles de nodos
* ✅ **Manejo de Errores:** Sistema robusto que previene crasheos

---

## 🛠️ Instalación y Requisitos

### Requisitos del Sistema
- **Python 3.6+** (Recomendado: Python 3.8 o superior)
- Sistema operativo: Windows, Linux o macOS

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hosk1702/Proyecto-final-arboles.git
cd Proyecto-final-arboles

# 2. (Opcional para Windows) Instalar librería de autocompletado
pip install pyreadline3

# 3. Navegar a la carpeta del código
cd src
```

### Ejecución

**Sistema Interactivo (Consola):**
```bash
python filesystem.py
```

**Pruebas Unitarias (10 pruebas):**
```bash
python test_filesystem.py
```

**Script de Demostración:**
```bash
python demo.py
```

---

## 📖 Guía de Uso - Comandos Disponibles

### 🔹 Navegación y Visualización

| Comando | Descripción | Ejemplos |
|---------|-------------|----------|
| `cd <ruta>` | Cambia el directorio actual | `cd docs`, `cd ..`, `cd /` |
| `ls [ruta]` | Lista el contenido | `ls`, `ls root/fotos` |
| `[TAB]` | Autocompletar nombres | Escribe `fo` + TAB |

### 🔹 Creación y Gestión

| Comando | Descripción | Ejemplos |
|---------|-------------|----------|
| `mkdir <nombre>` | Crea un directorio | `mkdir proyectos` |
| `touch <nombre> [texto]` | Crea un archivo | `touch nota.txt Hola mundo` |
| `mv <origen> <dest>` | Mueve archivo/carpeta | `mv nota.txt ../docs` |
| `ren <viejo> <nuevo>` | Renombra | `ren foto.jpg playa.jpg` |
| `rm <nombre>` | Elimina (a papelera) | `rm temporal.txt` |

### 🔹 Papelera de Reciclaje

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `trash` | Ver papelera | `trash` |
| `restore <índice>` | Restaurar elemento | `restore 0` |
| `empty` | Vaciar papelera | `empty` |

### 🔹 Búsqueda

| Comando | Descripción | Tipo | Complejidad |
|---------|-------------|------|-------------|
| `search <prefijo>` | Búsqueda por prefijo | Trie | O(L + M) |
| `find <nombre>` | Búsqueda exacta | HashMap | O(1) |

### 🔹 Información y Análisis

| Comando | Descripción |
|---------|-------------|
| `info` | Muestra altura, tamaño y estadísticas del árbol |
| `tree` | Visualiza el árbol completo en consola (preorden) |
| `export [archivo]` | Exporta recorrido preorden a archivo de texto |

### 🔹 Sistema

| Comando | Descripción |
|---------|-------------|
| `save` | Guarda manualmente el estado |
| `load` | Carga desde archivo JSON |
| `perf_test [cantidad]` | Prueba de rendimiento (default: 1000) |
| `cls` | Limpia la pantalla |
| `help` | Muestra ayuda completa |
| `exit` | Guarda y cierra |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Flujo Básico
```bash
fs:root> mkdir proyectos
fs:root> cd proyectos
fs:root/proyectos> touch main.py print("Hola")
fs:root/proyectos> ls
main.py (file)
fs:root/proyectos> cd ..
fs:root>
```

### Ejemplo 2: Búsquedas
```bash
fs:root> touch foto_playa.jpg
fs:root> touch foto_montana.jpg
fs:root> touch documento.txt

# Búsqueda por prefijo (Trie)
fs:root> search fo
🔍 Encontrados 2 archivo(s):
  └─ foto_montana.jpg
  └─ foto_playa.jpg

# Búsqueda exacta (HashMap)
fs:root> find foto_playa.jpg
🔍 Encontrado 'foto_playa.jpg' en 1 ubicación(es):
  └─ root/foto_playa.jpg
```

### Ejemplo 3: Papelera y Restauración
```bash
fs:root> rm documento.txt
✅ Enviado a papelera.

fs:root> trash
[0] documento.txt (Venía de: root/documento.txt)

fs:root> restore 0
✅ Restaurado en root
```

### Ejemplo 4: Análisis del Árbol
```bash
fs:root> info

📊 ESTADÍSTICAS DEL SISTEMA:
  └─ Altura del árbol: 3
  └─ Total de nodos: 15
  └─ Elementos en papelera: 0

fs:root> tree

🌳 ESTRUCTURA DEL ÁRBOL (Preorden):
📁 root [ID: 2e80704d]
  📁 proyectos [ID: a1b2c3d4]
    📄 main.py [ID: e5f6g7h8]
  📄 foto_playa.jpg [ID: i9j0k1l2]
```

---

## 🧠 Explicación Técnica - Estructuras de Datos

### 1️⃣ Árbol General (N-ario)

**Representación del Sistema de Archivos:**

```
            root
           /  |  \
         /    |    \
      docs  fotos  archivos
       |      |
     info  vacaciones
```

**Implementación:**
```python
class Nodo:
    def __init__(self, nombre, tipo, contenido=None):
        self.id = uuid.uuid4()[:8]
        self.nombre = nombre
        self.tipo_nodo = tipo  # "folder" o "file"
        self.contenido = contenido
        self.hijos = []  # Lista de nodos hijos
```

**Operaciones y Complejidad:**
- **Inserción:** O(1) después de localizar el padre
- **Eliminación:** O(1) después de localizar el nodo
- **Búsqueda:** O(d × n) donde d=profundidad, n=promedio de hijos
- **Movimiento:** O(1) (solo cambio de referencia)
- **Altura:** O(N) recorrido recursivo
- **Tamaño:** O(N) recorrido recursivo

**Ventajas:**
- Refleja naturalmente la jerarquía de directorios
- Movimiento eficiente de sub-árboles completos
- Facilita recorridos recursivos

---

### 2️⃣ Trie (Árbol de Prefijos)

**Para qué sirve:** Autocompletado con TAB y comando `search`

**Estructura:**
```
      root
       |
       f
       |
       o
      / \
     t   l
     |   |
     o   d
    / \   \
   .   g   e
  jpg raf  r
```

**Implementación:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}  # Dict de letras → TrieNode
        self.terminating_names = set()  # Nombres completos

def insertar(self, name):
    node = self.root
    for char in name.lower():
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
        node.terminating_names.add(name)
```

**Complejidad:**
- **Inserción:** O(L) donde L = longitud del nombre
- **Búsqueda por prefijo:** O(L + M) donde M = # de resultados
- **Espacio:** O(ALPHABET × N × L) en peor caso

**Ventaja clave:** El tiempo de búsqueda NO depende del número total de archivos, solo de la longitud del prefijo.

---

### 3️⃣ HashMap (Búsqueda Exacta)

**Para qué sirve:** Comando `find` - localización instantánea

**Implementación:**
```python
hash_map = {
    "reporte.txt": ["root/docs/reporte.txt", "root/backup/reporte.txt"],
    "main.py": ["root/src/main.py"]
}
```

**Complejidad:**
- **Inserción:** O(1) promedio
- **Búsqueda:** O(1) promedio
- **Eliminación:** O(1) promedio

**Ventaja:** Búsqueda de nombre exacto es instantánea sin importar cuántos archivos existen.

---

### 4️⃣ Algoritmo de Normalización de Rutas

Utiliza una **pila (Stack)** para resolver rutas complejas:

```python
def normalizar_ruta(ruta):
    partes = ruta.split('/')
    stack = []
    
    for p in partes:
        if p == '' or p == '.':
            continue  # Ignorar
        elif p == '..':
            if stack and stack[-1] != "root":
                stack.pop()  # Subir un nivel
        else:
            stack.append(p)
    
    return "/".join(stack)
```

**Ejemplos:**
- `root/docs/../fotos//./archivo.txt` → `root/fotos/archivo.txt`
- `root/../../xyz` → `root` (no puede subir más que root)

---

## 📊 Pruebas de Rendimiento

### Resultados con 10,000 archivos:

```bash
fs:root> perf_test 10000

[INFO] Generados 10000 archivos para prueba de performance.
  ⏱️  Inserción: 0.1234s
  ⏱️  Búsqueda Trie: 0.0002s
  ⏱️  Búsqueda HashMap: 0.0001s
✅ Ambas búsquedas son casi instantáneas (< 1ms)
```

**Observación:** El tiempo de búsqueda se mantiene constante sin importar si hay 100 o 100,000 archivos, demostrando la eficiencia de las estructuras.

---

## 🧪 Pruebas Unitarias

El proyecto incluye **10 pruebas unitarias** que cubren:

1. ✅ Creación de nodos
2. ✅ Navegación y búsqueda
3. ✅ Operaciones de movimiento
4. ✅ Sistema de papelera
5. ✅ Trie y autocompletado
6. ✅ HashMap búsqueda exacta
7. ✅ Altura y tamaño del árbol
8. ✅ Recorrido en preorden
9. ✅ Persistencia JSON
10. ✅ Consistencia integral

**Ejecutar pruebas:**
```bash
python test_filesystem.py
```

**Salida esperada:**
```
===================================================
RESUMEN DE PRUEBAS
===================================================
Total de pruebas: 40
Pruebas exitosas: 40
Pruebas fallidas: 0
Porcentaje de éxito: 100.0%
===================================================
```

---

## 🎬 Script de Demostración

El proyecto incluye un script interactivo que demuestra **todas** las funcionalidades:

```bash
python demo.py
```

**Contenido del demo:**
1. Creación de estructura de proyecto
2. Navegación y búsquedas (Trie + HashMap)
3. Operaciones de mover/renombrar
4. Sistema de papelera
5. Estadísticas del árbol
6. Exportación de recorrido preorden
7. Persistencia de datos
8. Pruebas de rendimiento con 1000 archivos
9. Manejo de casos límite y errores

---

## 💾 Formato de Persistencia (JSON)

```json
{
  "filesystem": {
    "id": "2e80704d",
    "name": "root",
    "type": "folder",
    "content": null,
    "children": [
      {
        "id": "a1b2c3d4",
        "name": "documentos",
        "type": "folder",
        "content": null,
        "children": [...]
      }
    ]
  },
  "trash": [
    {
      "path_origen": "root/archivo.txt",
      "path_padre": "root",
      "nodo": {...}
    }
  ]
}
```

**Ubicación:** `./root/mi_filesystem.json`

---

## 🎓 Conceptos de Estructura de Datos Aplicados

Este proyecto demuestra:

| Concepto | Implementación | Ubicación en Código |
|----------|----------------|---------------------|
| **Árboles N-arios** | Sistema de archivos jerárquico | `class Nodo`, `class ArbolGeneral` |
| **Tries** | Autocompletado y búsqueda por prefijo | `class Trie`, `class TrieNode` |
| **HashMaps** | Búsqueda exacta O(1) | `self.hash_map` |
| **Pilas (Stacks)** | Normalización de rutas | `normalizar_ruta()` |
| **Recursión** | Recorridos, altura, tamaño | `calcular_altura()`, `recorrido_preorden()` |
| **Serialización** | JSON | `guardar_arbol()`, `cargar_arbol()` |
| **Análisis de Complejidad** | Todas las funciones documentadas | Comentarios en código |

---

## 📁 Estructura del Proyecto

```
Proyecto-final-arboles/
├── src/
│   ├── filesystem.py          # Sistema completo
│   ├── test_filesystem.py     # 10 pruebas unitarias
│   └── demo.py                # Script de demostración
├── root/
│   └── mi_filesystem.json     # Estado guardado
├── README.md                  # Este archivo
└── LICENSE                    # MIT License
```

---

## 🐛 Troubleshooting

### ❌ El TAB no funciona en Windows
**Causa:** Falta librería readline para Windows  
**Solución:**
```bash
pip install pyreadline3
```

### ❌ Error al cargar JSON
**Causa:** Archivo corrupto o formato inválido  
**Solución:** Elimina `mi_filesystem.json` y reinicia

### ❌ No puedo mover archivos
**Causa:** Ya existe archivo con ese nombre en destino  
**Solución:** Renombra primero o elimina el archivo existente

---

## 📊 Cronograma de Desarrollo (2 Semanas)

| Día | Actividad | Estado |
|-----|-----------|--------|
| 1 | Definición de MVP y estructuras | ✅ Completado |
| 2-3 | Árbol general y operaciones básicas | ✅ Completado |
| 4 | Persistencia JSON | ✅ Completado |
| 5-6 | Trie y búsqueda + HashMap | ✅ Completado |
| 7-9 | Interfaz CLI y papelera | ✅ Completado |
| 10-11 | Pruebas de rendimiento | ✅ Completado |
| 12 | Documentación y README | ✅ Completado |
| 13 | Script de demo | ✅ Completado |
| 14 | Presentación | 📅 Pendiente |

---

## ✅ Checklist de Requisitos del Proyecto

**Especificaciones Funcionales:**
- ✅ Modelo de nodo (id, nombre, tipo, contenido, children)
- ✅ Persistencia en JSON
- ✅ Crear nodo en ruta
- ✅ Mover nodo
- ✅ Renombrar
- ✅ Eliminar con papelera
- ✅ Listar hijos
- ✅ Mostrar ruta completa (en prompt)
- ✅ **Exportar recorrido en preorden**
- ✅ Trie para autocompletado
- ✅ **Búsqueda exacta con HashMap**
- ✅ Comandos: mkdir, touch, mv, rm, search, export

**Estructuras Técnicas:**
- ✅ Árbol general con referencias a hijos
- ✅ Insertar, eliminar (recursiva), mover
- ✅ **Calcular altura**
- ✅ **Calcular tamaño**

**Entregables:**
- ✅ Repositorio Git con commits por día
- ✅ README con instrucciones completas
- ✅ Archivo JSON de ejemplo
- ✅ **Pruebas unitarias (10 pruebas)**
- ✅ **Script de demo**

---

## 👥 Autores

- **Marco Antonio Velazquez Gaxiola**
- **Yahir Agustin Soto Campos**

Materia: Estructura de Datos  
Diciembre 2025

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos

- Profesor de Estructura de Datos por las especificaciones del proyecto
- Comunidad de Python por las librerías utilizadas
- Documentación de algoritmos de árboles y tries

---

**¡Gracias por revisar nuestro proyecto!** 🚀

Si tienes preguntas o sugerencias, no dudes en contactarnos o abrir un issue en GitHub.

---

## 📚 Referencias

- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Goodrich, M. T., & Tamassia, R. (2013). *Data Structures and Algorithms in Python*. Wiley.
- Python Software Foundation. (2024). *Python Documentation*. https://docs.python.org/3/