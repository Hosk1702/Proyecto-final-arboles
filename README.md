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
