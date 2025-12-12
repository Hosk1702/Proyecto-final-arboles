# Proyecto-final-arboles
Proyecto final para la materia estructura de datos

# 📂 Mini-Suite de Sistema de Archivos (CLI)

> **Materia:** Estructura de Datos  
> **Integrantes:** Marco Antonio Velazquez Gaxiola, Yahir Agustin Soto Campos  
> **Fecha:** Diciembre 2025

Este proyecto implementa una simulación de un Sistema de Archivos en consola utilizando **Python**. El objetivo principal es aplicar estructuras de datos no lineales para gestionar jerarquías y búsquedas eficientes.

---

## 🚀 Características Principales

* **Gestión de Jerarquías:** Utiliza un **Árbol General** donde las carpetas pueden tener $N$ hijos.
* **Búsqueda Optimizada:** Implementación de un **Trie (Árbol de Prefijos)** para autocompletado y búsqueda instantánea.
* **Persistencia de Datos:** Guarda y carga el estado del sistema (incluyendo la papelera) en archivos `JSON`.
* **Papelera de Reciclaje:** Sistema de borrado lógico con capacidad de restauración.
* **Pruebas de Rendimiento:** Comando integrado para medir la eficiencia de las estructuras con miles de nodos.

---

## 🛠️ Instalación y Requisitos

Este proyecto requiere **Python 3.x**.

### Dependencias
El sistema utiliza la librería estándar de Python. Sin embargo, para el autocompletado con la tecla `TAB` en **Windows**, es necesario instalar:

```bash
pip install pyreadline3

### Ejecución
Para iniciar la consola interactiva, navega a la carpeta del código y ejecuta:

```bash
cd src
python filesystem.py

---

### 2. Sección de Guía de Uso

Esta es la tabla de comandos. Copia todo el bloque siguiente:

```markdown
## 📖 Guía de Uso (Comandos)

Una vez dentro de la consola `fs:root>`, puedes utilizar los siguientes comandos:

### Navegación y Gestión
| Comando | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `cd <ruta>` | Cambia el directorio actual. Soporta rutas relativas (`..`) y absolutas. | `cd docs`, `cd ..` |
| `ls [ruta]` | Lista el contenido del directorio actual o de la ruta especificada. | `ls`, `ls root/fotos` |
| `mkdir <nombre>` | Crea un nuevo directorio en la ubicación actual. | `mkdir vacaciones` |
| `touch <nombre> [txt]` | Crea un archivo, opcionalmente con contenido. | `touch nota.txt Hola mundo` |
| `mv <origen> <destino>` | Mueve un archivo o carpeta a otra ubicación. | `mv nota.txt ../docs` |
| `ren <viejo> <nuevo>` | Renombra un archivo o carpeta. | `ren foto.jpg playa.jpg` |

### Papelera y Búsqueda
| Comando | Descripción |
| :--- | :--- |
| `rm <nombre>` | Envía un elemento a la papelera (borrado lógico). |
| `trash` | Muestra la lista de elementos en la papelera con su índice. |
| `restore <índice>` | Restaura un elemento de la papelera a su ruta original. |
| `empty` | Vacía la papelera permanentemente (borrado físico). |
| `search <prefijo>` | Busca archivos en todo el sistema que inicien con el texto dado (Autocompletado Trie). |

### Sistema
| Comando | Descripción |
| :--- | :--- |
| `save` | Guarda el estado actual en `mi_filesystem.json`. |
| `load` | Carga el estado desde el archivo JSON. |
| `cls` | Limpia la pantalla de la consola. |
| `exit` | Guarda cambios y cierra el programa. |

## 🧠 Explicación Técnica (Educacional)

Este proyecto demuestra el uso práctico de dos estructuras de datos fundamentales:

### 1. Árbol General (File System)
El sistema de archivos se modela como un árbol donde:
* **Nodo Raíz:** Es la carpeta `root`.
* **Carpetas:** Son nodos que pueden tener una lista de hijos (`children`).
* **Archivos:** Son nodos hoja (sin hijos) que contienen datos (`content`).

Esto permite operaciones como `mv` (mover sub-árboles) simplemente cambiando la referencia del nodo padre, lo cual es muy eficiente ($O(1)$ en movimiento, aunque requiere búsqueda previa).

### 2. Trie / Árbol de Prefijos (Buscador)
Para el autocompletado y el comando `search`, utilizamos un **Trie**.
* **¿Por qué un Trie?** A diferencia de recorrer todo el árbol de carpetas (que sería lento, $O(N)$), el Trie permite encontrar una palabra en un tiempo proporcional a la longitud de la palabra buscada ($O(L)$), sin importar cuántos archivos existan en total.
* **Funcionamiento:** Cada nodo del Trie representa una letra. Al crear un archivo `foto.jpg`, se inserta la ruta de letras `f -> o -> t -> o...`.

### 3. Normalización de Rutas
Implementamos un algoritmo robusto para manejar rutas complejas ingresadas por el usuario (ej: `root/docs/../fotos//./`), convirtiéndolas a su forma canónica antes de procesarlas para evitar errores de navegación.

## 📊 Pruebas de Rendimiento

El sistema incluye un comando especial `perf_test` para validar la eficiencia del Trie ante grandes volúmenes de datos.

### Cómo probarlo:
Ejecuta en la consola:
```bash
fs:root> perf_test 1000
