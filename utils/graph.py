import matplotlib.pyplot as plt
import networkx as nx


class GraphViz:
    def __init__(self):
        self._G = None

    def get_graph(self):
        return self._G

    def draw(self, filename, connection_threshold=10.0, edge_labels=False):
        with open(filename, 'r') as f:
            lines = f.readlines()

        G = nx.Graph()

        edges_w = []
        for x in lines:
            a, b, w = x.split("\t")

            a = a.split("_")[0]
            b = b.split("_")[0]
            w = int(w.split(".")[0])

            if w >= connection_threshold and not G.has_edge(a, b):
                edges_w.append(w)
                G.add_edge(a, b, weight=w)
            else:
                G.add_node(a)
                G.add_node(b)

        if self._G is None:
            self._G = G

        print(G)

        if True:
            pos = nx.circular_layout(G)  # positions for all nodes - seed for reproducibility

            # nodes
            nx.draw_networkx_nodes(G, pos, node_size=150)

            # edges
            nx.draw_networkx_edges(G, pos, width=2, edge_color=edges_w, edge_cmap=plt.cm.Blues)
            # nx.draw_networkx_edges(
            #     G, pos, width=6, alpha=0.5, edge_color="b", style="dashed"
            # )

            # node labels
            nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
            # edge weight labels
            if edge_labels:
                edge_labels = nx.get_edge_attributes(G, "weight")
                nx.draw_networkx_edge_labels(G, pos, edge_labels)

            ax = plt.gca()
            ax.margins(0.08)
            plt.axis("off")
            plt.tight_layout()

            base_name = filename.split("/")[-1]
            plt.savefig(f"seasons_img/{'_'.join(base_name.split('_')[:3])}.png")
            plt.clf()
