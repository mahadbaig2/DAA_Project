import networkx as nx
import random


def create_transport_network(seed=42):
    """Create a deterministic transport network"""
    random.seed(seed)
    G = nx.DiGraph()

    cities = [
        "Karachi", "Lahore", "Islamabad", "Peshawar",
        "Quetta", "Multan", "Faisalabad"
    ]

    for city in cities:
        G.add_node(city)

    # Create edges ensuring connectivity
    edges = [
        ("Karachi", "Hyderabad", 150),
        ("Karachi", "Quetta", 680),
        ("Lahore", "Islamabad", 380),
        ("Lahore", "Faisalabad", 130),
        ("Lahore", "Multan", 340),
        ("Islamabad", "Peshawar", 170),
        ("Islamabad", "Lahore", 380),
        ("Faisalabad", "Multan", 135),
        ("Multan", "Quetta", 480),
        ("Peshawar", "Islamabad", 170),
        ("Quetta", "Multan", 480),
        ("Multan", "Lahore", 340),
        ("Karachi", "Multan", 900),
        ("Faisalabad", "Islamabad", 300),
        ("Karachi", "Lahore", 1200),
    ]

    for u, v, distance in edges:
        if u in cities and v in cities:
            speed = random.randint(70, 100)
            G.add_edge(
                u, v,
                distance=distance,
                time=distance / speed
            )

    return G