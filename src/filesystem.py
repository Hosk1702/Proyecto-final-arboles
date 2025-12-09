import json
import uuid
import os
import sys

# --- PARTE 1: EL BUSCADOR INTELIGENTE (Trie) ---
# Imagina que esto es un índice telefónico que se actualiza solo.
# Sirve para que cuando busques "fo", te encuentre rápido "fotos", "folder", etc.

class TrieNode:
    def __init__(self):
        # Cada nodo es una letra. 'children' son las letras que siguen.
        self.children = {}
        # Aquí anotamos los nombres completos que terminan aquí.
        self.terminating_names = set() 

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insertar(self, name):
        # Agrega una palabra nueva al índice, letra por letra.
        node = self.root
        name_lower = name.lower()
        for char in name_lower:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.terminating_names.add(name) 
    
    def eliminar(self, name):
        # Borra un nombre del índice para que ya no aparezca en las búsquedas.
        node = self.root
        name_lower = name.lower()
        for char in name_lower:
            if char not in node.children:
                return
            node = node.children[char]
        if name in node.terminating_names:
            node.terminating_names.remove(name)

    def buscar_por_prefijo(self, prefix):
        # Esta es la función que usa el comando 'search'.
        # Tú le das el inicio de una palabra y él te devuelve todas las coincidencias.
        node = self.root
        prefix_lower = prefix.lower()
        for char in prefix_lower:
            if char not in node.children:
                return [] 
            node = node.children[char]
        return sorted(list(node.terminating_names))


# --- PARTE 2: LOS "LADRILLOS" DEL SISTEMA (Carpetas y Archivos) ---
# Aquí definimos qué es un archivo o una carpeta.

class Nodo:
    def __init__(self, nombre, tipo_nodo, contenido=None, id_existente=None):
        # Le damos un ID único (como una cédula), su nombre y si es archivo o carpeta.
        self.id = id_existente if id_existente else str(uuid.uuid4())[:8]
        self.nombre = nombre
        self.tipo_nodo = tipo_nodo
        self.contenido = contenido
        # 'hijos' es la lista de cosas que guardamos DENTRO de esta carpeta.
        self.hijos = []

    def to_dict(self):
        # Convierte este archivo/carpeta en texto para poder guardarlo en el disco duro.
        return {
            "id": self.id,
            "name": self.nombre,
            "type": self.tipo_nodo,
            "content": self.contenido,
            "children": [hijo.to_dict() for hijo in self.hijos]
        }

    @classmethod
    def from_dict(cls, data):
        # Hace lo contrario: lee el texto guardado y reconstruye el archivo/carpeta en la memoria.
        nuevo = cls(data["name"], data["type"], data["content"], data["id"])
        # También reconstruye todo lo que tenía adentro (sus hijos).
        for hijo_data in data["children"]:
            nuevo.hijos.append(cls.from_dict(hijo_data))
        return nuevo


# --- PARTE 3: EL CEREBRO (El Árbol General) ---
# Aquí es donde ocurren todas las acciones: crear, borrar, mover, etc.

class ArbolGeneral:
    def __init__(self):
        # Creamos la carpeta principal "root" donde empieza todo.
        self.root = Nodo("root", "folder")
        # Preparamos la papelera de reciclaje.
        self.papelera = [] 
        # Iniciamos el buscador.
        self.trie = Trie()

    # --- HERRAMIENTAS INTERNAS (Auxiliares) ---
    
    def _indexar_trie_recursivamente(self, start_node):
        # Recorre todas las carpetas para "enseñarle" al buscador qué archivos existen al inicio.
        if start_node.nombre != "root":
            self.trie.insertar(start_node.nombre)
        for hijo in start_node.hijos:
            self._indexar_trie_recursivamente(hijo)

    def _actualizar_trie(self, operation, name_old=None, name_new=None):
        # Mantiene el buscador al día cuando creamos o borramos algo.
        if operation == "create":
            self.trie.insertar(name_new)
        elif operation == "rename":
            if name_old: self.trie.eliminar(name_old)
            self.trie.insertar(name_new)
        elif operation == "delete":
            if name_old: self.trie.eliminar(name_old)

    def _buscar_nodo_y_padre(self, ruta_partes):
        # Esta función es como un GPS. Le das una dirección (ej. "root/fotos/playa")
        # y te devuelve el objeto "playa" y su carpeta contenedora "fotos".
        if isinstance(ruta_partes, str):
            ruta_partes = ruta_partes.split('/')
            
        # Limpieza: quitamos partes vacías por si pusiste barras dobles (//).
        ruta_partes = [p for p in ruta_partes if p]

        if not ruta_partes or (len(ruta_partes) == 1 and ruta_partes[0] == "root"):
            return self.root, None
            
        if ruta_partes[0] == "root":
            ruta_partes = ruta_partes[1:]
        
        actual = self.root
        padre = None
        
        # Va saltando de carpeta en carpeta hasta encontrar lo que buscas.
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

    def _obtener_hijos_formato(self, nodo):
        # Prepara una lista bonita de nombres para mostrarla en pantalla.
        return [f"{h.nombre} ({h.tipo_nodo})" for h in nodo.hijos]

    def validar_ruta(self, ruta):
        # Verifica si una dirección existe y si es una carpeta (útil para el comando cd).
        nodo, _ = self._buscar_nodo_y_padre(ruta)
        if not nodo:
            return False, "Esa ruta no existe."
        if nodo.tipo_nodo == 'file':
            return False, "Eso es un archivo, no una carpeta. No puedes entrar ahí."
        return True, "OK"

    # --- ACCIONES PRINCIPALES (Los comandos que usarás) ---

    def crear_nodo(self, ruta_padre, nombre, tipo, contenido=None):
        # Crea carpetas o archivos nuevos.
        padre, _ = self._buscar_nodo_y_padre(ruta_padre)
        if not padre: return False, "Error: La carpeta donde quieres crear esto no existe."
        if padre.tipo_nodo == 'file': return False, "Error: No puedes meter cosas dentro de un archivo."
        
        # Revisa que no exista ya algo con el mismo nombre.
        for hijo in padre.hijos:
            if hijo.nombre == nombre: return False, f"Error: Ya existe '{nombre}' aquí."
                
        nuevo = Nodo(nombre, tipo, contenido)
        padre.hijos.append(nuevo)
        # Avisamos al buscador que hay algo nuevo.
        self._actualizar_trie("create", name_new=nombre)
        return True, f"Listo, creado: {nombre}"

    def mover_nodo(self, ruta_origen, ruta_destino):
        # Mueve cosas de un lugar a otro.
        nodo_mov, padre_orig = self._buscar_nodo_y_padre(ruta_origen)
        nuevo_padre, _ = self._buscar_nodo_y_padre(ruta_destino)

        if not nodo_mov or not padre_orig: return False, "No encuentro lo que quieres mover."
        if not nuevo_padre or nuevo_padre.tipo_nodo == 'file': return False, "El destino no es válido."
            
        for hijo in nuevo_padre.hijos:
            if hijo.nombre == nodo_mov.nombre: return False, "Ya hay algo con ese nombre en el destino."

        # Lo sacamos de la carpeta vieja y lo ponemos en la nueva.
        padre_orig.hijos.remove(nodo_mov)
        nuevo_padre.hijos.append(nodo_mov)
        return True, f"Movido exitosamente a {ruta_destino}"

    def renombrar_nodo(self, ruta_nodo, nuevo_nombre):
        # Cambia el nombre de un archivo.
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo)
        if not nodo or not padre: return False, "No encuentro el archivo."
            
        for hermano in padre.hijos:
            if hermano.nombre == nuevo_nombre: return False, "Ya existe ese nombre aquí."
        
        nombre_anterior = nodo.nombre
        nodo.nombre = nuevo_nombre
        # Actualizamos el buscador con el cambio de nombre.
        self._actualizar_trie("rename", name_old=nombre_anterior, name_new=nuevo_nombre)
        return True, f"Renombrado a {nuevo_nombre}"
    
    def buscar_autocompletado(self, prefix):
        # Busca coincidencias en el índice.
        return self.trie.buscar_por_prefijo(prefix)
    
    def listar_directorio(self, ruta):
        # Muestra qué hay dentro de una carpeta.
        nodo, _ = self._buscar_nodo_y_padre(ruta)
        if not nodo: return False, "Ruta no encontrada."
        if nodo.tipo_nodo == 'file':
            return True, f"Es un archivo: {nodo.nombre} (Tiene {len(str(nodo.contenido))} letras)"
        
        if not nodo.hijos:
            return True, "(carpeta vacía)"
        return True, "\n".join(self._obtener_hijos_formato(nodo))

    # --- PAPELERA Y RESTAURACIÓN ---

    def eliminar_nodo(self, ruta_nodo):
        # En lugar de borrar, mueve el archivo a la Papelera.
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo)
        if not nodo or not padre: return False, "No se puede eliminar (¿es root o no existe?)."
            
        padre.hijos.remove(nodo)
        self._actualizar_trie("delete", name_old=nodo.nombre)
        
        # Guardamos de DÓNDE venía para saber dónde restaurarlo luego.
        item_papelera = {
            "path_origen": ruta_nodo,
            "path_padre": "/".join(ruta_nodo.split('/')[:-1]),
            "nodo": nodo
        }
        self.papelera.append(item_papelera) 
        return True, "Enviado a papelera."

    def ver_papelera(self):
        # Muestra la lista de cosas borradas.
        if not self.papelera: return "La papelera está vacía."
        salida = []
        for idx, item in enumerate(self.papelera):
            salida.append(f"[{idx}] {item['nodo'].nombre} (Venía de: {item['path_origen']})")
        return "\n".join(salida)

    def restaurar_nodo(self, indice):
        # Recupera algo de la basura.
        try:
            idx = int(indice)
            if idx < 0 or idx >= len(self.papelera): return False, "Número inválido."
        except ValueError: return False, "Debes darme el número del archivo."

        item = self.papelera[idx]
        nodo_a_restaurar = item['nodo']
        path_padre_str = item['path_padre']

        # Verificamos si la carpeta original todavía existe.
        padre, _ = self._buscar_nodo_y_padre(path_padre_str)
        if not padre: return False, "La carpeta original ya no existe, no sé dónde ponerlo."

        for hijo in padre.hijos:
            if hijo.nombre == nodo_a_restaurar.nombre: return False, "Conflicto: Ya hay un archivo con ese nombre ahí."

        padre.hijos.append(nodo_a_restaurar)
        self.papelera.pop(idx)
        self._actualizar_trie("create", name_new=nodo_a_restaurar.nombre)
        return True, f"Restaurado en {path_padre_str}"

    def vaciar_papelera(self):
        # Borra todo definitivamente.
        c = len(self.papelera)
        self.papelera = []
        return True, f"Se eliminaron {c} elementos para siempre."

    # --- GUARDAR Y CARGAR EN DISCO ---

    def guardar_arbol(self, nombre_archivo="./root/mi_filesystem.json"):
        # Guarda todo (carpetas y papelera) en un archivo real.
        try:
            # Preparamos la papelera para guardarla.
            papelera_serializada = []
            for item in self.papelera:
                papelera_serializada.append({
                    "path_origen": item["path_origen"],
                    "path_padre": item["path_padre"],
                    "nodo": item["nodo"].to_dict()
                })
            # Juntamos árbol y papelera en un solo paquete.
            data = {"filesystem": self.root.to_dict(), "trash": papelera_serializada}
            
            with open(nombre_archivo, 'w') as f: json.dump(data, f, indent=4)
            return True, f"Guardado correctamente en {nombre_archivo}"
        except Exception as e: return False, str(e)

    def cargar_arbol(self, nombre_archivo="./root/mi_filesystem.json"):
        # Lee el archivo y reconstruye todo tal cual estaba.
        if not os.path.exists(nombre_archivo): return False, "No encuentro el archivo de guardado."
        try:
            with open(nombre_archivo, 'r') as f:
                data = json.load(f)
                # Detectamos si es formato nuevo o viejo.
                if "filesystem" in data:
                    root_data, trash_data = data["filesystem"], data.get("trash", [])
                else: root_data, trash_data = data, []

                # Reconstruimos memoria.
                self.root = Nodo.from_dict(root_data)
                self.papelera = []
                for item in trash_data:
                    self.papelera.append({
                        "path_origen": item["path_origen"],
                        "path_padre": item["path_padre"],
                        "nodo": Nodo.from_dict(item["nodo"])
                    })
                # Reconstruimos el índice del buscador.
                self.trie = Trie()
                self._indexar_trie_recursivamente(self.root)
            return True, "Sistema cargado correctamente."
        except Exception as e: return False, str(e)


# --- PARTE 4: LA CONSOLA (Donde escribes los comandos) ---

def resolver_ruta_absoluta(ruta_input, ruta_actual):
    # Esta función ayuda a entender dónde estás.
    # Si escribes "fotos", ella sabe que te refieres a "root/docs/fotos" (si estás en docs).
    if ruta_input == "root" or ruta_input.startswith("root/"):
        return ruta_input  # Si ya escribiste la ruta completa, la usamos tal cual.
    
    # Si no, le pegamos la carpeta actual al principio.
    if ruta_actual == "root":
        return f"{ruta_actual}/{ruta_input}"
    else:
        return f"{ruta_actual}/{ruta_input}"

def limpiarpantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
def imprimir_ayuda():
    # Esta función es tu "chivo" o acordeón. Muestra la lista de todo lo que puedes hacer
    # para que no tengas que memorizarlo.
    print("\n--- Comandos que puedes usar ---")
    
    # Comandos de movimiento y visualización
    print("  cd <carpeta>          : Entrar a una carpeta (Usa '..' para regresar o '/' para ir al inicio)")
    print("  ls [carpeta]          : Ver qué hay adentro (si no pones nada, muestra la carpeta donde estás)")
    
    # Comandos para crear y borrar
    print("  mkdir <nombre>        : Crear una carpeta nueva aquí mismo")
    print("  touch <nombre> [txt]  : Crear un archivo nuevo aquí mismo (opcional: ponle texto al final)")
    print("  mv <origen> <destino> : Mover un archivo o carpeta a otro lugar")
    print("  rm <nombre>           : Borrar algo (tranquilo, se va a la papelera primero)")
    
    # Comandos de la Papelera
    print("  trash                 : Ver qué cosas has borrado (la basura)")
    print("  restore <numero>      : Rescatar algo de la basura (usa el numerito que sale al poner 'trash')")
    print("  empty                 : Vaciar la basura para siempre (cuidado, esto sí borra todo)")
    
    # Comandos avanzados y del sistema
    print("  search <texto>        : Buscar archivos rapidísimo escribiendo solo el inicio del nombre")
    print("  load                  : Cargar lo que tenías guardado antes")
    print("  cls                   : Limpiar el historial de la pantalla")
    print("  exit                  : Salir del programa")

def main():
    fs = ArbolGeneral()
    
    # Variable que recuerda en qué carpeta estás parado ahora mismo.
    current_path = "root" 

    print("=== SISTEMA DE ARCHIVOS ===")
    exito, msg = fs.cargar_arbol()
    if exito: print(f"[INFO] {msg}")

    # Bucle infinito: Pide comandos hasta que digas 'exit'.
    while True:
        # El texto inicial te muestra dónde estás (ej: fs:root/fotos> ).
        try:
            comando_input = input(f"\nfs:{current_path}> ").strip().split()
        except EOFError: break
            
        if not comando_input: continue
        cmd = comando_input[0].lower() # El comando (ej: mkdir)
        args = comando_input[1:]       # Los detalles (ej: carpeta1)

        if cmd == "exit": 
            fs.guardar_arbol()[1]
            break
        
        elif cmd == "cd":
            # Comando para cambiar de carpeta (Navegar).
            if len(args) < 1:
                print("Dime a dónde ir. Ej: cd carpeta | cd .. (atrás) | cd / (inicio)")
                continue
            
            destino = args[0]
            
            # Opción 1: Ir al inicio (root)
            if destino == "/" or destino == "root":
                current_path = "root"
            
            # Opción 2: Ir atrás un paso (..)
            elif destino == "..":
                if current_path == "root":
                    print("Ya estás en el inicio, no puedes subir más.")
                else:
                    # Borramos la última parte de la ruta para subir.
                    partes = current_path.split('/')
                    current_path = "/".join(partes[:-1])
            
            # Opción 3: Entrar a una carpeta normal
            else:
                # Calculamos cuál sería la ruta completa.
                ruta_tentativa = resolver_ruta_absoluta(destino, current_path)
                
                # Le preguntamos al sistema si esa carpeta existe de verdad.
                ok, msg = fs.validar_ruta(ruta_tentativa)
                if ok:
                    current_path = ruta_tentativa
                else:
                    print(f"Error: {msg}")

        elif cmd == "ls":
            # Listar archivos.
            # Si no escribes nada, muestra lo que hay donde estás parado.
            if len(args) == 0:
                target = current_path
            else:
                # Si escribes una ruta, muestra lo que hay allá.
                target = resolver_ruta_absoluta(args[0], current_path)
            
            ok, res = fs.listar_directorio(target)
            print(res)

        elif cmd == "mkdir":
            # Crear carpeta.
            if not args: print("Faltó el nombre. Uso: mkdir <nombre>")
            else:
                nombre_nuevo = args[0]
                # La crea justo donde estás parado.
                ok, msg = fs.crear_nodo(current_path, nombre_nuevo, "folder")
                print(msg)

        elif cmd == "touch":
            # Crear archivo.
            if not args: print("Faltó el nombre. Uso: touch <nombre> [texto]")
            else:
                nombre_nuevo = args[0]
                contenido = " ".join(args[1:]) if len(args) > 1 else ""
                ok, msg = fs.crear_nodo(current_path, nombre_nuevo, "file", contenido)
                print(msg)

        elif cmd == "mv":
             # Mover archivo. Aquí sí necesitas escribir las rutas completas o relativas.
            if len(args) < 2: print("Faltan datos. Uso: mv <origen> <destino>")
            else:
                # Resolvemos las rutas por si usas nombres cortos.
                origen = resolver_ruta_absoluta(args[0], current_path)
                destino = resolver_ruta_absoluta(args[1], current_path)
                ok, msg = fs.mover_nodo(origen, destino)
                print(msg)

        elif cmd == "rm":
            # Eliminar (a papelera).
            if not args: print("Faltó el nombre. Uso: rm <nombre>")
            else:
                target = resolver_ruta_absoluta(args[0], current_path)
                ok, msg = fs.eliminar_nodo(target)
                print(msg)

        elif cmd == "trash": print(fs.ver_papelera())
        elif cmd == "restore":
            if args: print(fs.restaurar_nodo(args[0])[1])
            else: print("Falta el número de la papelera.")
        elif cmd == "empty": print(fs.vaciar_papelera()[1])
        elif cmd == "search":
            if args: print(fs.buscar_autocompletado(args[0]))
            else: print("Escribe qué buscar.")
        elif cmd == "load": 
            print(fs.cargar_arbol()[1])
            current_path = "root" # Al cargar de nuevo, te regresamos al inicio por seguridad.
        elif cmd == "cls":
            limpiarpantalla()
        elif cmd == "help":
            imprimir_ayuda()
        else:
            print("No entiendo ese comando.")                                     

if __name__ == "__main__":
    main()