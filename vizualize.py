from utils.graph import GraphViz


if __name__ == "__main__":
    FILENAME = "pl_afr_3_scores.txt"
    gv = GraphViz()
    gv.draw(f"seasons_score/{FILENAME}", connection_threshold=10.0, edge_labels=True)
