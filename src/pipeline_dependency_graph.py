import networkx as nx
import matplotlib.pyplot as plt

def draw_dependency_graph():
    # Define directed graph
    G = nx.DiGraph()
    
    # Explicitly map the architecture sequence
    G.add_edge('Orchestration_Service', 'ETL_Pipeline')
    G.add_edge('ETL_Pipeline', 'Data Quality Check')
    G.add_edge('Data Quality Check', 'Observability Dashboard')
    
    # Layout configuration
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    plt.title("Axiom Dataops Platform - Pipeline Dependency Lineage", fontsize=14, fontweight='bold', pad=20)
    
    # Render nodes and edges
    nx.draw_networkx(
        G, pos, 
        with_labels=True, 
        node_size=4500, 
        node_color='#9ecae1', 
        edge_color='#969696', 
        font_size=10, 
        font_weight='bold',
        width=2,
        arrowsize=20
    )
    
    plt.tight_layout()
    print("Displaying Pipeline Dependency Graph...")
    plt.show()

if __name__ == "__main__":
    draw_dependency_graph()