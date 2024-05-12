import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
# %matplotlib inline

def calculate_threat_centrality(G):
    threat_centrality = {}
    for node in G.nodes():
        shortest_paths = nx.shortest_path_length(G, source=node)
        threat_score = sum(shortest_paths.values())
        threat_centrality[node] = threat_score
    return threat_centrality

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

# Calculate threat centrality
threat_centrality = calculate_threat_centrality(G)
# Print the threat centrality of each node
# Uncomment to print each node's centrality
# for node, score in threat_centrality.items():
#     print(f"Node {node} has a threat centrality of {score}")

# Output results to a CSV file
degree_centrality_data = [(node, threat_centrality) for node, threat_centrality in threat_centrality.items()]
degree_centrality_df = pd.DataFrame(degree_centrality_data, columns=['id', 'threat_centrality'])
degree_centrality_df.to_csv('threat centrality.csv', index=False)
