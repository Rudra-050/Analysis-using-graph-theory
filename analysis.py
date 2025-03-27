from collections import defaultdict

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
