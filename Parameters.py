import pickle
import pandas as pd
import network2 as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Settings
plt.rcParams['font.family'] = 'Times New Roman'

def draw(G, pos, measures, measure_name):
    plt.figure(figsize=(20, 20))
    node_size = [v * 2000 for v in measures.values()]  # Calculate node size based on values
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, cmap=plt.cm.RdBu_r,
                                   node_color=list(measures.values()), nodelist=measures.keys())

    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    edges = nx.draw_networkx_edges(G, pos)
    labels = nx.draw_networkx_labels(G, pos, font_family="Times New Roman", font_size=12, font_color='black')

    # Add a legend
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu_r)
    sm.set_array(list(measures.values()))
    plt.colorbar(sm, label=measure_name, shrink=0.2)

    plt.title(measure_name, fontsize=30)
    plt.axis('off')
    plt.show()

# Read CSV file
df = pd.read_csv('PageRank.csv')

# Create an undirected graph
G = nx.Graph()

# Add nodes and edges
for idx, row in df.iterrows():
    origin = int(row['origin'])
    target = int(row['target'])
    pr = row['pr']
    G.add_node(origin, pr=pr)
    G.add_node(target, pr=pr)
    G.add_edge(origin, target)

# Perform node layout using spring_layout
pos = nx.spring_layout(G)

# Retrieve node PageRank values
page_rank_values = nx.get_node_attributes(G, 'pr')

# Draw the graph
draw(G, pos, page_rank_values, 'PageRank')

# Save parameter file
with open('parameters.pkl', 'wb') as f:
    parameters = {
        'graph': G,
        'node_positions': pos
    }
    pickle.dump(parameters, f)
