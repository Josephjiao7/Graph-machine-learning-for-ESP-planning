import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
# %matplotlib inline

def diffusion_centrality(G, iterations=500):
    diffusion_centralities = {}
    for node in G.nodes():
        active_nodes = set([node])
        for _ in range(iterations):
            new_active_nodes = set()
            for n in active_nodes:
                neighbors = list(G.neighbors(n))
                new_active_nodes.update(neighbors)
            active_nodes.update(new_active_nodes)
            active_nodes.difference_update(diffusion_centralities.keys())  # Update the active node set, excluding nodes already computed
        diffusion_centralities[node] = len(active_nodes)
    return diffusion_centralities

# Read CSV file
df = pd.read_csv('ESP.csv')

# Create an undirected graph
G = nx.Graph()

# Create graph from connectivity table
for idx, row in df.iterrows():
    G.add_edges_from([(row['origin'], row['target'])], line=row['Link_ID'], cost=row['CW_Dist'])

print('Number of nodes')
print(len(G.nodes))

print('Number of edges')
print(len(G.edges))

# Calculate diffusion centrality
diffusion_centralities = diffusion_centrality(G)

# Print the diffusion centrality of each node
for idx, row in df.iterrows():
    node = row['origin']
    centrality = diffusion_centralities[node]
    print(f"Node {node} has diffusion centrality of {centrality}")

# Output the results to a CSV file
degree_centrality_data = [(node, centrality) for node, centrality in diffusion_centralities.items()]
degree_centrality_df = pd.DataFrame(degree_centrality_data, columns=['id', 'diffusion_centralities'])
degree_centrality_df.to_csv('diffusion_centralities.csv', index=False)
