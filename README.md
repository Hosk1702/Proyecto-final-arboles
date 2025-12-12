# 📂 Mini-Suite de Sistema de Archivos (CLI)

> **Materia:** Estructura de Datos  
> **Integrantes:** Marco Antonio Velazquez Gaxiola, Yahir Agustin Soto Campos  
> **Fecha:** Diciembre 2025

Este proyecto implementa una simulación completa de un Sistema de Archivos en consola utilizando **Python**. El objetivo principal es aplicar estructuras de datos no lineales para gestionar jerarquías de archivos y realizar búsquedas eficientes mediante algoritmos avanzados.

---

## 🚀 Características Principales

* **Gestión de Jerarquías:** Utiliza un **Árbol General** donde las carpetas pueden tener _N_ hijos (archivos y subcarpetas).
* **Búsqueda Optimizada:** Implementación de un **Trie (Árbol de Prefijos)** para autocompletado con TAB y búsqueda instantánea.
* **Persistencia de Datos:** Guarda y carga el estado completo del sistema (incluyendo la papelera) en archivos JSON.
* **Papelera de Reciclaje:** Sistema de borrado lógico con capacidad de restauración de elementos eliminados.
* **Autocompletado Inteligente:** Presiona TAB para autocompletar nombres de archivos mientras escribes.
* **Pruebas de Rendimiento:** Comando integrado `perf_test` para medir la eficiencia de las estructuras con miles de nodos.
* **Normalización de Rutas:** Manejo robusto de rutas relativas y absolutas (soporta `..`, `.`, `/`, etc.).

---

## 🛠️ Instalación y Requisitos

### Requisitos del Sistema
- **Python 3.x** (Versión 3.6 o superior recomendada)

### Dependencias

El sistema utiliza principalmente la librería estándar de Python. Sin embargo, para habilitar el **autocompletado con TAB** en **Windows**, necesitas instalar una librería adicional:

```bash
pip install pyreadline3
```

**Nota:** En Linux y macOS, el módulo `readline` viene incluido por defecto.

### Instalación

1. Clona o descarga este repositorio:
```bash
git clone https://github.com/tuusuario/Proyecto-final-arboles.git
cd Proyecto-final-arboles
```

2. (Opcional) Instala la dependencia para Windows:
```bash
pip install pyreadline3
```

3. Navega a la carpeta del código fuente:
```bash
cd src
```

### Ejecución

Para iniciar la consola interactiva, ejecuta:

```bash
python filesystem.py
```

Verás el prompt del sistema:
```
fs:root>
```

---

## 📖 Guía de Uso - Comandos Disponibles

Una vez dentro de la consola `fs:root>`, puedes utilizar los siguientes comandos:

### 🔹 Navegación y Visualización

| Comando | Descripción | Ejemplos |
|---------|-------------|----------|
| `cd <ruta>` | Cambia el directorio actual. Soporta rutas relativas (`..`) y absolutas. | `cd docs`<br>`cd ..`<br>`cd /`<br>`cd root/fotos` |
| `ls [ruta]` | Lista el contenido del directorio actual o de la ruta especificada. | `ls`<br>`ls root/fotos`<br>`ls ../documentos` |

### 🔹 Creación y Gestión de Archivos

| Comando | Descripción | Ejemplos |
|---------|-------------|----------|
| `mkdir <nombre>` | Crea un nuevo directorio en la ubicación actual. | `mkdir vacaciones`<br>`mkdir proyectos` |
| `touch <nombre> [texto]` | Crea un archivo. Opcionalmente puedes agregar contenido. | `touch nota.txt`<br>`touch tarea.txt Este es el contenido` |
| `mv <origen> <destino>` | Mueve un archivo o carpeta a otra ubicación. | `mv nota.txt ../docs`<br>`mv fotos root/backup` |
| `ren <viejo> <nuevo>` | Renombra un archivo o carpeta. | `ren foto.jpg playa.jpg`<br>`ren carpeta1 proyectos` |
| `rm <nombre>` | Envía un elemento a la papelera (borrado lógico). | `rm archivo_viejo.txt`<br>`rm carpeta_temporal` |

### 🔹 Papelera de Reciclaje

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `trash` | Muestra la lista de elementos en la papelera con su índice. | `trash` |
| `restore <índice>` | Restaura un elemento de la papelera a su ubicación original. | `restore 0`<br>`restore 2` |
| `empty` | Vacía la papelera permanentemente (borrado físico irreversible). | `empty` |

### 🔹 Búsqueda y Autocompletado

| Comando/Acción | Descripción | Ejemplo |
|----------------|-------------|---------|
| `[TAB]` | Presiona TAB mientras escribes para autocompletar nombres de archivos. | Escribe `fo` + TAB |
| `search <prefijo>` | Busca todos los archivos que comienzan con el prefijo dado. | `search foto`<br>`search doc` |

### 🔹 Persistencia y Sistema

| Comando | Descripción |
|---------|-------------|
| `save` | Guarda manualmente el estado actual del sistema (se hace automáticamente al salir). |
| `load` | Carga el estado guardado desde el archivo JSON. |
| `cls` | Limpia la pantalla de la consola. |
| `help` | Muestra la lista de comandos disponibles. |
| `exit` | Guarda cambios automáticamente y cierra el programa. |

### 🔹 Pruebas de Rendimiento

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `perf_test [cantidad]` | Genera archivos de prueba y mide el rendimiento del Trie. Por defecto genera 1000 archivos. | `perf_test`<br>`perf_test 5000` |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Navegación Básica
```bash
fs:root> mkdir documentos
fs:root> cd documentos
fs:root/documentos> touch reporte.txt Contenido del reporte
fs:root/documentos> ls
reporte.txt (file)
fs:root/documentos> cd ..
fs:root>
```

### Ejemplo 2: Usar la Papelera
```bash
fs:root> touch temporal.txt
fs:root> rm temporal.txt
Enviado a papelera.
fs:root> trash
[0] temporal.txt (Venía de: root/temporal.txt)
fs:root> restore 0
Restaurado en root
fs:root> ls
temporal.txt (file)
```

### Ejemplo 3: Autocompletado
```bash
fs:root> touch foto_playa.jpg
fs:root> touch foto_montana.jpg
fs:root> search fo
['foto_montana.jpg', 'foto_playa.jpg']
# O presiona TAB después de escribir "fo" para autocompletar
```

### Ejemplo 4: Rutas Relativas
```bash
fs:root> mkdir fotos
fs:root> cd fotos
fs:root/fotos> mkdir vacaciones
fs:root/fotos> cd vacaciones
fs:root/fotos/vacaciones> cd ../..
fs:root>
```

---

## 🧠 Explicación Técnica - Estructuras de Datos

Este proyecto demuestra el uso práctico de estructuras de datos fundamentales en Ciencias de la Computación:

### 1️⃣ Árbol General (File System Hierarchy)

El sistema de archivos se modela como un **árbol N-ario** donde:

- **Nodo Raíz:** Es la carpeta `root`, punto de partida del sistema.
- **Nodos Internos (Carpetas):** Pueden contener una lista de hijos (`children`), que pueden ser archivos u otras carpetas.
- **Nodos Hoja (Archivos):** No tienen hijos y contienen datos en el atributo `content`.

#### Ventajas de esta Estructura:
- **Operación de Movimiento Eficiente:** Mover un archivo o carpeta completa es O(1) una vez localizado, ya que solo se cambia la referencia del nodo padre.
- **Jerarquía Natural:** La estructura de árbol refleja perfectamente la organización jerárquica de un sistema de archivos real.
- **Recorridos Recursivos:** Operaciones como listar recursivamente o indexar el Trie se implementan de forma natural con recursión.

#### Complejidad Algorítmica:
- **Búsqueda de archivo:** O(d × n) donde d es la profundidad y n es el promedio de hijos por nivel.
- **Inserción/Eliminación:** O(1) después de encontrar el nodo padre.
- **Mover sub-árbol completo:** O(1) (solo cambio de referencia).

---

### 2️⃣ Trie / Árbol de Prefijos (Búsqueda y Autocompletado)

Para el autocompletado con TAB y el comando `search`, se utiliza un **Trie (Árbol de Prefijos)**.

#### ¿Por qué un Trie?

En lugar de recorrer todo el árbol de carpetas cada vez que buscas algo (complejidad O(N) donde N es el total de archivos), el Trie permite:

- **Búsqueda por Prefijo:** Encuentra todas las coincidencias en tiempo O(L + M), donde:
  - L = longitud del prefijo buscado
  - M = número de coincidencias encontradas
  
- **Independencia del Tamaño Total:** El tiempo de búsqueda NO depende del número total de archivos en el sistema, solo de la longitud de la palabra buscada.

#### Funcionamiento:

1. **Indexación:** Al crear un archivo `foto.jpg`, se inserta en el Trie letra por letra:
   ```
   root
    └─ f
       └─ o
          └─ t
             └─ o
                └─ .
                   └─ j
                      └─ p
                         └─ g [marca: "foto.jpg"]
   ```

2. **Búsqueda:** Al buscar "fo", el Trie navega:
   - root → f → o
   - Luego recolecta todas las palabras que terminan en esa rama.

#### Complejidad del Trie:
- **Inserción:** O(L) donde L es la longitud del nombre del archivo.
- **Búsqueda por prefijo:** O(L + M) donde M es el número de resultados.
- **Espacio:** O(ALPHABET_SIZE × N × L) en el peor caso, pero optimizado en la práctica.

---

### 3️⃣ Normalización de Rutas

Implementamos un algoritmo robusto para manejar rutas complejas ingresadas por el usuario usando una **pila (stack)**:

```python
def normalizar_ruta(ruta):
    partes = ruta.split('/')
    partes_resueltas = []
    
    for p in partes:
        if p == '' or p == '.':
            continue  # Ignora barras dobles y directorio actual
        elif p == '..':
            if partes_resueltas and partes_resueltas[-1] != "root":
                partes_resueltas.pop()  # Sube un nivel
        else:
            partes_resueltas.append(p)
    
    return "/".join(partes_resueltas)
```

**Ejemplo:**
- Entrada: `root/docs/../fotos//./playa.jpg`
- Salida: `root/fotos/playa.jpg`

Esto previene errores de navegación y garantiza que las rutas sean consistentes.

---

## 📊 Pruebas de Rendimiento

El sistema incluye el comando `perf_test` para validar la eficiencia del Trie con grandes volúmenes de datos.

### Cómo Ejecutar las Pruebas:

```bash
fs:root> perf_test 1000
```

Esto hará:
1. Generar 1000 archivos de prueba.
2. Indexarlos todos en el Trie.
3. Realizar una búsqueda por prefijo.
4. Mostrar los tiempos de ejecución.

### Resultados Esperados:

```
[INFO] Generados 1000 archivos para prueba de performance.
  > Tiempo de Inserción (Nodos + Trie Indexing): 0.0234 segundos.
  > Tiempo de Búsqueda (Trie) entre 1000 elementos: 0.000123 segundos.
Resultado esperado del Trie: El tiempo de búsqueda debe ser casi instantáneo, sin importar la cantidad.
```

**Observación Importante:** A medida que aumentas la cantidad de archivos (prueba con 10,000 o 100,000), notarás que el tiempo de búsqueda se mantiene prácticamente constante, demostrando la eficiencia del Trie.

---

## 💾 Persistencia de Datos

El sistema guarda automáticamente el estado al ejecutar `exit`. Los datos se almacenan en:

```
./root/mi_filesystem.json
```

### Formato del Archivo JSON:

```json
{
  "filesystem": {
    "id": "abc123",
    "name": "root",
    "type": "folder",
    "content": null,
    "children": [...]
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

**Nota:** La papelera también se guarda y restaura, así que no pierdes elementos eliminados entre sesiones.

---

## 🎓 Conceptos Aplicados

Este proyecto demuestra:

- ✅ **Árboles N-arios** (Estructura jerárquica)
- ✅ **Tries / Árboles de Prefijos** (Búsqueda eficiente)
- ✅ **Pilas** (Stack para normalización de rutas)
- ✅ **Recursión** (Recorrido de árboles)
- ✅ **Serialización/Deserialización** (JSON)
- ✅ **Complejidad Algorítmica** (Análisis de eficiencia)
- ✅ **Diseño de Interfaces CLI** (User Experience)

---

## 📝 Notas Finales

- El sistema no permite crear archivos duplicados en la misma carpeta.
- Los IDs únicos (UUID) previenen conflictos al restaurar de la papelera.
- Las rutas siempre se normalizan antes de procesarse.
- El autocompletado con TAB funciona globalmente (busca en todo el sistema, no solo en la carpeta actual).

---

## 🐛 Troubleshooting

### El TAB no funciona en Windows
**Solución:** Instala `pyreadline3`:
```bash
pip install pyreadline3
```

### Error al cargar el archivo JSON
**Causa:** Archivo corrupto o formato inválido.  
**Solución:** Elimina `mi_filesystem.json` y el sistema creará uno nuevo.

### No puedo mover archivos
**Causa:** Probablemente ya existe un archivo con ese nombre en el destino.  
**Solución:** Renombra el archivo primero o elimina el archivo existente en el destino.

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

**¡Gracias por usar nuestro Sistema de Archivos!** 🚀

Si tienes preguntas o sugerencias, no dudes en contactarnos.