import sys 
import networkx as nx
import matplotlib.pyplot as plt

# Número de distritos
V = 6  

def select_min_vertex(value, set_mst):
    minimum = sys.maxsize
    vertex = -1
    for i in range(V):
        if not set_mst[i] and value[i] < minimum:
            vertex = i
            minimum = value[i]
    return vertex

def find_mst(graph, district_names):
    parent = [-1] * V  # Almacena el MST
    value = [sys.maxsize] * V  # Para la relajación de los bordes
    set_mst = [False] * V  # True -> Vértice incluido en el MST
    
    value[0] = 0  # Nodo inicial
    
    for _ in range(V - 1):
        u = select_min_vertex(value, set_mst)
        set_mst[u] = True
        
        for j in range(V):
            if graph[u][j] != 0 and not set_mst[j] and graph[u][j] < value[j]:
                value[j] = graph[u][j]
                parent[j] = u
    
    edges = []
    total_cost = 0
    print("\nConexión óptima para la instalación de fibra óptica:")
    for i in range(1, V):
        print(f"{district_names[parent[i]]} <-> {district_names[i]}  (Costo: {graph[parent[i]][i]})")
        edges.append((parent[i], i, graph[parent[i]][i]))
        total_cost += graph[parent[i]][i]
    
    print(f"Costo total mínimo: {total_cost}\n")
    plot_graph(graph, edges, district_names)

def plot_graph(graph, mst_edges, district_names):
    G = nx.Graph()
    
    for i in range(V):
        for j in range(i + 1, V):
            if graph[i][j] != 0:
                G.add_edge(district_names[i], district_names[j], weight=graph[i][j])
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
    
    mst = nx.Graph()
    for edge in mst_edges:
        mst.add_edge(district_names[edge[0]], district_names[edge[1]], weight=edge[2])
    nx.draw_networkx_edges(G, pos, edgelist=mst.edges(), edge_color='red', width=2)
    
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.title("Red Óptima de Fibra Óptica")
    plt.show()

def main():
    district_names = ["Centro", "Norte", "Sur", "Este", "Oeste", "Suburbios"]
    graph = [
        [0, 10, 20, 0, 0, 0],
        [10, 0, 25, 16, 18, 0],
        [20, 25, 0, 8, 30, 0],
        [0, 16, 8, 0, 12, 14],
        [0, 18, 30, 12, 0, 22],
        [0, 0, 0, 14, 22, 0]
    ]
    
    find_mst(graph, district_names)
    
if __name__ == "__main__":
    main()
