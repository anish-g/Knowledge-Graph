import networkx as nx
import matplotlib.pyplot as plt

graph_filename = "knowledge_graph.graphml"

G = nx.read_graphml(graph_filename)
print("GraphML file loaded")


print("Drawing Knowledge Graph image...")
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color="skyblue",
        edge_cmap=plt.cm.Blues, pos=pos)
plt.show()


question = "Who filed a petition late on Tuesday?"

