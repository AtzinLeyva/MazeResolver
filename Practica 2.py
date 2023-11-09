import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque   
arbol_expansion = nx.DiGraph()
arbol_expansion_bfs = nx.DiGraph()
arbol_expansion_astar = nx.DiGraph()
import heapq
def heuristica(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)
def astar(start_x, start_y):
    pq = []
    heapq.heappush(pq, (0 + heuristica((start_x, start_y), (fin_x, fin_y)), 0, None, (start_x, start_y), [(start_x, start_y)]))
    visitados = set()
    costes_g = {(start_x, start_y): 0}
    arbol_expansion_astar.clear()
    arbol_expansion_astar.add_node((start_x, start_y))

    while pq:
        _, costo, padre, current, path = heapq.heappop(pq)
        if current in visitados:
            continue

        if padre:
            arbol_expansion_astar.add_edge(padre, current)

        if current == (fin_x, fin_y):
            return path, costo
        
        visitados.add(current)
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecino = (current[0] + dx, current[1] + dy)
            if 0 <= vecino[0] < len(m) and 0 <= vecino[1] < len(m[0]) and puede_pasar(jugador, m[vecino[0]][vecino[1]]):
                nuevo_costo = costo + obtener_costo(vecino[0], vecino[1])

                if vecino not in costes_g or nuevo_costo < costes_g[vecino]:
                    costes_g[vecino] = nuevo_costo
                    prioridad = nuevo_costo + heuristica(vecino, (fin_x, fin_y))
                    heapq.heappush(pq, (prioridad, nuevo_costo, current, vecino, path + [vecino]))

    return None, float('inf')  # Si no se encuentra camino
def graficar_arbol_astar():
    pos = nx.spring_layout(arbol_expansion_astar)  
    nx.draw(arbol_expansion_astar, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=15)
    plt.title("Árbol de Expansión A*")
    plt.show()
def ejecutar_astar():
    arbol_expansion_astar.clear()
    arbol_expansion_astar.add_node((jugador.x, jugador.y))
    path, total_cost = astar(jugador.x, jugador.y)

    if not path:
        messagebox.showinfo("Información", "No se encontró un camino con A*!")
        return

    for i, (x, y) in enumerate(path):
        # Marcar casillas adyacentes con una 'O' solo si no son parte del camino ya marcado con 'X'
        if i > 0:  # Saltar la primera posición ya que el jugador ya está allí
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                # Asegúrate de no sobrescribir el inicio, el fin, o el camino con 'O'
                if (0 <= nx < len(m) and 0 <= ny < len(m[0]) and 
                        botones[nx][ny]['text'] != 'X' and 
                        (nx, ny) != (jugador.x, jugador.y) and 
                        (nx, ny) != (fin_x, fin_y)):
                    botones[nx][ny].config(text='O')

        # Actualizar la posición del jugador con una 'X' y asegurarse de que quede marcada
        botones[x][y].config(bg='lightgreen', text='X')
        ventana.update()
        time.sleep(0.2)

    botones[jugador.x][jugador.y].config(bg='red')  # Marcar la posición inicial
    botones[fin_x][fin_y].config(bg='green')  # Marcar la posición final
    messagebox.showinfo("Costo total", f"El costo total del recorrido con A* es: {total_cost}")
    graficar_arbol_astar()


    arbol_expansion.clear()
    arbol_expansion.add_node((jugador.x, jugador.y))
    path, total_cost = astar(jugador.x, jugador.y)

    if not path:
        messagebox.showinfo("Información", "No se encontró un camino con A*!")
        return

    for (x, y) in path:
        botones[x][y].config(bg='lightblue')
        ventana.update()
        time.sleep(0.2)

    botones[jugador.x][jugador.y].config(bg='red')
    botones[fin_x][fin_y].config(bg='green')
    messagebox.showinfo("Costo total", f"El costo total del recorrido con A* es: {total_cost}")
    # Opcional: graficar el árbol si es necesario
def bfs(x, y):
    visitados_bfs = [[False for _ in range(len(m[0]))] for _ in range(len(m))]
    cola = deque([(x, y, [], 0, None)])  
    
    while cola:
        x, y, path, costo, padre = cola.popleft()

        if x < 0 or x >= len(m) or y < 0 or y >= len(m[0]) or visitados_bfs[x][y] or not puede_pasar(jugador, m[x][y]):
            continue

        path = path + [(x, y)]

        if padre:  
            arbol_expansion_bfs.add_edge(padre, (x, y))

        if (x, y) == (fin_x, fin_y):
            return path, costo  
        
        visitados_bfs[x][y] = True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_cost = costo + obtener_costo(x, y)
            cola.append((x + dx, y + dy, path, new_cost, (x, y)))

    return None, 0
def graficar_arbol_bfs():
    pos = nx.spring_layout(arbol_expansion_bfs)  
    nx.draw(arbol_expansion_bfs, pos, with_labels=True, node_size=500, node_color="lightgreen", font_size=15)
    plt.title("Árbol de Expansión BFS")
    plt.show()
def ejecutar_bfs():
    arbol_expansion_bfs.clear()
    arbol_expansion_bfs.add_node((jugador.x, jugador.y))
    path, total_cost = bfs(jugador.x, jugador.y)

    if not path:
        messagebox.showinfo("Información", "No se encontró un camino!")
        return

    for i, (x, y) in enumerate(path):
        # Marcar casillas adyacentes con una 'O' solo si no son parte del camino ya marcado con 'X'
        if i > 0:  # Saltar la primera posición ya que el jugador ya está allí
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                # Asegúrate de no sobrescribir el inicio, el fin, o el camino con 'O'
                if (0 <= nx < len(botones) and 0 <= ny < len(botones[0]) and
                        botones[nx][ny]['text'] != 'X' and 
                        (nx, ny) != (jugador.x, jugador.y) and 
                        (nx, ny) != (fin_x, fin_y)):
                    botones[nx][ny].config(text='O')

        # Actualizar la posición del jugador con una 'X' y asegurarse de que quede marcada
        botones[x][y].config(bg='lightgreen', text='X')
        ventana.update()
        time.sleep(0.2)

    # Marcar la posición final
    botones[fin_x][fin_y].config(bg='green', text='X')

    messagebox.showinfo("Costo total", f"El costo total del recorrido es: {total_cost}")
    graficar_arbol_bfs()
def puede_pasar(jugador, valor_casilla):
    restricciones = {
        'Humano': ['0'],
        'Mono': ['0', '6'],
        'Pulpo': ['0', '3', '6'],
        'Pie Grande': ['2', '3']
    }
    return valor_casilla not in restricciones[jugador.tipo]
def dfs(x, y, path, costo=0, padre=None):
    if x < 0 or x >= len(m) or y < 0 or y >= len(m[0]) or visitados[x][y] or not puede_pasar(jugador, m[x][y]):
        return None, 0
    if padre:  
        arbol_expansion.add_edge(padre, (x, y))
    if (x, y) == (fin_x, fin_y):
        return path + [(x, y)], costo + obtener_costo(x, y)  
    visitados[x][y] = True
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_path, next_cost = dfs(x+dx, y+dy, path + [(x, y)], costo + obtener_costo(x, y), padre=(x, y)) 
        if next_path:
            return next_path, next_cost       
    return None, 0
def obtener_costo(x, y):
    valor_casilla = m[x][y]
    if jugador.tipo == 'Humano':
        costos = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
    elif jugador.tipo == 'Mono':
        costos = {'0': 0, '1': 2, '2': 4, '3': 3, '4': 1, '5': 5, '6': 0}
    elif jugador.tipo == 'Pulpo':
        costos = {'0': 0, '1': 2, '2': 1, '3': 0, '4': 3, '5': 2, '6': 0}
    elif jugador.tipo == 'Pie Grande':
        costos = {'0': 15, '1': 4, '2': 0, '3': 0, '4': 4, '5': 5, '6': 3}
    else:
        return 0
    return costos[valor_casilla]
def graficar_arbol():
    pos = nx.spring_layout(arbol_expansion) 
    nx.draw(arbol_expansion, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=15)
    plt.title("Árbol de Expansión DFS")
    plt.show()
def ejecutar_dfs():
    global visitados
    visitados = [[False for _ in range(len(m[0]))] for _ in range(len(m))]
    arbol_expansion.add_node((jugador.x, jugador.y))
    path, total_cost = dfs(jugador.x, jugador.y, [])

    if not path:
        messagebox.showinfo("Información", "No se encontró un camino!")
        return

    for (x, y) in path:
        botones[x][y].config(text='X', bg='green')  # Marcar con 'X' y color verde la ruta del jugador
        ventana.update()
        time.sleep(0.2)

        # Marcar las casillas adyacentes con 'O' si no están en el camino y no han sido visitadas
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Direcciones adyacentes
            nx, ny = x + dx, y + dy
            # Comprobar que estamos dentro de los límites y que la casilla no es parte del camino
            if 0 <= nx < len(m) and 0 <= ny < len(m[0]) and (nx, ny) not in path and not visitados[nx][ny]:
                botones[nx][ny].config(text='O')  # Solo marcar la casilla actual, sin actualizar visitados
    # Resto del código que actualiza el estado final de los botones y muestra el costo
    botones[jugador.x][jugador.y].config(bg='red')
    botones[fin_x][fin_y].config(bg='green')
    messagebox.showinfo("Costo total", f"El costo total del recorrido es: {total_cost}")
    graficar_arbol()
class Jugador:
    def __init__(self, x=0, y=0, tipo='Humano'):
        self.x = x
        self.y = y
        self.tipo = tipo
def seleccionar_personaje():
    global jugador
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Seleccionar Personaje")
    tk.Label(dialogo, text="Elige un personaje:").pack(pady=10)

    combobox = ttk.Combobox(dialogo, values=["Humano", "Mono", "Pulpo", "Pie Grande"], state="readonly")
    combobox.pack(pady=10, padx=10)
    combobox.set("Humano")

    def confirmar_seleccion():
        global jugador
        jugador.tipo = combobox.get()  # Asignamos el tipo al objeto jugador
        print(f"Tipo de jugador seleccionado: {jugador.tipo}")  # Añadir esta línea
        dialogo.destroy()

    btn_confirmar = tk.Button(dialogo, text="Confirmar", command=confirmar_seleccion)
    btn_confirmar.pack(pady=10)
    ventana.wait_window(dialogo)
personaje_seleccionado = ""
costos_movimiento = {
    'Humano': {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6},
    'Mono': {'0': 0, '1': 2, '2': 4, '3': 3, '4': 1, '5': 5, '6': 0},
    'Pulpo': {'0': 0, '1': 2, '2': 1, '3': 0, '4': 3, '5': 2, '6': 0},
    'Pie Grande': {'0': 15, '1': 4, '2': 0, '3': 0, '4': 4, '5': 5, '6': 3}
}
def definir_costos_movimiento():
    global jugador
    return costos_movimiento.get(jugador.tipo, {})  # Obtener los costos para el tipo de jugador actual
def mostrar_info(x, y):
    tipo_terreno = {
        '0': "Montaña",
        '1': "Pradera",
        '2': "Agua",
        '3': "Arena",
        '4': "Bosque",
        '5': "Pantano",
        '6': "Nieve"
    }.get(m[x][y], "Desconocido")
    valor = m[x][y]
    estado_jugador = "El jugador ha pasado por aquí" if visitados[x][y] else "El jugador no ha pasado por aquí"
    
    respuesta = messagebox.askyesnocancel("Información", f"Estado: {estado_jugador}\n\nCoordenadas: ({x}, {y})\n\nTipo de terreno: {tipo_terreno}\n\n¿Deseas modificar esta casilla?")

    if respuesta == True:
        nuevo_valor = simpledialog.askstring("Modificar Casilla", "Ingresa el nuevo valor (0-6):")
        if nuevo_valor in ['0', '1', '2', '3', '4', '5', '6']:
            m[x][y] = nuevo_valor
            botones[x][y].config(bg=colores[nuevo_valor], text=nuevo_valor)
def actualizar_colores_casillas():
    for i in range(len(m)):
        for j in range(len(m[i])):
            if (i == jugador.x and (j == jugador.y - 1 or j == jugador.y + 1)) or (j == jugador.y and (i == jugador.x - 1 or i == jugador.x + 1)):
                if botones[i][j]["text"] != "X":
                    botones[i][j].config(bg=colores[m[i][j]], text="O")
            elif visitados[i][j] and botones[i][j]["text"] != "X":
                botones[i][j].config(text="X" if botones[i][j]["text"] != "I" and botones[i][j]["text"] != "F" else botones[i][j]["text"])
            
    # Llama a pintar_casillas para actualizar los colores de las casillas con "O" y "X"
    pintar_casillas()
def marcar_terreno(x, y):
    if 0 <= x < len(m) and 0 <= y < len(m[0]):
        if visitados[x][y]:
            botones[x][y].config(text='X', bg=colores[m[x][y]])
        else:
            botones[x][y].config(text='O', bg=colores[m[x][y]])
def pintar_casillas():
    for i in range(len(m)):
        for j in range(len(m[i])):
            if botones[i][j]["text"] == "O" and (i != inicio_x or j != inicio_y) and (i != fin_x or j != fin_y):
                costo = costos_movimiento.get(jugador.tipo, {}).get(m[i][j], "N/A")
                botones[i][j].config(bg=colores[m[i][j]], text=f"O, {costo}")
            elif botones[i][j]["text"] == "X" and (i != inicio_x or j != inicio_y) and (i != fin_x or j != fin_y):
                costo = costos_movimiento.get(jugador.tipo, {}).get(m[i][j], "N/A")
                botones[i][j].config(bg=colores[m[i][j]], text=f"X, {costo}")

    # Conservar el color original y el texto de las casillas de inicio y final
    botones[inicio_x][inicio_y].config(bg=colores[m[inicio_x][inicio_y]], text="I")
    botones[fin_x][fin_y].config(bg=colores[m[fin_x][fin_y]], text="F")
def actualizar_contador():
    mensaje_contador.config(text=f"El número que llevas es: {contador.get()}")

def mover_jugador(x, y):
    global jugador
    if 0 <= x < len(m) and 0 <= y < len(m[0]):
        valor_casilla = int(m[x][y])
        costos = definir_costos_movimiento()
        # Verificar si el jugador es un humano y la casilla es una montaña
        if jugador.tipo == 'Humano' and valor_casilla == 0:  
            return 
        if jugador.tipo == 'Mono' and valor_casilla == 0:  
            return  
        if jugador.tipo == 'Mono' and valor_casilla == 6:  
            return  
        if jugador.tipo == 'Pulpo' and valor_casilla == 0:  
            return
        if jugador.tipo == 'Pulpo' and valor_casilla == 3:  
            return
        if jugador.tipo == 'Pulpo' and valor_casilla == 6:  
            return        
        if jugador.tipo == 'Pie Grande' and valor_casilla == 3:  
            return  
        if jugador.tipo == 'Pie Grande' and valor_casilla == 4:  
            return  
        costo_movimiento = costos.get(str(valor_casilla), 0)
        contador.set(contador.get() + costo_movimiento)
        boton_anterior = botones[jugador.x][jugador.y]
        boton_anterior.config(bg=colores[m[jugador.x][jugador.y]])
        jugador.x, jugador.y = x, y
        actualizar_colores_casillas()
        botones[jugador.x][jugador.y].config(bg='red', text="O")
        visitados[jugador.x][jugador.y] = True
        jugador.x, jugador.y = x, y
        actualizar_colores_casillas()
        botones[jugador.x][jugador.y].config(bg='red', text="X")
        actualizar_contador()
        # Actualizar los botones alrededor de la nueva posición del jugador
        marcar_terreno(jugador.x, jugador.y - 1)  # Izquierda
        marcar_terreno(jugador.x, jugador.y + 1)  # Derecha
        marcar_terreno(jugador.x - 1, jugador.y)  # Arriba
        marcar_terreno(jugador.x + 1, jugador.y)  # Abajo
        # Mover al jugador a la nueva posición y actualizar el botón del jugador
        jugador.x, jugador.y = x, y
        botones[jugador.x][jugador.y].config(text=m[jugador.x][jugador.y], bg='red')
        visitados[jugador.x][jugador.y] = True
        actualizar_contador()
        if (jugador.x, jugador.y) == (fin_x, fin_y):
            messagebox.showinfo("Victoria", f"Has llegado al final!\n\nPuntuación: {contador.get()}")
def manejar_teclas(event):
    if event.keysym == 'Up':
        mover_jugador(jugador.x - 1, jugador.y)
    elif event.keysym == 'Down':
        mover_jugador(jugador.x + 1, jugador.y)
    elif event.keysym == 'Left':
        mover_jugador(jugador.x, jugador.y - 1)
    elif event.keysym == 'Right':
        mover_jugador(jugador.x, jugador.y + 1)
# Leer el archivo y preparar el mapa
with open("prueba.txt", "r") as archivo:
    contenido = archivo.read()
filas = contenido.split('\n')
m = [list(fila.strip()) for fila in filas if fila.strip()]
visitados = [[False for _ in range(len(m[0]))] for _ in range(len(m))]

colores = {
    '0': "#D2691E",  # Montaña
    '1': "#B8860B",  # Pradera
    '2': "#00BFFF",  # Agua
    '3': "#F0E68C",  # Arena
    '4': "#3CB371",  # Bosque
    '5': "#800080",  # Pantano (morado)
    '6': "#FFFFFF"   # Nieve (blanco)
}
ventana = tk.Tk()
ventana.title("Botones de caracteres")
ventana.bind('<Key>', manejar_teclas)
ventana.focus_set()
jugador = Jugador()
seleccionar_personaje()
ventana_contador = tk.Toplevel(ventana)
ventana_contador.title("Contador")
mensaje_contador = tk.Label(ventana_contador, text="")
mensaje_contador.pack(pady=20, padx=20)
inicio_x = simpledialog.askinteger("Inicio", "Coordenada X de inicio:", minvalue=0, maxvalue=len(m)-1)
inicio_y = simpledialog.askinteger("Inicio", "Coordenada Y de inicio:", minvalue=0, maxvalue=len(m[0])-1)
jugador.x = inicio_x
jugador.y = inicio_y
fin_x = simpledialog.askinteger("Final", "Coordenada X final:", minvalue=0, maxvalue=len(m)-1)
fin_y = simpledialog.askinteger("Final", "Coordenada Y final:", minvalue=0, maxvalue=len(m[0])-1)
visitados[jugador.x][jugador.y] = True
contador = tk.IntVar(value=int(m[inicio_x][inicio_y]))
actualizar_contador()
def limpiar_casillas():
    global visitados  # Asegúrate de usar la variable global
    for i in range(len(m)):
        for j in range(len(m[i])):
            if (i, j) == (inicio_x, inicio_y):
                botones[i][j].config(text='I', bg=colores[m[i][j]])  # Restablecer inicio
            elif (i, j) == (fin_x, fin_y):
                botones[i][j].config(text='F', bg=colores[m[i][j]])  # Restablecer final
            else:
                botones[i][j].config(text='', bg="#D3D3D3")  # Limpiar casilla
    # Restablecer los visitados, manteniendo el inicio como visitado si es necesario
    visitados = [[False for _ in range(len(m[0]))] for _ in range(len(m))]
    visitados[inicio_x][inicio_y] = True  # El inicio ya está visitado
botones = []
for i in range(len(m)):
    fila_botones = []
    for j in range(len(m[i])):
        # Elimina la asignación de "texto = char" y solo usa "texto" para marcar inicio y final
        if (i, j) == (inicio_x, inicio_y):
            texto = "I"
        elif (i, j) == (fin_x, fin_y):
            texto = "F"
        else:
            texto = ""  # Esta línea asegura que las casillas normales no tengan texto

        boton = tk.Button(ventana, text=texto, bg="#D3D3D3", command=lambda x=i, y=j: mostrar_info(x, y))
        boton.grid(row=i, column=j, padx=5, pady=5)
        fila_botones.append(boton)
    botones.append(fila_botones)
    btn_resolver = tk.Button(ventana, text="Resolver por Profundidad", command=ejecutar_dfs)
    btn_resolver.grid(row=len(m), column=0, columnspan=len(m[0]), pady=10)
    btn_bfs = tk.Button(ventana, text="Resolver por Amplitud", command=ejecutar_bfs)
    btn_bfs.grid(row=len(m), column=10, columnspan=len(m[0]), pady=10)
    btn_astar = tk.Button(ventana, text="Resolver A*", command=ejecutar_astar)
    btn_astar.grid(row=len(m)+1, column=0, columnspan=len(m[0]), pady=10)
# Configuración de la ventana
ventana.title("Mi Aplicación")  # Poner título a la ventana
ventana.geometry("800x600")     # Configurar tamaño de la ventana
# Configurar el color de fondo a beige
ventana.configure(bg='beige')
btn_limpiar = tk.Button(ventana, text="Limpiar Casillas", command=limpiar_casillas)
btn_limpiar.grid(row=len(m)+2, column=0, columnspan=len(m[0]), pady=10)
# Ahora que todos los botones están creados, actualizamos sus colores.
actualizar_colores_casillas()
ventana.mainloop()
