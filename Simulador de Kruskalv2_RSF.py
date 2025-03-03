import matplotlib.pyplot as plt  # Biblioteca para graficar.
import networkx as nx  # Biblioteca para trabajar con grafos.

# Clase Union-Find (Disjoint Set Union) para gestionar conjuntos disjuntos.
class UnionFind:
    def __init__(self, n):
        # Inicializa cada nodo como su propio padre y los rangos en 0.
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        # Encuentra la raíz del conjunto al que pertenece u (con compresión de caminos).
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        # Une los conjuntos de u y v según el rango.
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

# Algoritmo de Kruskal para construir un árbol de expansión mínimo o máximo.
def kruskal_simulator(graph_edges, num_nodes, max_tree=False):
    # Ordena las aristas por peso (ascendente para mínimo, descendente para máximo).
    graph_edges = sorted(graph_edges, key=lambda x: x[2], reverse=max_tree)
    uf = UnionFind(num_nodes)  # Inicializa Union-Find.
    mst_edges = []  # Lista para almacenar las aristas del árbol.
    total_cost = 0  # Costo total del árbol.

    print(f"\nConstrucción del Árbol de {'Máximo' if max_tree else 'Mínimo'} Costo usando Kruskal:")

    # Recorre las aristas ordenadas.
    for u, v, weight in graph_edges:
        # Si los nodos no están en el mismo conjunto, añade la arista al árbol.
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append((u, v, weight))
            total_cost += weight
            print(f"Añadiendo arista ({u}, {v}) con peso {weight}")

            # Detén el proceso si ya se tienen n-1 aristas.
            if len(mst_edges) == num_nodes - 1:
                break

    print(f"\nCosto total del Árbol de {'Máximo' if max_tree else 'Mínimo'} Costo: {total_cost}")
    return mst_edges, total_cost  # Retorna las aristas del árbol y su costo.

# Función para graficar el árbol de expansión.
def draw_graph(edges, num_nodes, title):
    G = nx.Graph()  # Crea un grafo vacío.
    G.add_nodes_from(range(num_nodes))  # Añade los nodos.
    G.add_weighted_edges_from(edges)  # Añade las aristas con sus pesos.

    pos = nx.spring_layout(G)  # Calcula la posición de los nodos para el dibujo.
    plt.figure(figsize=(8, 6))  # Define el tamaño de la figura.
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)  # Dibuja el grafo.
    edge_labels = {(u, v): f"{w}" for u, v, w in edges}  # Crea etiquetas para las aristas.
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")  # Dibuja las etiquetas.

    plt.title(title)  # Establece el título del gráfico.
    plt.show()  # Muestra el gráfico en pantalla.

# Datos de entrada: conexiones entre oficinas y sus costos.
edges = [
    (0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
    (2, 3, 4), (3, 4, 2), (4, 5, 6), (3, 5, 3)
]  # Lista de aristas (oficina1, oficina2, costo).
num_nodes = 6  # Número total de oficinas.

# Árbol de Mínimo Costo
print("=== Árbol de Mínimo Costo ===")
mst_min_edges, min_cost = kruskal_simulator(edges, num_nodes, max_tree=False)
draw_graph(mst_min_edges, num_nodes, "Árbol de Mínimo Costo - Conexión de Oficinas")

# Árbol de Máximo Costo
print("\n=== Árbol de Máximo Costo ===")
mst_max_edges, max_cost = kruskal_simulator(edges, num_nodes, max_tree=True)
draw_graph(mst_max_edges, num_nodes, "Árbol de Máximo Costo - Conexión de Oficinas")