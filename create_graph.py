import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

from reduce_tags import TagReducer
from url_processor import UrlProcessor

# Subset the DataFrame to the first 10 lines
# df = pd.read_csv("data/pornhub.csv")
# df_subset = df.head(100)
# # Save the subset to a file
# df_subset.to_csv("data/pornhub-10.csv", index=False)

# reduce tags to popular tags only
tag_reducer = TagReducer("data/pornhub-10.csv")
tag_reducer.reduce_to_popular_tags(quantile=0.90)
df = tag_reducer.df

# replace url with hash
processor = UrlProcessor()
processor.add_id_column(df, "url")

# df.id
# df.popular_tags

B = nx.Graph()

# Add nodes with the 'url' column values as node attributes
B.add_nodes_from(df["id"], bipartite=0)

# Add nodes with the 'tags' column values as node attributes
for tags in df["popular_tags"]:
    B.add_nodes_from(tags, bipartite=1)

# Add edges between URLs and corresponding tags
for id, tags in zip(df["id"], df["popular_tags"]):
    B.add_edges_from([(id, tag) for tag in tags])


# # Check if the graph is bipartite
# is_bipartite = nx.is_bipartite(B)
# print("Is the graph bipartite?", is_bipartite)
# nx.is_connected(B)
# bottom_nodes, top_nodes = bipartite.sets(B)

# Analyze the bipartite graph
# # Get the sets of nodes of each bipartite partition
top_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
bottom_nodes = set(B) - top_nodes
print(round(bipartite.density(B, bottom_nodes), 2))

print("URL nodes:", top_nodes)
print("Tag nodes:", bottom_nodes)

# Visualise the bipartite graph
plt.figure(figsize=(10, 10))
pos = nx.bipartite_layout(B, df["id"])
nx.draw(
    B, pos, with_labels=True, node_color="r", edge_color="g", node_size=900, font_size=8
)
plt.title("Bipartite Network of URLs and Tags")
plt.show()
