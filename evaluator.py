import time
from algorithms import dijkstra, bellman_ford, floyd_warshall


def reconstruct_path(prev, src, dst):
    """Reconstruct path from source to destination using prev dictionary"""
    if dst not in prev and dst != src:
        return None

    path = []
    curr = dst
    while curr != src:
        path.append(curr)
        curr = prev.get(curr)
        if curr is None:
            return None
    path.append(src)
    return path[::-1]


def reconstruct_path_fw(next_node, src, dst):
    """Reconstruct path for Floyd-Warshall using next_node matrix"""
    if next_node[src][dst] is None:
        return None

    path = [src]
    curr = src
    while curr != dst:
        curr = next_node[curr][dst]
        if curr is None:
            return None
        path.append(curr)
    return path


def evaluate_algorithms(graph, source, destination):
    """Evaluate all three pathfinding algorithms"""
    results = {}

    # Dijkstra's Algorithm
    start = time.time()
    dist_d, prev_d = dijkstra(graph, source)
    time_d = time.time() - start
    path_d = reconstruct_path(prev_d, source, destination)

    results["Dijkstra"] = {
        "time": time_d,
        "path": path_d if path_d else [],
        "distance": dist_d.get(destination, float('inf'))
    }

    # Bellman-Ford Algorithm
    start = time.time()
    dist_bf, prev_bf = bellman_ford(graph, source)
    time_bf = time.time() - start
    path_bf = reconstruct_path(prev_bf, source, destination)

    results["Bellman-Ford"] = {
        "time": time_bf,
        "path": path_bf if path_bf else [],
        "distance": dist_bf.get(destination, float('inf'))
    }

    # Floyd-Warshall Algorithm
    start = time.time()
    dist_fw, next_fw = floyd_warshall(graph)
    time_fw = time.time() - start
    path_fw = reconstruct_path_fw(next_fw, source, destination)

    results["Floyd-Warshall"] = {
        "time": time_fw,
        "path": path_fw if path_fw else [],
        "distance": dist_fw[source][destination]
    }

    return results