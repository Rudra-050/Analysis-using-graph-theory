from image_process import preprocess_image, detect_nodes_edges
from analysis import build_graph, is_eulerian, has_hamiltonian_path
import matplotlib.pyplot as plt
import networkx as nx
import os

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

def analyze_graph_from_image(image_path):
    """Analyze graph from an image file."""
    edges_img = preprocess_image(image_path)
    if edges_img is None:
        print("❌ ERROR: Image preprocessing failed.")
        return
    
    nodes, edges = detect_nodes_edges(edges_img)
    if not nodes or not edges:
        print("❌ ERROR: Node/Edge detection failed or returned empty lists.")
        return
    
    graph = build_graph(nodes, edges)
    eulerian_status = is_eulerian(graph)
    hamiltonian_status = has_hamiltonian_path(graph)
    
    print("\n🔍 Graph Analysis Results:")
    print(f"✅ Eulerian Path Status: {eulerian_status}")
    print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
    plot_graph(nodes, edges, eulerian_status, hamiltonian_status)

def analyze_graph_from_input():
    """Allow user to input nodes and edges manually."""
    num_nodes = int(input("Enter the number of nodes: "))
    nodes = []
    for i in range(num_nodes):
        node = input(f"Enter node {i+1} label: ")
        nodes.append(node)
    
    num_edges = int(input("Enter the number of edges: "))
    edges = []
    for i in range(num_edges):
        u, v = input(f"Enter edge {i+1} (node1 node2): ").split()
        edges.append((u, v))
    
    graph = build_graph(nodes, edges)
    eulerian_status = is_eulerian(graph)
    hamiltonian_status = has_hamiltonian_path(graph)
    
    print("\n🔍 Graph Analysis Results:")
    print(f"✅ Eulerian Path Status: {eulerian_status}")
    print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
    plot_graph(nodes, edges, eulerian_status, hamiltonian_status)

def plot_graph(nodes, edges, eulerian_status, hamiltonian_status):
    """Plot the detected graph using NetworkX."""
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="black", node_size=800, font_size=10)
    
    if eulerian_status in ["Eulerian Circuit", "Eulerian Path"]:
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)
    
    if hamiltonian_status == "Hamiltonian Path Exists":
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color="green", node_size=800)
    
    plt.title("Graph Visualization")
    plt.show()

if __name__ == "__main__":
    print("Choose analysis mode:")
    print("1. Predefined Case Studies")
    print("2. Load graph from an image")
    print("3. Enter graph manually")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        print("Select a case study:")
        print("1. Logistics Optimization")
        print("2. Social Network Analysis")
        print("3. Traffic Network")
        case_choice = input("Enter case number: ").strip()
        predefined_case_study(case_choice)
    elif choice == "2":
        image_path = input("Enter the image path: ").strip()
        if not os.path.exists(image_path):
            print("❌ ERROR: Image file not found!")
        else:
            analyze_graph_from_image(image_path)
    elif choice == "3":
        analyze_graph_from_input()
    else:
        print("❌ ERROR: Invalid choice! Please restart the program.")
