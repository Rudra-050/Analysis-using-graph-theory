from collections import defaultdict
import cv2
import numpy as np
from matplotlib import pyplot as plt

def build_graph(nodes, edges):
    """Convert detected nodes and edges into an adjacency list."""
    graph = defaultdict(set)  # Use set to avoid duplicate edges
    
    for edge in edges:
        u, v = edge
        if u != v:  # Avoid self-loops
            graph[u].add(v)
            graph[v].add(u)  # Undirected graph

    return {node: list(neighbors) for node, neighbors in graph.items()}  # Convert to list for consistency

def is_eulerian(graph):
    """Check if the graph is Eulerian."""
    odd_degree_nodes = [node for node in graph if len(graph[node]) % 2 != 0]
    
    if len(odd_degree_nodes) == 0:
        return "Eulerian Circuit ✅"
    elif len(odd_degree_nodes) == 2:
        return "Eulerian Path ✅"
    else:
        return "❌ Neither Eulerian Circuit nor Eulerian Path"

def is_hamiltonian_path(graph, path, visited):
    """Recursive function to check for a Hamiltonian Path."""
    if len(path) == len(graph):  # If path covers all nodes, it's Hamiltonian
        return True
    
    last_node = path[-1]
    for neighbor in graph[last_node]:
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)
            
            if is_hamiltonian_path(graph, path, visited):  # Return early if found
                return True
            
            path.pop()
            visited.remove(neighbor)

    return False

def has_hamiltonian_path(graph):
    """Check if a Hamiltonian path exists."""
    for start_node in graph:
        if is_hamiltonian_path(graph, [start_node], {start_node}):
            return "Hamiltonian Path Exists ✅"
    return "❌ No Hamiltonian Path Found"

def analyze_graph(nodes, edges):
    """Improved graph analysis with validation"""
    if len(nodes) < 2:
        print("❌ Insufficient nodes for analysis")
        return
    
    # Build adjacency list
    adj = {i: [] for i in range(len(nodes))}
    edge_count = 0
    
    for (pt1, pt2) in edges:
        # Find closest nodes to edge endpoints
        n1 = min(range(len(nodes)), key=lambda i: np.linalg.norm(np.array(nodes[i])-np.array(pt1)))
        n2 = min(range(len(nodes)), key=lambda i: np.linalg.norm(np.array(nodes[i])-np.array(pt2)))
        
        if n1 != n2:
            adj[n1].append(n2)
            adj[n2].append(n1)
            edge_count += 1
    
    # Analysis
    degrees = [len(links) for links in adj.values()]
    odd_degree = sum(1 for d in degrees if d % 2 != 0)
    
    print("\n🔍 Enhanced Analysis Results:")
    print(f"• Total nodes: {len(nodes)}")
    print(f"• Valid edges: {edge_count}")
    print(f"• Node degrees: {degrees}")
    
    # Eulerian analysis
    if odd_degree == 0:
        print("✅ Eulerian Circuit exists")
    elif odd_degree == 2:
        print("✅ Eulerian Path exists")
    else:
        print("❌ No Eulerian Path/Circuit")
    
    # Hamiltonian analysis (simplified check)
    if len(nodes) > 2 and edge_count >= len(nodes):
        print("⚠️ Possible Hamiltonian Path (needs verification)")
    else:
        print("❌ No Hamiltonian Path detected")

def visualize(image_path, nodes, edges):
    """Enhanced visualization with labels"""
    img = cv2.imread(image_path)
    for i, (x,y) in enumerate(nodes):
        cv2.circle(img, (x,y), 10, (0,255,0), 2)
        cv2.putText(img, str(i), (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    
    for (pt1, pt2) in edges:
        cv2.line(img, pt1, pt2, (255,0,0), 2)
    
    cv2.imwrite('analysis_result.jpg', img)
    print("💾 Saved visualization to analysis_result.jpg")
