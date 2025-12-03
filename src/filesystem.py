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

if __name__ == "__main__":
    root = nodo("root", "folder")
    
    # 2. Crear manualmente un archivo
    archivo = nodo("tarea.txt", "file", "Texto de prueba")
    
    root.hijos.append(archivo)

    print(json.dumps(root.to_dic(), indent=4))