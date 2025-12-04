import json
import uuid

class nodo:
    def __init__(self,nombre, tipo_nodo, contenido=None):
        self.id=str(uuid.uuid4())[:8]

        self.nombre = nombre
        self.tipo_nodo = tipo_nodo
        self.contenido = contenido

        self.hijos = []

    def to_dic(self):
        return{
            "Id": self.id,
            "Nombre": self.nombre,
            "Tipo": self.tipo_nodo,
            "Contenido": self.contenido,
            "Hijos": [hijo.to_dic() for hijo in self.hijos]
        }
class ArbolGeneral:
    
    def __init__(self):
        self.root = nodo("root","folder")
        self.papelera = []
        
    def _buscar_nodo_por_ruta(self,ruta_partes):
        if ruta_partes and ruta_partes[0] == "root":
            ruta_partes = ruta_partes[1:]
            
        if not ruta_partes:
            return self.root
        
        actual = self.root
        
        for nombre_parte in ruta_partes:
            encontrado = None
            for hijo in actual.hijos:
                if hijo.nombre == nombre_parte:
                    encontrado = hijo
                    break
            if encontrado is None:
                return None
            actual = encontrado
        return actual
    
    def _buscar_nodo_y_padre(self,ruta_partes):
        if not ruta_partes or (len(ruta_partes) == 1 and ruta_partes[0]=="root"):
            return self.root,None
        
        partes_ruta = ruta_partes.copy()
        if partes_ruta[0] == "root":
            partes_ruta = partes_ruta[1:]
        
        actual = self.root
        padre = None
        
        for i, nombre_parte in enumerate(partes_ruta):
            encontrado = None
            for hijo in actual.hijos:
                if hijo.nombre == nombre_parte:
                    encontrado = hijo
                    break
            if encontrado is None:
                return None,None
            padre = actual
            actual = encontrado
        return actual,padre
    
    #INSERCIION DE ELEMENTOS
    
    def crear_nodo_en_ruta(self,ruta_padre,nombre,tipo_nodo,contenido=None):
        partes = ruta_padre.split('/')
        nodo_padre = self._buscar_nodo_por_ruta(partes)
        
        if nodo_padre is None:
            return False,"Error: La ruta padre no se encontro"
        if nodo_padre.tipo_nodo == 'file':
            return False, "Error: No puede crearse un nodo dentro de un archivo"
        
        for hijo in nodo_padre.hijos:
            if hijo.nombre == nombre:
                return False,f"Error: Ya existe un nodo llamado '{nombre}' en esta ruta"
        
        nuevo_nodo = nodo(nombre,tipo_nodo,contenido)
        nodo_padre.hijos.append(nuevo_nodo)
        return True, f"'{tipo_nodo.capitalize()}' '{nombre}' creado en '{ruta_padre}'"
    
    # DÍA 3: RENOMBRAR
    
    def renombrar_nodo(self, ruta_nodo, nuevo_nombre):
        partes = ruta_nodo.split('/')
        nodo_a_renombrar, nodo_padre = self._buscar_nodo_y_padre(partes)

        if nodo_a_renombrar is None:
            return False, "Error: Nodo a renombrar no encontrado."
        
        if nodo_a_renombrar == self.root:
            return False, "Error: No se puede renombrar el nodo raíz 'root'."

        for hijo in nodo_padre.hijos:
            if hijo != nodo_a_renombrar and hijo.nombre == nuevo_nombre:
                return False, f"Error: Ya existe un nodo llamado '{nuevo_nombre}' en el padre."
        
        nombre_anterior = nodo_a_renombrar.nombre
        nodo_a_renombrar.nombre = nuevo_nombre
        
        return True, f"Nodo '{nombre_anterior}' renombrado a '{nuevo_nombre}'."

    # DÍA 3: ELIMINAR CON PAPELERA
    
    def eliminar_nodo(self, ruta_nodo):
        partes = ruta_nodo.split('/')
        nodo_a_eliminar, nodo_padre = self._buscar_nodo_y_padre(partes)

        if nodo_a_eliminar is None:
            return False, "Error: Nodo a eliminar no encontrado."
        
        if nodo_a_eliminar == self.root:
            return False, "Error: No se puede eliminar el nodo raíz 'root'."

        try:
            nodo_padre.hijos.remove(nodo_a_eliminar)
        except ValueError:
            return False, "Error interno al intentar eliminar el nodo."

        self.papelera.append(nodo_a_eliminar)
        
        return True, f"Nodo '{nodo_a_eliminar.nombre}' eliminado y enviado a la papelera."
    
    def exportar_json(self):
        return json.dumps(self.root.to_dic(), indent=4)    

if __name__ == "__main__":
    root = nodo("root", "folder")
    
    # 2. Crear manualmente un archivo
    archivo = nodo("tarea.txt", "file", "Texto de prueba")
    
    root.hijos.append(archivo)

    print(json.dumps(root.to_dic(), indent=4))