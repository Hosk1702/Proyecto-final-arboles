import json
import uuid
import os

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
        return True, f"Creado: {nombre}"

    def renombrar_nodo(self, ruta_nodo, nuevo_nombre):
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo.split('/'))
        if not nodo or not padre: 
            return False, "Error: Nodo no encontrado o es root."
            
        # Validar que no exista el nombre en los hermanos
        for hermano in padre.hijos:
            if hermano.nombre == nuevo_nombre:
                return False, f"Error: Ya existe '{nuevo_nombre}' en este destino."
        
        nodo.nombre = nuevo_nombre
        return True, f"Renombrado a {nuevo_nombre}"

    def eliminar_nodo(self, ruta_nodo):
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo.split('/'))
        if not nodo or not padre:
            return False, "Error: No se puede eliminar root o nodo no existe."
            
        padre.hijos.remove(nodo)
        self.papelera.append(nodo) 
        return True, "Nodo eliminado y enviado a papelera."

    def mover_nodo(self, ruta_origen, ruta_destino):
        """Implementación FALTANTE del Día 3."""
        nodo_mov, padre_orig = self._buscar_nodo_y_padre(ruta_origen.split('/'))
        nuevo_padre, _ = self._buscar_nodo_y_padre(ruta_destino.split('/'))

        if not nodo_mov or not padre_orig:
            return False, "Error: Origen no válido."
        if not nuevo_padre:
            return False, "Error: Destino no existe."
        if nuevo_padre.tipo_nodo == 'file':
            return False, "Error: No puedes mover algo dentro de un archivo."
            
        # Validar duplicados en destino
        for hijo in nuevo_padre.hijos:
            if hijo.nombre == nodo_mov.nombre:
                return False, "Error: Ya existe un archivo con ese nombre en el destino."

        # Mover: Sacar de uno y meter en otro
        padre_orig.hijos.remove(nodo_mov)
        nuevo_padre.hijos.append(nodo_mov)
        return True, f"Movido: {nodo_mov.nombre} a {ruta_destino}"

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
            return True, "Árbol cargado exitosamente."
        except Exception as e:
            return False, f"Error al cargar: {str(e)}"

if __name__ == "__main__":
    fs = ArbolGeneral()
    
    print("--- 1. Creando estructura inicial ---")
    fs.crear_nodo("root", "docs", "folder")
    fs.crear_nodo("root/docs", "tarea.txt", "file", "Contenido X")
    fs.crear_nodo("root", "fotos", "folder")
    
    print("--- 2. Probando Mover (Faltaba) ---")
    # Movemos tarea.txt de 'docs' a 'fotos'
    exito, msg = fs.mover_nodo("root/docs/tarea.txt", "root/fotos")
    print(msg)
    
    print("--- 3. Guardando en JSON (Día 4) ---")
    fs.guardar_arbol("./root/mi_filesystem.json")
    
    print("--- 4. Simulando reinicio (Cargar JSON) ---")
    fs_nuevo = ArbolGeneral()
    fs_nuevo.cargar_arbol("mi_filesystem.json")
    print("Árbol recargado, hijos en 'fotos':")
    # Verificamos si la tarea sigue ahí después de cargar
    for h in fs_nuevo.root.hijos:
        if h.nombre == "fotos":
            print([n.nombre for n in h.hijos])