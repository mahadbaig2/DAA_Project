import heapq
import time
from typing import Dict, List, Tuple, Optional


class PathfindingResult:
    """Container for algorithm results"""

    def __init__(self, path: List[str], total_weight: float,
                 execution_time: float, details: Dict):
        self.path = path
        self.total_weight = total_weight
        self.execution_time = execution_time
        self.details = details


def dijkstra_shortest_distance(graph, source: str, destination: str) -> PathfindingResult:
    """
    Dijkstra's Algorithm - Optimized for SHORTEST DISTANCE
    Greedy approach: always picks the nearest unvisited node
    Time Complexity: O((V + E) log V) with binary heap
    Space Complexity: O(V)
    """
    start_time = time.time()

    dist = {node: float('inf') for node in graph.nodes()}
    prev = {}
    dist[source] = 0
    pq = [(0, source)]
    visited = set()
    nodes_explored = 0

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)
        nodes_explored += 1

        if u == destination:
            break

        for v in graph.neighbors(u):
            edge_data = graph[u][v]
            weight = edge_data['distance']  # Optimize for DISTANCE

            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    # Reconstruct path
    path = []
    current = destination
    while current in prev:
        path.append(current)
        current = prev[current]
    path.append(source)
    path.reverse()

    # Calculate detailed metrics
    total_distance = 0
    total_time = 0
    total_cost = 0

    for i in range(len(path) - 1):
        edge = graph[path[i]][path[i + 1]]
        total_distance += edge['distance']
        total_time += edge['time']
        total_cost += edge['cost']

    execution_time = time.time() - start_time

    details = {
        'optimization_target': 'Shortest Distance',
        'algorithm_type': 'Greedy (Single-Source)',
        'nodes_explored': nodes_explored,
        'total_distance': round(total_distance, 2),
        'total_time': round(total_time, 2),
        'total_cost': round(total_cost, 2),
        'hops': len(path) - 1
    }

    return PathfindingResult(path, dist[destination], execution_time, details)


def bellman_ford_cheapest_route(graph, source: str, destination: str) -> PathfindingResult:
    """
    Bellman-Ford Algorithm - Optimized for CHEAPEST COST
    Dynamic Programming: handles negative weights, penalty adjustments
    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """
    start_time = time.time()

    dist = {node: float('inf') for node in graph.nodes()}
    prev = {}
    dist[source] = 0
    iterations = 0

    # Relax edges |V| - 1 times
    for _ in range(len(graph.nodes()) - 1):
        iterations += 1
        updated = False

        for u, v, data in graph.edges(data=True):
            # Optimize for COST with penalties
            base_cost = data['cost']

            # Apply dynamic pricing adjustments
            # Reward direct flights (fewer layovers)
            layover_penalty = data['layover'] * 50  # $50 per hour layover

            # Fuel surcharge affects cost optimization differently
            adjusted_cost = base_cost + layover_penalty

            if dist[u] != float('inf') and dist[u] + adjusted_cost < dist[v]:
                dist[v] = dist[u] + adjusted_cost
                prev[v] = u
                updated = True

        if not updated:
            break

    # Check for negative cycles
    for u, v, data in graph.edges(data=True):
        adjusted_cost = data['cost'] + data['layover'] * 50
        if dist[u] != float('inf') and dist[u] + adjusted_cost < dist[v]:
            raise ValueError("Graph contains negative-weight cycle")

    # Reconstruct path
    path = []
    current = destination
    while current in prev:
        path.append(current)
        current = prev[current]
    path.append(source)
    path.reverse()

    # Calculate metrics
    total_distance = 0
    total_time = 0
    total_cost = 0

    for i in range(len(path) - 1):
        edge = graph[path[i]][path[i + 1]]
        total_distance += edge['distance']
        total_time += edge['time']
        total_cost += edge['cost']

    execution_time = time.time() - start_time

    details = {
        'optimization_target': 'Cheapest Cost',
        'algorithm_type': 'Dynamic Programming',
        'iterations': iterations,
        'total_distance': round(total_distance, 2),
        'total_time': round(total_time, 2),
        'total_cost': round(total_cost, 2),
        'hops': len(path) - 1
    }

    return PathfindingResult(path, dist[destination], execution_time, details)


def floyd_warshall_fastest_time(graph, source: str, destination: str) -> PathfindingResult:
    """
    Floyd-Warshall Algorithm - Optimized for FASTEST TIME
    All-Pairs Shortest Path: precomputes all routes globally
    Time Complexity: O(V³)
    Space Complexity: O(V²)
    """
    start_time = time.time()

    nodes = list(graph.nodes())
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}

    # Initialize distance and next matrices
    dist = [[float('inf')] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    # Set diagonal to 0
    for i in range(n):
        dist[i][i] = 0

    # Initialize with edge weights (optimizing for TIME)
    for u, v, data in graph.edges(data=True):
        i, j = node_idx[u], node_idx[v]
        # Optimize for TIME (includes layover consideration)
        dist[i][j] = data['time']
        next_node[i][j] = j

    # Floyd-Warshall main loop
    operations = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                operations += 1
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    # Reconstruct path
    src_idx = node_idx[source]
    dst_idx = node_idx[destination]

    if next_node[src_idx][dst_idx] is None:
        return PathfindingResult([], float('inf'), time.time() - start_time, {})

    path = [nodes[src_idx]]
    current = src_idx
    while current != dst_idx:
        current = next_node[current][dst_idx]
        path.append(nodes[current])

    # Calculate metrics
    total_distance = 0
    total_time = 0
    total_cost = 0

    for i in range(len(path) - 1):
        edge = graph[path[i]][path[i + 1]]
        total_distance += edge['distance']
        total_time += edge['time']
        total_cost += edge['cost']

    execution_time = time.time() - start_time

    details = {
        'optimization_target': 'Fastest Time',
        'algorithm_type': 'All-Pairs (Global Optimization)',
        'total_operations': operations,
        'matrix_size': f"{n}x{n}",
        'total_distance': round(total_distance, 2),
        'total_time': round(total_time, 2),
        'total_cost': round(total_cost, 2),
        'hops': len(path) - 1
    }

    return PathfindingResult(path, dist[src_idx][dst_idx], execution_time, details)


def compare_all_algorithms(graph, source: str, destination: str) -> Dict:
    """Run all three algorithms and return comparison"""

    results = {}

    try:
        # Dijkstra - Shortest Distance
        results['Dijkstra'] = dijkstra_shortest_distance(graph, source, destination)
    except Exception as e:
        print(f"Dijkstra failed: {e}")
        results['Dijkstra'] = None

    try:
        # Bellman-Ford - Cheapest Cost
        results['Bellman-Ford'] = bellman_ford_cheapest_route(graph, source, destination)
    except Exception as e:
        print(f"Bellman-Ford failed: {e}")
        results['Bellman-Ford'] = None

    try:
        # Floyd-Warshall - Fastest Time
        results['Floyd-Warshall'] = floyd_warshall_fastest_time(graph, source, destination)
    except Exception as e:
        print(f"Floyd-Warshall failed: {e}")
        results['Floyd-Warshall'] = None

    return results