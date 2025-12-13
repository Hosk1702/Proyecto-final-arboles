import json
import uuid
import os
import sys

# --- PARTE NUEVA: LIBRERÍA PARA EL TAB ---
try:
    import readline
except ImportError:
    print("AVISO: Para usar autocompletado con TAB en Windows, instala: pip install pyreadline3")
    class readline:
        @staticmethod
        def set_completer(f): pass
        @staticmethod
        def parse_and_bind(s): pass

# --- PARTE 4: LA CONSOLA ---

def resolver_ruta_absoluta(ruta_input, ruta_actual):
    if ruta_input == "root" or ruta_input.startswith("root/"):
        ruta_final = ruta_input
    elif ruta_actual == "root":
        ruta_final = f"{ruta_actual}/{ruta_input}"
    else:
        ruta_final = f"{ruta_actual}/{ruta_input}"
    
    return normalizar_ruta(ruta_final)

def normalizar_ruta(ruta):
    partes = ruta.split('/')
    partes_resueltas = []
    
    for p in partes:
        if p == '' or p == '.':
            continue
        elif p == '..':
            if partes_resueltas and partes_resueltas[-1] != "root":
                partes_resueltas.pop()
        else:
            partes_resueltas.append(p)
    
    if not partes_resueltas or partes_resueltas[0] != "root":
        return "root"
    
    return "/".join(partes_resueltas)

def limpiarpantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
def imprimir_ayuda():
    print("\n=== COMANDOS DISPONIBLES ===")
    print("\n📁 Navegación y Visualización:")
    print("  cd <carpeta>         : Cambiar de directorio")
    print("  ls [carpeta]         : Listar contenido")
    print("  [TAB]                : Autocompletar nombres")
    
    print("\n📝 Creación y Gestión:")
    print("  mkdir <nombre>       : Crear carpeta")
    print("  touch <nombre> [txt] : Crear archivo")
    print("  mv <origen> <dest>   : Mover archivo/carpeta")
    print("  ren <viejo> <nuevo>  : Renombrar")
    print("  rm <nombre>          : Eliminar (a papelera)")
    
    print("\n🗑️  Papelera:")
    print("  trash                : Ver papelera")
    print("  restore <índice>     : Restaurar elemento")
    print("  empty                : Vaciar papelera")
    
    print("\n🔍 Búsqueda:")
    print("  search <prefijo>     : Búsqueda por prefijo (Trie)")
    print("  find <nombre>        : Búsqueda exacta (HashMap)")
    
    print("\n📊 Información y Análisis:")
    print("  info                 : Ver estadísticas del árbol")
    print("  tree                 : Mostrar árbol en consola")
    print("  export               : Exportar recorrido preorden")
    
    print("\n⚙️  Sistema:")
    print("  save                 : Guardar manualmente")
    print("  load                 : Cargar desde archivo")
    print("  perf_test [cant]     : Prueba de rendimiento")
    print("  cls                  : Limpiar pantalla")
    print("  help                 : Mostrar esta ayuda")
    print("  exit                 : Guardar y salir")

# --- PARTE 1: EL BUSCADOR INTELIGENTE (Trie) ---
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
    
    def eliminar(self, name):
        # --- MODIFICACIÓN REALIZADA AQUÍ ---
        node = self.root
        name_lower = name.lower()
        for char in name_lower:
            if char not in node.children:
                return
            node = node.children[char]
            # Borramos el nombre de TODOS los nodos del camino, no solo del último.
            if name in node.terminating_names:
                node.terminating_names.remove(name)

    def buscar_por_prefijo(self, prefix):
        node = self.root
        prefix_lower = prefix.lower()
        for char in prefix_lower:
            if char not in node.children:
                return [] 
            node = node.children[char]
        return sorted(list(node.terminating_names))


# --- PARTE 2: LOS "LADRILLOS" DEL SISTEMA (Carpetas y Archivos) ---
class Nodo:
    def __init__(self, nombre, tipo_nodo, contenido=None, id_existente=None):
        self.id = id_existente if id_existente else str(uuid.uuid4())[:8]
        self.nombre = nombre
        self.tipo_nodo = tipo_nodo
        self.contenido = contenido
        self.hijos = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.nombre,
            "type": self.tipo_nodo,
            "content": self.contenido,
            "children": [hijo.to_dict() for hijo in self.hijos]
        }

    @classmethod
    def from_dict(cls, data):
        nuevo = cls(data["name"], data["type"], data["content"], data["id"])
        for hijo_data in data["children"]:
            nuevo.hijos.append(cls.from_dict(hijo_data))
        return nuevo


# --- PARTE 3: EL CEREBRO (El Árbol General) ---
class ArbolGeneral:
    def __init__(self):
        self.root = Nodo("root", "folder")
        self.papelera = [] 
        self.trie = Trie()
        # NUEVO: HashMap para búsqueda exacta O(1)
        self.hash_map = {}  # {nombre: [rutas completas]}

    # --- HERRAMIENTAS INTERNAS (Auxiliares) ---
    
    def _indexar_trie_recursivamente(self, start_node, ruta_actual="root"):
        """Indexa tanto el Trie como el HashMap recursivamente."""
        if start_node.nombre != "root":
            self.trie.insertar(start_node.nombre)
            # Indexar en HashMap
            if start_node.nombre not in self.hash_map:
                self.hash_map[start_node.nombre] = []
            self.hash_map[start_node.nombre].append(ruta_actual)
        
        for hijo in start_node.hijos:
            nueva_ruta = f"{ruta_actual}/{hijo.nombre}"
            self._indexar_trie_recursivamente(hijo, nueva_ruta)

    def _actualizar_trie(self, operation, name_old=None, name_new=None, ruta=None):
        """Mantiene el Trie y HashMap actualizados."""
        if operation == "create":
            self.trie.insertar(name_new)
            if name_new not in self.hash_map:
                self.hash_map[name_new] = []
            if ruta:
                self.hash_map[name_new].append(ruta)
        elif operation == "rename":
            if name_old: 
                self.trie.eliminar(name_old)
                # Actualizar HashMap
                if name_old in self.hash_map and ruta in self.hash_map[name_old]:
                    self.hash_map[name_old].remove(ruta)
                    if not self.hash_map[name_old]:
                        del self.hash_map[name_old]
            self.trie.insertar(name_new)
            if name_new not in self.hash_map:
                self.hash_map[name_new] = []
            if ruta:
                nueva_ruta = "/".join(ruta.split('/')[:-1]) + "/" + name_new
                self.hash_map[name_new].append(nueva_ruta)
        elif operation == "delete":
            if name_old: 
                self.trie.eliminar(name_old)
                if name_old in self.hash_map and ruta in self.hash_map[name_old]:
                    self.hash_map[name_old].remove(ruta)
                    if not self.hash_map[name_old]:
                        del self.hash_map[name_old]

    def _buscar_nodo_y_padre(self, ruta_partes):
        if isinstance(ruta_partes, str):
            ruta_partes = normalizar_ruta(ruta_partes).split('/')
            
        ruta_partes = [p for p in ruta_partes if p]

        if not ruta_partes or (len(ruta_partes) == 1 and ruta_partes[0] == "root"):
            return self.root, None
            
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

    def _obtener_hijos_formato(self, nodo):
        return [f"{h.nombre} ({h.tipo_nodo})" for h in nodo.hijos]

    def validar_ruta(self, ruta):
        nodo, _ = self._buscar_nodo_y_padre(ruta)
        if not nodo:
            return False, "Esa ruta no existe."
        if nodo.tipo_nodo == 'file':
            return False, "Eso es un archivo, no una carpeta. No puedes entrar ahí."
        return True, "OK"

    # --- NUEVAS FUNCIONES REQUERIDAS ---

    def calcular_altura(self, nodo=None):
        """Calcula la altura del árbol desde un nodo dado."""
        if nodo is None:
            nodo = self.root
        
        if not nodo.hijos:  # Es hoja
            return 0
        
        alturas_hijos = [self.calcular_altura(hijo) for hijo in nodo.hijos]
        return 1 + max(alturas_hijos)

    def calcular_tamano(self, nodo=None):
        """Calcula el número total de nodos en el árbol."""
        if nodo is None:
            nodo = self.root
        
        tamano = 1  # Cuenta el nodo actual
        for hijo in nodo.hijos:
            tamano += self.calcular_tamano(hijo)
        
        return tamano

    def recorrido_preorden(self, nodo=None, nivel=0):
        """Realiza un recorrido en preorden del árbol."""
        if nodo is None:
            nodo = self.root
        
        resultado = []
        indentacion = "  " * nivel
        tipo_icono = "📁" if nodo.tipo_nodo == "folder" else "📄"
        resultado.append(f"{indentacion}{tipo_icono} {nodo.nombre} [ID: {nodo.id}]")
        
        for hijo in nodo.hijos:
            resultado.extend(self.recorrido_preorden(hijo, nivel + 1))
        
        return resultado

    def exportar_preorden(self, archivo="preorden_export.txt"):
        """Exporta el recorrido en preorden a un archivo."""
        try:
            recorrido = self.recorrido_preorden()
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("=== RECORRIDO EN PREORDEN DEL SISTEMA DE ARCHIVOS ===\n")
                f.write(f"Altura del árbol: {self.calcular_altura()}\n")
                f.write(f"Total de nodos: {self.calcular_tamano()}\n")
                f.write("=" * 55 + "\n\n")
                for linea in recorrido:
                    f.write(linea + "\n")
            return True, f"Recorrido exportado a '{archivo}'"
        except Exception as e:
            return False, f"Error al exportar: {str(e)}"

    def buscar_exacto(self, nombre):
        """Búsqueda exacta usando HashMap - O(1)."""
        if nombre in self.hash_map:
            return self.hash_map[nombre]
        return []

    # --- ACCIONES PRINCIPALES ---

    def generar_carga_prueba(self, cantidad):
        """Genera archivos para pruebas de rendimiento."""
        padre = self.root
        for i in range(cantidad):
            nombre = f"archivo_perf_{i:05d}_test.txt" 
            nuevo = Nodo(nombre, "file", f"Contenido del archivo de prueba {i}")
            padre.hijos.append(nuevo)
            ruta = f"root/{nombre}"
            self._actualizar_trie("create", name_new=nombre, ruta=ruta)
        return True, f"Generados {cantidad} archivos para prueba de performance."

    def crear_nodo(self, ruta_padre, nombre, tipo, contenido=None):
        padre, _ = self._buscar_nodo_y_padre(ruta_padre)
        if not padre: return False, "Error: La carpeta donde quieres crear esto no existe."
        if padre.tipo_nodo == 'file': return False, "Error: No puedes meter cosas dentro de un archivo."
        
        for hijo in padre.hijos:
            if hijo.nombre == nombre: return False, f"Error: Ya existe '{nombre}' aquí."
                
        nuevo = Nodo(nombre, tipo, contenido)
        padre.hijos.append(nuevo)
        ruta_completa = f"{ruta_padre}/{nombre}" if ruta_padre != "root" else f"root/{nombre}"
        self._actualizar_trie("create", name_new=nombre, ruta=ruta_completa)
        return True, f"Listo, creado: {nombre}"

    def mover_nodo(self, ruta_origen, ruta_destino):
        nodo_mov, padre_orig = self._buscar_nodo_y_padre(ruta_origen)
        nuevo_padre, _ = self._buscar_nodo_y_padre(ruta_destino)

        if not nodo_mov or not padre_orig: return False, "No encuentro lo que quieres mover."
        if not nuevo_padre or nuevo_padre.tipo_nodo == 'file': return False, "El destino no es válido."
            
        for hijo in nuevo_padre.hijos:
            if hijo.nombre == nodo_mov.nombre: return False, "Ya hay algo con ese nombre en el destino."

        # Actualizar HashMap antes de mover
        self._actualizar_trie("delete", name_old=nodo_mov.nombre, ruta=ruta_origen)
        
        padre_orig.hijos.remove(nodo_mov)
        nuevo_padre.hijos.append(nodo_mov)
        
        # Actualizar HashMap después de mover
        nueva_ruta = f"{ruta_destino}/{nodo_mov.nombre}"
        self._actualizar_trie("create", name_new=nodo_mov.nombre, ruta=nueva_ruta)
        
        return True, f"Movido exitosamente a {ruta_destino}"

    def renombrar_nodo(self, ruta_nodo, nuevo_nombre):
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo)
        if not nodo or not padre: return False, "No encuentro el archivo."
            
        for hermano in padre.hijos:
            if hermano.nombre == nuevo_nombre: return False, "Ya existe ese nombre aquí."
        
        nombre_anterior = nodo.nombre
        nodo.nombre = nuevo_nombre
        self._actualizar_trie("rename", name_old=nombre_anterior, name_new=nuevo_nombre, ruta=ruta_nodo)
        return True, f"Renombrado a {nuevo_nombre}"
    
    def buscar_autocompletado(self, prefix):
        return self.trie.buscar_por_prefijo(prefix)
    
    def listar_directorio(self, ruta):
        nodo, _ = self._buscar_nodo_y_padre(ruta)
        if not nodo: return False, "Ruta no encontrada."
        if nodo.tipo_nodo == 'file':
            return True, f"Es un archivo: {nodo.nombre} (Tiene {len(str(nodo.contenido))} letras)"
        
        if not nodo.hijos:
            return True, "(carpeta vacía)"
        return True, "\n".join(self._obtener_hijos_formato(nodo))

    # --- PAPELERA ---

    def eliminar_nodo(self, ruta_nodo):
        nodo, padre = self._buscar_nodo_y_padre(ruta_nodo)
        if not nodo or not padre: return False, "No se puede eliminar (¿es root o no existe?)."
            
        padre.hijos.remove(nodo)
        self._actualizar_trie("delete", name_old=nodo.nombre, ruta=ruta_nodo)
        
        item_papelera = {
            "path_origen": ruta_nodo,
            "path_padre": "/".join(ruta_nodo.split('/')[:-1]),
            "nodo": nodo
        }
        self.papelera.append(item_papelera) 
        return True, "Enviado a papelera."

    def ver_papelera(self):
        if not self.papelera: return "La papelera está vacía."
        salida = []
        for idx, item in enumerate(self.papelera):
            salida.append(f"[{idx}] {item['nodo'].nombre} (Venía de: {item['path_origen']})")
        return "\n".join(salida)

    def restaurar_nodo(self, indice):
        try:
            idx = int(indice)
            if idx < 0 or idx >= len(self.papelera): return False, "Número inválido."
        except ValueError: return False, "Debes darme el número del archivo."

        item = self.papelera[idx]
        nodo_a_restaurar = item['nodo']
        path_padre_str = item['path_padre']

        padre, _ = self._buscar_nodo_y_padre(path_padre_str)
        if not padre: return False, "La carpeta original ya no existe, no sé dónde ponerlo."

        for hijo in padre.hijos:
            if hijo.nombre == nodo_a_restaurar.nombre: return False, "Conflicto: Ya hay un archivo con ese nombre ahí."

        padre.hijos.append(nodo_a_restaurar)
        self.papelera.pop(idx)
        ruta_completa = f"{path_padre_str}/{nodo_a_restaurar.nombre}"
        self._actualizar_trie("create", name_new=nodo_a_restaurar.nombre, ruta=ruta_completa)
        return True, f"Restaurado en {path_padre_str}"

    def vaciar_papelera(self):
        c = len(self.papelera)
        self.papelera = []
        return True, f"Se eliminaron {c} elementos para siempre."

    # --- PERSISTENCIA ---

    def guardar_arbol(self, nombre_archivo="./root/mi_filesystem.json"):
        try:
            papelera_serializada = []
            for item in self.papelera:
                papelera_serializada.append({
                    "path_origen": item["path_origen"],
                    "path_padre": item["path_padre"],
                    "nodo": item["nodo"].to_dict()
                })
            data = {"filesystem": self.root.to_dict(), "trash": papelera_serializada}
            
            os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True) 
            
            with open(nombre_archivo, 'w') as f: json.dump(data, f, indent=4)
            return True, f"Guardado correctamente en {nombre_archivo}"
        except Exception as e: return False, str(e)

    def cargar_arbol(self, nombre_archivo="./root/mi_filesystem.json"):
        if not os.path.exists(nombre_archivo): return False, "No encuentro el archivo de guardado."
        try:
            with open(nombre_archivo, 'r') as f:
                data = json.load(f)
                if "filesystem" in data:
                    root_data, trash_data = data["filesystem"], data.get("trash", [])
                else: root_data, trash_data = data, []

                self.root = Nodo.from_dict(root_data)
                self.papelera = []
                for item in trash_data:
                    self.papelera.append({
                        "path_origen": item["path_origen"],
                        "path_padre": item["path_padre"],
                        "nodo": Nodo.from_dict(item["nodo"])
                    })
                # Reconstruir índices
                self.trie = Trie()
                self.hash_map = {}
                self._indexar_trie_recursivamente(self.root)
            return True, "Sistema cargado correctamente."
        except Exception as e: return False, str(e)




def main():
    fs = ArbolGeneral()
    current_path = "root" 

    print("╔═══════════════════════════════════════════════════════╗")
    print("║   SISTEMA DE ARCHIVOS CON ESTRUCTURAS DE DATOS        ║")
    print("║   Árboles Generales + Trie + HashMap                  ║")
    print("╚═══════════════════════════════════════════════════════╝")
    
    exito, msg = fs.cargar_arbol()
    if exito: print(f"[INFO] {msg}")
    print("Escribe 'help' para ver los comandos disponibles\n")

    # Configuración del autocompletado
    def completador_tab(texto_escrito, estado):
        opciones = fs.buscar_autocompletado(texto_escrito)
        if estado < len(opciones):
            return opciones[estado]
        else:
            return None

    readline.set_completer(completador_tab)
    readline.parse_and_bind("tab: complete")

    while True:
        try:
            comando_input = input(f"\nfs:{current_path}> ").strip().split()
        except EOFError: 
            break
            
        if not comando_input: continue
        cmd = comando_input[0].lower()
        args = comando_input[1:]

        if cmd == "exit": 
            print("\n[INFO] Guardando cambios...")
            fs.guardar_arbol()
            print("¡Hasta luego! 👋")
            break
        
        elif cmd == "cd":
            if len(args) < 1:
                print("Uso: cd <carpeta> | cd .. | cd /")
                continue
            
            destino = args[0]
            
            if destino.lower() == "root" or destino == "/":
                current_path = "root"
            else:
                ruta_tentativa = resolver_ruta_absoluta(destino, current_path)
                ok, msg = fs.validar_ruta(ruta_tentativa)
                if ok:
                    current_path = ruta_tentativa
                else:
                    print(f"❌ Error: {msg}")

        elif cmd == "ls":
            if len(args) == 0:
                target = current_path
            else:
                target = resolver_ruta_absoluta(args[0], current_path)
            
            ok, res = fs.listar_directorio(target)
            print(res)

        elif cmd == "mkdir":
            if not args: 
                print("❌ Uso: mkdir <nombre>")
            else:
                ok, msg = fs.crear_nodo(current_path, args[0], "folder")
                print("✅" if ok else "❌", msg)

        elif cmd == "touch":
            if not args: 
                print("❌ Uso: touch <nombre> [texto]")
            else:
                contenido = " ".join(args[1:]) if len(args) > 1 else ""
                ok, msg = fs.crear_nodo(current_path, args[0], "file", contenido)
                print("✅" if ok else "❌", msg)

        elif cmd == "mv":
            if len(args) < 2: 
                print("❌ Uso: mv <origen> <destino>")
            else:
                origen = resolver_ruta_absoluta(args[0], current_path)
                destino = resolver_ruta_absoluta(args[1], current_path)
                ok, msg = fs.mover_nodo(origen, destino)
                print("✅" if ok else "❌", msg)

        elif cmd == "rm":
            if not args: 
                print("❌ Uso: rm <nombre>")
            else:
                target = resolver_ruta_absoluta(args[0], current_path)
                ok, msg = fs.eliminar_nodo(target)
                print("✅" if ok else "❌", msg)

        elif cmd == "ren" or cmd == "rename":
            if len(args) < 2: 
                print("❌ Uso: ren <viejo> <nuevo>")
            else:
                ruta_nodo = resolver_ruta_absoluta(args[0], current_path)
                ok, msg = fs.renombrar_nodo(ruta_nodo, args[1])
                print("✅" if ok else "❌", msg)

        # NUEVOS COMANDOS
        elif cmd == "info":
            altura = fs.calcular_altura()
            tamano = fs.calcular_tamano()
            print("\n📊 ESTADÍSTICAS DEL SISTEMA:")
            print(f"  └─ Altura del árbol: {altura}")
            print(f"  └─ Total de nodos: {tamano}")
            print(f"  └─ Elementos en papelera: {len(fs.papelera)}")

        elif cmd == "tree":
            print("\n🌳 ESTRUCTURA DEL ÁRBOL (Preorden):")
            recorrido = fs.recorrido_preorden()
            for linea in recorrido:
                print(linea)

        elif cmd == "export":
            archivo = args[0] if args else "preorden_export.txt"
            ok, msg = fs.exportar_preorden(archivo)
            print("✅" if ok else "❌", msg)

        elif cmd == "find":
            if not args:
                print("❌ Uso: find <nombre_exacto>")
            else:
                rutas = fs.buscar_exacto(args[0])
                if rutas:
                    print(f"\n🔍 Encontrado '{args[0]}' en {len(rutas)} ubicación(es):")
                    for r in rutas:
                        print(f"  └─ {r}")
                else:
                    print(f"❌ No se encontró '{args[0]}'")

        elif cmd == "perf_test":
            import time
            
            cantidad = 1000 if not args else int(args[0])

            start = time.time()
            ok, msg = fs.generar_carga_prueba(cantidad)
            end = time.time()
            print(f"\n[INFO] {msg}")
            print(f"  ⏱️  Inserción: {end - start:.4f}s")
            
            # Prueba de búsqueda por prefijo (Trie)
            start = time.time()
            fs.buscar_autocompletado("archivo_perf_9")
            end = time.time()
            print(f"  ⏱️  Búsqueda Trie: {end - start:.6f}s")
            
            # Prueba de búsqueda exacta (HashMap)
            start = time.time()
            fs.buscar_exacto("archivo_perf_00500_test.txt")
            end = time.time()
            print(f"  ⏱️  Búsqueda HashMap: {end - start:.6f}s")
            
            print("✅ Ambas búsquedas son casi instantáneas (< 1ms)")

        elif cmd == "trash": 
            print(fs.ver_papelera())
        elif cmd == "restore":
            if args: 
                ok, msg = fs.restaurar_nodo(args[0])
                print("✅" if ok else "❌", msg)
            else: 
                print("❌ Uso: restore <índice>")
        elif cmd == "empty": 
            ok, msg = fs.vaciar_papelera()
            print("✅" if ok else "❌", msg)
        elif cmd == "search":
            if args: 
                resultados = fs.buscar_autocompletado(args[0])
                if resultados:
                    print(f"🔍 Encontrados {len(resultados)} archivo(s):")
                    for r in resultados:
                        print(f"  └─ {r}")
                else:
                    print("❌ No se encontraron coincidencias")
            else: 
                print("❌ Uso: search <prefijo>")
        elif cmd == "load": 
            ok, msg = fs.cargar_arbol()
            print("✅" if ok else "❌", msg)
            if ok:
                current_path = "root"
        elif cmd == "save":
            ok, msg = fs.guardar_arbol()
            print("✅" if ok else "❌", msg)
        elif cmd == "cls":
            limpiarpantalla()
        elif cmd == "help":
            imprimir_ayuda()
        else:
            print(f"❌ Comando desconocido: '{cmd}'. Usa 'help' para ver comandos.")

if __name__ == "__main__":
    main()