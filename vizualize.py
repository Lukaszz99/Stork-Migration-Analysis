from utils.graph import GraphViz


if __name__ == "__main__":
    gv = GraphViz()
    gv.draw("pl_afr_3_scores.txt", connection_threshold=10.0, edge_labels=True)
