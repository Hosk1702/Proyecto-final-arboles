import json
import uuid
import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.terminating_names = set() 

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insertar(self, name):
        node = self.root
        name_lower = name.lower()
        for char in name_lower:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.terminating_names.add(name) 

    def buscar_por_prefijo(self, prefix):
        node = self.root
        prefix_lower = prefix.lower()
        
        for char in prefix_lower:
            if char not in node.children:
                return [] 
            node = node.children[char]
            
        return sorted(list(node.terminating_names))


class Nodo:
    def __init__(self, nombre, tipo_nodo, contenido=None, id_existente=None):
        # Si cargamos desde JSON, usamos el ID que ya tenía, si es nuevo, generamos uno.
        self.id = id_existente if id_existente else str(uuid.uuid4())[:8]
        self.nombre = nombre
        self.tipo_nodo = tipo_nodo  # "file" o "folder"
        self.contenido = contenido
        self.hijos = []

    def to_dict(self):
        """Convierte el nodo a diccionario (Formato estándar JSON)."""
        return {
            "id": self.id,
            "name": self.nombre,
            "type": self.tipo_nodo,
            "content": self.contenido,
            "children": [hijo.to_dict() for hijo in self.hijos]
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye un nodo a partir de un diccionario (Para cargar JSON)."""
        nuevo = cls(data["name"], data["type"], data["content"], data["id"])
        # Recursividad: reconstruir también a los hijos
        for hijo_data in data["children"]:
            nuevo.hijos.append(cls.from_dict(hijo_data))
        return nuevo


class ArbolGeneral:
    def __init__(self):
        self.root = Nodo("root", "folder")
        self.papelera = [] # Lista temporal para nodos eliminados
        self.trie = Trie()

    def _indexar_trie_recursivamente(self, start_node):
        if start_node.nombre != "root":
            self.trie.insertar(start_node.nombre)
            
        for hijo in start_node.hijos:
            self._indexar_trie_recursivamente(hijo)

    def _actualizar_trie(self, operation, name_old=None, name_new=None):
        if operation == "create":
            self.trie.insertar(name_new)
        elif operation == "rename":
            self.trie.insertar(name_new)

    def _buscar_nodo_y_padre(self, ruta_partes):
        # Lógica auxiliar para encontrar un nodo y quién lo contiene
        if not ruta_partes or (len(ruta_partes) == 1 and ruta_partes[0] == "root"):
            return self.root, None
        
        # Ajuste: Si la ruta llega como string "root/carpeta", hacemos split si es necesario
        if isinstance(ruta_partes, str):
            ruta_partes = ruta_partes.split('/')
            
        if ruta_partes[0] == "root":
            ruta_partes = ruta_partes[1:]
        
        actual = self.root
        padre = None
        
        for nombre_parte in ruta_partes:
            encontrado = None
            for hijo in actual.hijos:
                if hijo.nombre == nombre_parte:
                    encontrado = hijo
                    break
            if encontrado is None:
                return None, None
            padre = actual
            actual = encontrado
        return actual, padre

    def crear_nodo(self, ruta_padre, nombre, tipo, contenido=None):
        padre, _ = self._buscar_nodo_y_padre(ruta_padre.split('/'))
        if not padre:
            return False, "Error: Ruta padre no existe."
        if padre.tipo_nodo == 'file':
            return False, "Error: No se puede crear dentro de un archivo."
        
        # Validar duplicados
        for hijo in padre.hijos:
            if hijo.nombre == nombre:
                return False, f"Error: '{nombre}' ya existe aquí."
                
        nuevo = Nodo(nombre, tipo, contenido)
        padre.hijos.append(nuevo)
        self._actualizar_trie("create", name_new=nombre)
        return True, f"Creado: {nombre}"

    def renombrar_nodo(self, ruta_nodo, nuevo_nombre):
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo.split('/'))
        if not nodo or not padre: 
            return False, "Error: Nodo no encontrado o es root."
            
        # Validar que no exista el nombre en los hermanos
        for hermano in padre.hijos:
            if hermano.nombre == nuevo_nombre:
                return False, f"Error: Ya existe '{nuevo_nombre}' en este destino."
        
        nombre_anterior = nodo.nombre
        nodo.nombre = nuevo_nombre
        self._actualizar_trie("rename", name_old=nombre_anterior, name_new=nuevo_nombre)
        return True, f"Renombrado a {nuevo_nombre}"

    def eliminar_nodo(self, ruta_nodo):
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo.split('/'))
        if not nodo or not padre:
            return False, "Error: No se puede eliminar root o nodo no existe."
            
        padre.hijos.remove(nodo)
        self.papelera.append(nodo) 
        return True, "Nodo eliminado y enviado a papelera."

    def mover_nodo(self, ruta_origen, ruta_destino):
        nodo_mov, padre_orig = self._buscar_nodo_y_padre(ruta_origen.split('/'))
        nuevo_padre, _ = self._buscar_nodo_y_padre(ruta_destino.split('/'))

        if not nodo_mov or not padre_orig:
            return False, "Error: Origen no válido."
        if not nuevo_padre or nuevo_padre.tipo_nodo == 'file':
            return False, "Error: Destino no existe o es un archivo."
            
        # Validar duplicados en destino
        for hijo in nuevo_padre.hijos:
            if hijo.nombre == nodo_mov.nombre:
                return False, "Error: Ya existe un archivo con ese nombre en el destino."

        # Mover: Sacar de uno y meter en otro
        padre_orig.hijos.remove(nodo_mov)
        nuevo_padre.hijos.append(nodo_mov)
        return True, f"Movido: {nodo_mov.nombre} a {ruta_destino}"

    def buscar_autocompletado(self, prefix):
        return self.trie.buscar_por_prefijo(prefix)

    def guardar_arbol(self, nombre_archivo="arbol.json"):
        """Guarda el estado actual en un archivo JSON físico."""
        try:
            with open(nombre_archivo, 'w') as f:
                json.dump(self.root.to_dict(), f, indent=4)
            return True, f"Árbol guardado en {nombre_archivo}"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"

    def cargar_arbol(self, nombre_archivo="arbol.json"):
        """Lee el JSON y reconstruye los objetos Nodo en memoria."""
        if not os.path.exists(nombre_archivo):
            return False, "El archivo no existe."
        
        try:
            with open(nombre_archivo, 'r') as f:
                data = json.load(f)
                # Reconstruimos usando el método estático from_dict
                self.root = Nodo.from_dict(data) 
                
                # Re-indexar Trie
                self.trie = Trie()
                self._indexar_trie_recursivamente(self.root)
                
            return True, "Árbol cargado exitosamente."
        except Exception as e:
            return False, f"Error al cargar: {str(e)}"

if __name__ == "__main__":
    
    fs = ArbolGeneral()
    
    print("--- 1. Creando estructura inicial y probando indexación ---")
    fs.crear_nodo("root", "documentos", "folder")
    fs.crear_nodo("root/documentos", "Reporte_final.txt", "file", "Contenido X")
    fs.crear_nodo("root", "fotos", "folder")
    fs.crear_nodo("root/fotos", "Foto_vacaciones.jpg", "file")
    fs.crear_nodo("root/fotos", "Foto_carnet.jpg", "file")
    
    
    print("\n--- 2. Probando Búsqueda por Prefijo (Autocompletado) ---")
    
    prefix_R = "R"
    resultados_R = fs.buscar_autocompletado(prefix_R)
    print(f"Resultados para '{prefix_R}': {resultados_R}")
    
    prefix_foto = "foto"
    resultados_foto = fs.buscar_autocompletado(prefix_foto)
    print(f"Resultados para '{prefix_foto}': {resultados_foto}")
    
    
    print("\n--- 3. Prueba de Consistencia: Renombrar y Autocompletado ---")
    fs.renombrar_nodo("root/fotos/Foto_carnet.jpg", "Foto_perfil.png")
    
    prefix_Foto = "Foto"
    resultados_cambio = fs.buscar_autocompletado(prefix_Foto)
    print(f"Resultados para '{prefix_Foto}' después de renombrar: {resultados_cambio}")
    
    
    print("\n--- 4. Guardando, Recargando y Probando Indexación ---")
    
    # Guardamos la estructura
    nombre_archivo = "test_mi_filesystem.json"
    fs.guardar_arbol(nombre_archivo)
    
    # Simulando reinicio
    fs_nuevo = ArbolGeneral()
    fs_nuevo.cargar_arbol(nombre_archivo)
    
    # Volvemos a probar el autocompletado en el árbol cargado
    resultados_recargados = fs_nuevo.buscar_autocompletado(prefix_R)
    print(f"Resultados para '{prefix_R}' en árbol cargado: {resultados_recargados}")
    
    # Limpieza
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)