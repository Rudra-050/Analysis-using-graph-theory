from image_process import preprocess_image, detect_nodes_edges
from analysis import build_graph, is_eulerian, has_hamiltonian_path
import matplotlib.pyplot as plt
import networkx as nx
import os
import cv2
import numpy as np
import json

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
    """Enhanced graph analysis from image with multiple fallback methods."""
    try:
        print(f"\nProcessing image: {os.path.basename(image_path)}")
        
        # Try standard detection first
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            print("❌ Image preprocessing failed")
            return
            
        nodes, edges = detect_nodes_edges(processed_img)
        
        # If detection fails, try alternative methods
        if not nodes or not edges:
            print("⚠️ Primary detection failed, trying alternative methods...")
            nodes, edges = alternative_detection_methods(image_path)
            if not nodes or not edges:
                print("❌ All detection methods failed")
                offer_alternatives(image_path)
                return
        
        # Successful detection - proceed with analysis
        analyze_and_visualize(nodes, edges, image_path)
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        offer_alternatives(image_path)

def alternative_detection_methods(image_path):
    """Try multiple detection approaches."""
    methods = [
        detect_with_contours,
        detect_with_hough,
        detect_with_feature_matching
    ]
    
    for method in methods:
        nodes, edges = method(image_path)
        if nodes and edges:
            print(f"✅ Success with {method.__name__}")
            return nodes, edges
        print(f"⚠️ {method.__name__} failed")
    
    return [], []

def detect_with_contours(image_path):
    """Contour-based detection."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    nodes = []
    edges = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        
        # Node detection
        if 100 < area < 3000 and 0.7 < w/h < 1.3:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                nodes.append((int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])))
        
        # Edge detection
        elif area > 20 and max(w,h)/min(w,h) > 3:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) >= 2:
                edges.append((tuple(approx[0][0]), tuple(approx[-1][0])))
    
    return nodes, edges

def detect_with_hough(image_path):
    """Hough transform-based detection with proper type conversion"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Detect circles (nodes)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                             param1=50, param2=30, minRadius=5, maxRadius=50)
    
    nodes = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            # Convert to standard Python int types
            nodes.append((int(circle[0]), int(circle[1])))
    
    # Detect lines (edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                          minLineLength=30, maxLineGap=10)
    edges = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Convert to tuples of integers
            edges.append(((int(x1), int(y1)), (int(x2), int(y2))))
    
    return nodes, edges

def detect_with_feature_matching(image_path):
    """Feature-based detection (for special graph types)."""
    # This would be customized based on your specific graph images
    # Implement your own feature detection logic here
    return [], []  # Placeholder

def offer_alternatives(image_path=None):
    """Provide alternative analysis options with exit handling"""
    print("\n🔧 Image analysis failed. Options:")
    print("1. Enter graph manually")
    print("2. Use a predefined case study")
    if image_path:
        print("3. Try editing the image")
    print("Or press 'q' to return to main menu")
    
    choice = input("Your choice: ").strip().lower()
    if choice == 'q':
        return
    elif choice == "1":
        analyze_graph_from_input()
    elif choice == "2":
        print("Available cases: 1, 2, 3 (or 'q' to cancel)")
        case_choice = input("Select case: ").strip().lower()
        if case_choice != 'q':
            predefined_case_study(case_choice)
    elif choice == "3" and image_path:
        print("Try improving contrast or removing noise from the image")
        analyze_graph_from_image(image_path)

def analyze_and_visualize(nodes, edges, image_path=None):
    """Common analysis and visualization routine with validation"""
    try:
        # Validate and normalize nodes
        validated_nodes = []
        for node in nodes:
            if isinstance(node, tuple) and len(node) == 2:
                try:
                    x = float(node[0])
                    y = float(node[1])
                    validated_nodes.append((x, y))
                except (ValueError, TypeError):
                    print(f"⚠️ Invalid node coordinates: {node}")
                    validated_nodes.append((0, 0))  # Default position
            else:
                validated_nodes.append(str(node))
        
        # Validate edges - NEW FIXED VERSION
        validated_edges = []
        for edge in edges:
            try:
                if isinstance(validated_nodes[0], tuple):
                    # For coordinate graphs
                    if (isinstance(edge, (tuple, list)) and len(edge) == 2):
                        if (isinstance(edge[0], (tuple, list)) and len(edge[0])== 2) and \
                           (isinstance(edge[1], (tuple, list)) and len(edge[1]) == 2):
                            validated_edges.append((
                                (float(edge[0][0]), float(edge[0][1])),
                                (float(edge[1][0]), float(edge[1][1]))
                            ))
                else:
                    # For labeled graphs
                    if len(edge) == 2:
                        validated_edges.append((str(edge[0]), str(edge[1])))
            except (ValueError, TypeError, IndexError):
                print(f"⚠️ Invalid edge skipped: {edge}")
        
        # Build and analyze graph
        graph = build_graph(validated_nodes, validated_edges)  # Now using validated_edges
        eulerian_status = is_eulerian(graph)
        hamiltonian_status = has_hamiltonian_path(graph)
        
        print("\n🔍 Graph Analysis Results:")
        print(f"• Valid nodes: {len(validated_nodes)}")
        print(f"• Valid edges: {len(validated_edges)}")  # Now properly defined
        print(f"✅ Eulerian Path Status: {eulerian_status}")
        print(f"✅ Hamiltonian Path Exists? {hamiltonian_status}")
        
        if image_path:
            try:
                visualization_path = f"result_{os.path.basename(image_path)}"
                save_visualization(image_path, validated_nodes, validated_edges, visualization_path)
                print(f"💾 Visualization saved to: {visualization_path}")
            except Exception as e:
                print(f"⚠️ Could not save visualization: {str(e)}")
        
        plot_graph(validated_nodes, validated_edges, eulerian_status, hamiltonian_status)
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")

def save_visualization(image_path, nodes, edges, output_path):
    """Save visualization with type-checked coordinates"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image")
            
        # Draw nodes with type conversion
        for i, (x, y) in enumerate(nodes):
            try:
                x_int, y_int = int(round(float(x))), int(round(float(y)))
                cv2.circle(img, (x_int, y_int), 10, (0,255,0), 2)
                cv2.putText(img, str(i), (x_int-10, y_int-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            except (ValueError, TypeError) as e:
                print(f"⚠️ Skipping invalid node {i}: {x},{y} - {str(e)}")
        
        # Draw edges with type conversion
        for (pt1, pt2) in edges:
            try:
                x1, y1 = int(round(float(pt1[0]))), int(round(float(pt1[1])))
                x2, y2 = int(round(float(pt2[0]))), int(round(float(pt2[1])))
                cv2.line(img, (x1, y1), (x2, y2), (255,0,0), 2)
            except (ValueError, TypeError, IndexError) as e:
                print(f"⚠️ Skipping invalid edge: {pt1}-{pt2} - {str(e)}")
        
        cv2.imwrite(output_path, img)
        return True
    except Exception as e:
        print(f"❌ Failed to save visualization: {str(e)}")
        return False

def analyze_graph_from_input():
    """Manual graph input with validation and exit handling"""
    try:
        print("\n📝 Manual Graph Input (enter 'q' at any time to cancel)")
        nodes = []
        while True:
            node = input("Node label (blank when done): ").strip()
            if node.lower() in ['q', 'quit']:
                print("Cancelling manual input...")
                return
            if not node:
                if len(nodes) >= 2:
                    break
                print("Need at least 2 nodes")
                continue
            nodes.append(node)
        
        print("\nEnter edges as pairs (0-based indices), blank when done:")
        edges = []
        while True:
            edge = input("Edge (i j): ").strip().lower()
            if edge in ['q', 'quit']:
                print("Cancelling manual input...")
                return
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
        
    except KeyboardInterrupt:
        print("\nInput cancelled")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def plot_graph(nodes, edges, eulerian_status, hamiltonian_status):
    """Robust visualization with position handling"""
    G = nx.Graph()
    
    # Create nodes with valid positions
    pos = {}
    for i, node in enumerate(nodes):
        if isinstance(node, tuple):
            G.add_node(i)
            pos[i] = node  # Use exact coordinates
        else:
            G.add_node(node)
    
    # Add only valid edges
    for edge in edges:
        try:
            if isinstance(nodes[0], tuple):
                G.add_edge(edge[0], edge[1])
            else:
                G.add_edge(*edge)
        except:
            continue  # Skip invalid edges
    
    # Generate layout if no coordinates
    if not pos:
        pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 8))
    
    # Draw with appropriate styling
    node_color = "green" if hamiltonian_status == "Hamiltonian Path Exists" else "skyblue"
    edge_color = "red" if "Eulerian" in eulerian_status else "gray"
    
    nx.draw(G, pos, 
            with_labels=True,
            node_color=node_color,
            edge_color=edge_color,
            node_size=800,
            width=2 if "Eulerian" in eulerian_status else 1)
    
    plt.title(f"Graph Analysis\nEulerian: {eulerian_status}\nHamiltonian: {hamiltonian_status}")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    print("\n📊 Graph Analysis Tool")
    print("="*40)
    print("Press 'q' at any time to exit or return to main menu\n")
    
    while True:
        print("\nChoose analysis mode:")
        print("1. Predefined Case Studies")
        print("2. Load graph from an image")
        print("3. Enter graph manually")
        print("4. Exit")
        
        try:
            choice = input("Enter your choice (1-4 or 'q' to quit): ").strip().lower()
            
            # Exit handling
            if choice in ['q', 'quit', 'exit', '4']:
                print("\nExiting Graph Analysis Tool...")
                break
                
            if choice == "1":
                print("\nAvailable Case Studies:")
                print("1. Logistics Optimization")
                print("2. Social Network Analysis")
                print("3. Traffic Network")
                print("Or press 'q' to return to main menu")
                case_choice = input("Enter case number: ").strip().lower()
                
                if case_choice == 'q':
                    continue
                predefined_case_study(case_choice)
                
            elif choice == "2":
                print("\nEnter image path or 'q' to return to main menu")
                image_path = input("Path: ").strip()
                if image_path.lower() == 'q':
                    continue
                if os.path.exists(image_path):
                    analyze_graph_from_image(image_path)
                else:
                    print("❌ Image not found")
                    offer_alternatives()
                    
            elif choice == "3":
                print("\nManual entry - press 'q' at any prompt to cancel")
                analyze_graph_from_input()
                
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
