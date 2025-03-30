from analysis import build_graph, is_eulerian, has_hamiltonian_path
import matplotlib.pyplot as plt
import networkx as nx

def predefined_case_study(choice):
    """Predefined real-world graph cases for analysis."""
    case_studies = {
        "1": {
            "name": "Logistics Optimization",
            "nodes": ["Warehouse A", "Warehouse B", "City 1", "City 2", "City 3"],
            "edges": [("Warehouse A", "City 1"), ("Warehouse A", "City 2"),
                     ("City 1", "City 3"), ("City 2", "City 3"), ("City 3", "Warehouse B")],
            "insight": "Eulerian circuits help optimize delivery routes."
        },
        "2": {
            "name": "Social Network Analysis",
            "nodes": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "edges": [("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "David"),
                     ("Charlie", "David"), ("David", "Eve"), ("Eve", "Alice")],
            "insight": "Hamiltonian paths reveal strong social connections."
        },
        "3": {
            "name": "Traffic Network",
            "nodes": ["Intersection 1", "Intersection 2", "Intersection 3", "Intersection 4"],
            "edges": [("Intersection 1", "Intersection 2"), ("Intersection 2", "Intersection 3"),
                     ("Intersection 3", "Intersection 4"), ("Intersection 4", "Intersection 1"),
                     ("Intersection 1", "Intersection 3")],
            "insight": "Eulerian paths help in efficient street cleaning planning."
        }
    }
    
    case = case_studies.get(choice)
    if case:
        graph = build_graph(case["nodes"], case["edges"])
        eulerian_status = is_eulerian(graph)
        hamiltonian_status = has_hamiltonian_path(graph)
        
        print(f"\n🔍 {case['name']} Analysis:")
        print(f"✅ Eulerian Path Status: {eulerian_status}")
        print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
        print(f"💡 Insight: {case['insight']}")
        
        plot_graph(case["nodes"], case["edges"], eulerian_status, hamiltonian_status)
    else:
        print("❌ ERROR: Invalid case study selection!")

def analyze_graph_from_input():
    """Manual graph input with validation."""
    try:
        print("\n📝 Manual Graph Input")
        print("Enter node labels (one per line, blank to finish):")
        nodes = []
        while True:
            node = input("Node label: ").strip()
            if not node:
                if len(nodes) >= 2:
                    break
                print("Need at least 2 nodes")
                continue
            nodes.append(node)
        
        print("\nEnter edges as pairs of node indices (0-based):")
        edges = []
        while True:
            edge = input("Edge (i j): ").strip()
            if not edge:
                if edges:
                    break
                print("Need at least 1 edge")
                continue
            try:
                i, j = map(int, edge.split())
                if 0 <= i < len(nodes) and 0 <= j < len(nodes):
                    edges.append((nodes[i], nodes[j]))
                else:
                    print("Invalid node indices")
            except:
                print("Use format: i j")
        
        analyze_and_visualize(nodes, edges)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def analyze_and_visualize(nodes, edges):
    """Common analysis and visualization routine."""
    try:
        graph = build_graph(nodes, edges)
        eulerian_status = is_eulerian(graph)
        hamiltonian_status = has_hamiltonian_path(graph)
        
        print("\n🔍 Graph Analysis Results:")
        print(f"• Nodes: {len(nodes)}")
        print(f"• Edges: {len(edges)}")
        print(f"✅ Eulerian Path Status: {eulerian_status}")
        print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
        
        plot_graph(nodes, edges, eulerian_status, hamiltonian_status)
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")

def plot_graph(nodes, edges, eulerian_status, hamiltonian_status):
    """Visualize the graph with analysis highlights."""
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Base drawing
    nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=800)
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1)
    
    # Highlight Eulerian path if exists
    if "Eulerian" in eulerian_status:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)
    
    # Highlight Hamiltonian path if exists
    if hamiltonian_status == "Hamiltonian Path Exists":
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color="green", node_size=800)
    
    plt.title(f"Graph Analysis\nEulerian: {eulerian_status} | Hamiltonian: {hamiltonian_status}")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    print("\n📊 Graph Analysis Tool")
    print("="*40)
    while True:
        print("\nChoose analysis mode:")
        print("1. Predefined Case Studies")
        print("2. Enter graph manually")
        print("3. Exit")
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\nAvailable Case Studies:")
                print("1. Logistics Optimization")
                print("2. Social Network Analysis")
                print("3. Traffic Network")
                case_choice = input("Enter case number: ").strip()
                predefined_case_study(case_choice)
            elif choice == "2":
                analyze_graph_from_input()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("❌ Invalid choice")
        except KeyboardInterrupt:
            print("\nOperation cancelled")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
