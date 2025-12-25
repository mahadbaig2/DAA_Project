import heapq

def dijkstra(graph, source):
    dist = {n: float("inf") for n in graph.nodes}
    prev = {}
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        cd, u = heapq.heappop(pq)
        for v in graph.neighbors(u):
            w = graph[u][v]["distance"]
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev

def bellman_ford(graph, source):
    dist = {n: float("inf") for n in graph.nodes}
    prev = {}
    dist[source] = 0

    for _ in range(len(graph.nodes) - 1):
        for u, v, data in graph.edges(data=True):
            w = data["distance"]
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    return dist, prev

def floyd_warshall(graph):
    nodes = list(graph.nodes)
    dist = {i: {j: float("inf") for j in nodes} for i in nodes}

    for n in nodes:
        dist[n][n] = 0

    for u, v, data in graph.edges(data=True):
        dist[u][v] = data["distance"]

    for k in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist
