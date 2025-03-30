from collections import defaultdict

def build_graph(nodes, edges):
    """Convert nodes and edges into an adjacency list."""
    graph = defaultdict(set)  # Use set to avoid duplicate edges
    
    for edge in edges:
        u, v = edge
        if u != v:  # Avoid self-loops
            graph[u].add(v)
            graph[v].add(u)  # Undirected graph

    return {node: list(neighbors) for node, neighbors in graph.items()}

def is_eulerian(graph):
    """Check if the graph is Eulerian."""
    odd_degree_nodes = [node for node in graph if len(graph[node]) % 2 != 0]
    
    if len(odd_degree_nodes) == 0:
        return "Eulerian Circuit"
    elif len(odd_degree_nodes) == 2:
        return "Eulerian Path"
    else:
        return "Neither Eulerian Circuit nor Eulerian Path"

def is_hamiltonian_path(graph, path, visited):
    """Recursive helper function for Hamiltonian path check."""
    if len(path) == len(graph):
        return True
    
    last_node = path[-1]
    for neighbor in graph[last_node]:
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)
            
            if is_hamiltonian_path(graph, path, visited):
                return True
            
            path.pop()
            visited.remove(neighbor)

    return False

def has_hamiltonian_path(graph):
    """Check if a Hamiltonian path exists."""
    for start_node in graph:
        if is_hamiltonian_path(graph, [start_node], {start_node}):
            return "Hamiltonian Path Exists"
    return "No Hamiltonian Path Found"

def analyze_graph(nodes, edges):
    """Analyze graph properties with clear output."""
    if len(nodes) < 2:
        print("❌ Insufficient nodes for analysis")
        return
    
    graph = build_graph(nodes, edges)
    
    print("\n🔍 Graph Analysis Results:")
    print(f"• Total nodes: {len(nodes)}")
    print(f"• Total edges: {len(edges)}")
    
    # Calculate and show degrees
    degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    print(f"• Node degrees: {degrees}")
    
    # Eulerian analysis
    eulerian_status = is_eulerian(graph)
    print(f"✅ Eulerian Status: {eulerian_status}")
    
    # Hamiltonian analysis
    hamiltonian_status = has_hamiltonian_path(graph)
    print(f"✅ Hamiltonian Status: {hamiltonian_status}")
