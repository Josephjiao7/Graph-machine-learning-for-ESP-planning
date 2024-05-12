import pandas as pd
import networkx as nx

def calculate_node_connectivity(G):
    node_connectivity = {}
    for node in G.nodes():
        connectivity = 0
        visited = set()
        queue = [node]
        while queue:
            current_node = queue.pop(0)
            if current_node not in visited:
                visited.add(current_node)
                neighbors = G.neighbors(current_node)
                queue.extend(neighbors)
                connectivity += 1
        node_connectivity[node] = connectivity - 1  # Subtract the node itself
    return node_connectivity

# Read the dataset
df = pd.read_csv('ESP.csv')

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for _, row in df.iterrows():
    id1 = row['origin']
    id2 = row['target']
    attribute = row['CW_Dist']

    G.add_edge(id1, id2, attribute=attribute)

# Calculate node connectivity
node_connectivity = calculate_node_connectivity(G)

# Print the connectivity of each node
for node, connectivity in node_connectivity.items():
    print(f"Node {node} has connectivity {connectivity}")

# Output the results to a CSV file
degree_centrality_data = [(node, centrality) for node, centrality in node_connectivity.items()]
degree_centrality_df = pd.DataFrame(degree_centrality_data, columns=['id', 'node_connectivity'])
degree_centrality_df.to_csv('node_connectivity.csv', index=False)
