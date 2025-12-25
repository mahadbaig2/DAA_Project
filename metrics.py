def calculate_metrics(path, graph):
    distance = 0
    time = 0

    for i in range(len(path) - 1):
        edge = graph[path[i]][path[i+1]]
        distance += edge["distance"]
        time += edge["time"]

    return {
        "Distance (km)": round(distance, 1),
        "Travel Time (hrs)": round(time, 2),
        "Fuel Cost ($)": round(distance * 0.12, 2)
    }
