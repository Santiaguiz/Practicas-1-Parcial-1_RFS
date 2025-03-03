import sys
import matplotlib.pyplot as plt
import networkx as nx

# Número de estaciones (nodos)
V = 6  

# Nombres de las estaciones
estaciones = ["Terminal", "Centro", "Universidad", "Hospital", "Aeropuerto", "Estación Norte"]

def select_min_vertex(value, processed):
    minimum = sys.maxsize
    vertex = -1
    for i in range(V):
        if not processed[i] and value[i] < minimum:
            vertex = i
            minimum = value[i]
    return vertex

def dijkstra(graph, inicio, destino):
    parent = [-1] * V  # Estructura del camino más corto
    value = [sys.maxsize] * V  # Inicialización de distancias
    processed = [False] * V  # Estado de los nodos procesados

    # Nodo inicial
    value[inicio] = 0  # La distancia a la estación inicial es 0

    for _ in range(V - 1):
        u = select_min_vertex(value, processed)
        processed[u] = True

        for j in range(V):
            if graph[u][j] != 0 and not processed[j] and value[u] != sys.maxsize and (value[u] + graph[u][j] < value[j]):
                value[j] = value[u] + graph[u][j]
                parent[j] = u

    # Construcción del camino más corto
    camino = []
    temp = destino
    while temp != -1:
        camino.append(temp)
        temp = parent[temp]
    camino.reverse()

    print("Ruta más corta desde", estaciones[inicio], "hasta", estaciones[destino], ":")
    print(" -> ".join(estaciones[i] for i in camino), f"(Tiempo total: {value[destino]} minutos)")

    # Dibujar la red de transporte
    plot_graph(graph, camino)

def plot_graph(graph, camino):
    G = nx.Graph()
    for i in range(V):
        G.add_node(i, label=estaciones[i])
    
    for i in range(V):
        for j in range(V):
            if graph[i][j] != 0:
                G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=1000, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f"{graph[i][j]} min" for i in range(V) for j in range(V) if graph[i][j] != 0})
    
    edges_resaltados = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges_resaltados, edge_color='red', width=2)
    
    plt.title("Red de Transporte Público - Camino más corto")
    plt.show()

# Matriz de adyacencia con tiempos de viaje (en minutos)
graph = [
    [0, 10, 0, 0, 30, 0],
    [10, 0, 15, 0, 0, 25],
    [0, 15, 0, 20, 0, 0],
    [0, 0, 20, 0, 10, 0],
    [30, 0, 0, 10, 0, 5],
    [0, 25, 0, 0, 5, 0]
]

# Estación de inicio y destino
inicio = 0  # Terminal
destino = 3  # Hospital

dijkstra(graph, inicio, destino)
