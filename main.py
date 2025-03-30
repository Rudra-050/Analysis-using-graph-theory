from image_process import preprocess_image, detect_nodes_edges
from analysis import build_graph, is_eulerian, has_hamiltonian_path
import matplotlib.pyplot as plt
import networkx as nx
import os
import cv2
import numpy as np

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
    """Enhanced graph analysis from image with better detection."""
    try:
        print(f"\nProcessing image: {os.path.basename(image_path)}")
        
        # Step 1: Enhanced preprocessing
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            print("❌ Image preprocessing failed")
            return
            
        # Step 2: Improved node and edge detection
        nodes, edges = detect_nodes_edges(processed_img)
        if not nodes or not edges:
            print("⚠️ Initial detection failed, trying alternative methods...")
            nodes, edges = alternative_detection(image_path)
            if not nodes or not edges:
                print("❌ ERROR: Node/Edge detection failed after all attempts")
                return
        
        # Step 3: Build and analyze graph
        graph = build_graph(nodes, edges)
        eulerian_status = is_eulerian(graph)
        hamiltonian_status = has_hamiltonian_path(graph)
        
        # Step 4: Visualization and results
        print("\n🔍 Graph Analysis Results:")
        print(f"• Detected {len(nodes)} nodes and {len(edges)} edges")
        print(f"✅ Eulerian Path Status: {eulerian_status}")
        print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
        
        # Save visualization
        visualization_path = os.path.join(os.path.dirname(image_path), 
                                f"result_{os.path.basename(image_path)}")
        save_visualization(image_path, nodes, edges, visualization_path)
        print(f"💾 Visualization saved to: {visualization_path}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def alternative_detection(image_path):
    """Fallback detection method when primary fails."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Alternative thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    nodes = []
    edges = []
    min_node_area = 100
    max_node_area = 3000
    min_edge_length = 20
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = w/h
        
        # Node detection
        if min_node_area < area < max_node_area and 0.7 < aspect_ratio < 1.3:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                nodes.append((cx, cy))
        
        # Edge detection
        elif area > min_edge_length and max(w,h)/min(w,h) > 3:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) >= 2:
                pt1 = tuple(approx[0][0])
                pt2 = tuple(approx[-1][0])
                edges.append((pt1, pt2))
    
    return nodes, edges

def save_visualization(image_path, nodes, edges, output_path):
    """Save visualization to file with node/edge highlighting."""
    img = cv2.imread(image_path)
    
    # Draw nodes
    for i, (x,y) in enumerate(nodes):
        cv2.circle(img, (x,y), 10, (0,255,0), 2)
        cv2.putText(img, str(i), (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    
    # Draw edges
    for (pt1, pt2) in edges:
        cv2.line(img, pt1, pt2, (255,0,0), 2)
    
    cv2.imwrite(output_path, img)

def analyze_graph_from_input():
    """Manual graph input with validation."""
    try:
        num_nodes = int(input("Enter the number of nodes: "))
        if num_nodes <= 0:
            raise ValueError("Number of nodes must be positive")
            
        nodes = []
        for i in range(num_nodes):
            node = input(f"Enter node {i+1} label: ").strip()
            if not node:
                raise ValueError("Node label cannot be empty")
            nodes.append(node)
        
        num_edges = int(input("Enter the number of edges: "))
        edges = []
        for i in range(num_edges):
            parts = input(f"Enter edge {i+1} (node1 node2): ").split()
            if len(parts) != 2:
                raise ValueError("Edge must have exactly two nodes")
            u, v = parts
            if u not in nodes or v not in nodes:
                raise ValueError("Edge nodes must exist in node list")
            edges.append((u, v))
        
        graph = build_graph(nodes, edges)
        eulerian_status = is_eulerian(graph)
        hamiltonian_status = has_hamiltonian_path(graph)
        
        print("\n🔍 Graph Analysis Results:")
        print(f"✅ Eulerian Path Status: {eulerian_status}")
        print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
        plot_graph(nodes, edges, eulerian_status, hamiltonian_status)
        
    except ValueError as e:
        print(f"❌ Input error: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def plot_graph(nodes, edges, eulerian_status, hamiltonian_status):
    """Enhanced graph visualization with analysis highlights."""
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
    print("Choose analysis mode:")
    print("1. Predefined Case Studies")
    print("2. Load graph from an image")
    print("3. Enter graph manually")
    
    try:
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            print("\nAvailable Case Studies:")
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
            print("❌ ERROR: Invalid choice! Please select 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
