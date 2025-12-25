import time
from algorithms import dijkstra, bellman_ford, floyd_warshall

def reconstruct_path(prev, src, dst):
    path = []
    curr = dst
    while curr != src:
        path.append(curr)
        curr = prev.get(curr)
        if curr is None:
            return None
    path.append(src)
    return path[::-1]


def evaluate_algorithms(graph, source, destination):
    results = {}

    # Dijkstra
    start = time.time()
    dist, prev = dijkstra(graph, source)
    results["Dijkstra"] = {
        "time": time.time() - start,
        "path": reconstruct_path(prev, source, destination),
        "distance": dist[destination]
    }

    # Bellman-Ford
    start = time.time()
    dist, prev = bellman_ford(graph, source)
    results["Bellman-Ford"] = {
        "time": time.time() - start,
        "path": reconstruct_path(prev, source, destination),
        "distance": dist[destination]
    }

    # Floyd-Warshall
    start = time.time()
    fw = floyd_warshall(graph)
    results["Floyd-Warshall"] = {
        "time": time.time() - start,
        "distance": fw[source][destination],
        "path": "Computed via matrix"
    }

    return results
