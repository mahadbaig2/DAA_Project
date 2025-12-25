import heapq
import copy


def dijkstra(graph, source):
    """Dijkstra's algorithm - works on directed/undirected graphs with non-negative weights"""
    dist = {n: float("inf") for n in graph.nodes}
    prev = {}
    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    while pq:
        cd, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)

        for v in graph.neighbors(u):
            w = graph[u][v]["distance"]
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def bellman_ford(graph, source):
    """Bellman-Ford algorithm - works with negative weights, detects negative cycles"""
    dist = {n: float("inf") for n in graph.nodes}
    prev = {}
    dist[source] = 0

    # Relax edges |V|-1 times
    for _ in range(len(graph.nodes) - 1):
        for u, v, data in graph.edges(data=True):
            w = data["distance"]
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    # Check for negative cycles
    for u, v, data in graph.edges(data=True):
        w = data["distance"]
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist, prev


def floyd_warshall(graph):
    """Floyd-Warshall algorithm - computes all-pairs shortest paths"""
    nodes = list(graph.nodes)
    dist = {i: {j: float("inf") for j in nodes} for i in nodes}
    next_node = {i: {j: None for j in nodes} for i in nodes}

    # Initialize distances
    for n in nodes:
        dist[n][n] = 0

    for u, v, data in graph.edges(data=True):
        dist[u][v] = data["distance"]
        next_node[u][v] = v

    # Floyd-Warshall main loop
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node