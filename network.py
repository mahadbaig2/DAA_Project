import networkx as nx
import random

def create_transport_network():
    G = nx.DiGraph()

    cities = [
        "Karachi", "Lahore", "Islamabad", "Peshawar",
        "Quetta", "Multan", "Faisalabad"
    ]

    for city in cities:
        G.add_node(city)

    for _ in range(18):
        u, v = random.sample(cities, 2)
        distance = random.randint(100, 1500)  # km
        speed = random.randint(60, 120)       # km/h

        G.add_edge(
            u, v,
            distance=distance,
            time=distance / speed
        )

    return G
