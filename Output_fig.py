import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pickle
import numpy as np

# Settings
plt.rcParams['font.family'] = 'Times New Roman'

def draw(G, pos, measures, measure_name):
    plt.figure(figsize=(12, 9))
    # Calculate node size based on values; adjust size according to the actual situation
    node_size = [v * 6 for v in measures.values()]  # threat centrality

    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, cmap=plt.cm.rainbow,
                                   node_color=list(measures.values()), nodelist=measures.keys())

    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    edges = nx.draw_networkx_edges(G, pos)
    labels = nx.draw_networkx_labels(G, pos, font_family="Times New Roman", font_size=12, font_color='black')

    # Add a legend
    sm = plt.cm.ScalarMappable(cmap=plt.cm.rainbow)
    sm.set_array(list(measures.values()))
    plt.colorbar(sm, label='value', shrink=0.5)

    plt.title(measure_name, fontsize=18)
    plt.axis('off')
    plt.savefig('test.png', dpi=400)  # Output location and resolution
    plt.show()

# Read CSV file
df = pd.read_csv('test.csv')

# Create an undirected graph
G = nx.Graph()

# Add nodes and edges
for idx, row in df.iterrows():
    origin = int(row['origin'])
    target = int(row['target'])
    pr = row['tc']  # Choose which result to plot
    G.add_node(origin, pr=pr)
    G.add_node(target, pr=pr)
    G.add_edge(origin, target)

# Read node positions from the parameter file
with open('parameters.pkl', 'rb') as f:
    parameters = pickle.load(f)
node_positions = parameters['node_positions']

# Retrieve node values
page_rank_values = nx.get_node_attributes(G, 'pr')

# Draw the graph
draw(G, node_positions, page_rank_values, 'Pagerank')
