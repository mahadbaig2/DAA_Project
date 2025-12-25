import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import networkx as nx


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth in kilometers"""
    R = 6371  # Earth's radius in km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def create_comprehensive_aviation_network():
    """Create a comprehensive aviation network with major global airports"""

    # Major international airports with real coordinates
    airports_data = {
        'iata': [
            'JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'MIA', 'SFO', 'SEA',  # USA
            'LHR', 'CDG', 'FRA', 'AMS', 'MAD', 'FCO', 'ZRH', 'VIE',  # Europe
            'DXB', 'DOH', 'AUH', 'JED', 'CAI', 'IST',  # Middle East
            'SIN', 'HKG', 'NRT', 'ICN', 'PVG', 'PEK', 'BKK', 'KUL',  # Asia
            'DEL', 'BOM', 'BLR', 'KHI', 'LHE', 'ISB',  # South Asia
            'SYD', 'MEL', 'AKL',  # Oceania
            'YYZ', 'YVR',  # Canada
            'GRU', 'EZE', 'SCL', 'BOG',  # South America
            'JNB', 'CPT', 'ADD'  # Africa
        ],
        'name': [
            'John F Kennedy Intl', 'Los Angeles Intl', 'O\'Hare Intl', 'Dallas/Fort Worth Intl',
            'Hartsfield-Jackson Atlanta Intl', 'Miami Intl', 'San Francisco Intl', 'Seattle-Tacoma Intl',
            'London Heathrow', 'Charles de Gaulle', 'Frankfurt', 'Amsterdam Schiphol',
            'Madrid Barajas', 'Rome Fiumicino', 'Zurich', 'Vienna Intl',
            'Dubai Intl', 'Hamad Intl', 'Abu Dhabi Intl', 'King Abdulaziz Intl', 'Cairo Intl', 'Istanbul',
            'Singapore Changi', 'Hong Kong Intl', 'Tokyo Narita', 'Incheon Intl',
            'Shanghai Pudong', 'Beijing Capital', 'Bangkok Suvarnabhumi', 'Kuala Lumpur Intl',
            'Indira Gandhi Intl', 'Chhatrapati Shivaji', 'Kempegowda Intl',
            'Jinnah Intl', 'Allama Iqbal Intl', 'Islamabad Intl',
            'Sydney Kingsford Smith', 'Melbourne', 'Auckland',
            'Toronto Pearson', 'Vancouver Intl',
            'São Paulo–Guarulhos', 'Ministro Pistarini', 'Santiago Intl', 'El Dorado Intl',
            'OR Tambo Intl', 'Cape Town Intl', 'Addis Ababa Bole'
        ],
        'city': [
            'New York', 'Los Angeles', 'Chicago', 'Dallas', 'Atlanta', 'Miami', 'San Francisco', 'Seattle',
            'London', 'Paris', 'Frankfurt', 'Amsterdam', 'Madrid', 'Rome', 'Zurich', 'Vienna',
            'Dubai', 'Doha', 'Abu Dhabi', 'Jeddah', 'Cairo', 'Istanbul',
            'Singapore', 'Hong Kong', 'Tokyo', 'Seoul', 'Shanghai', 'Beijing', 'Bangkok', 'Kuala Lumpur',
            'Delhi', 'Mumbai', 'Bangalore', 'Karachi', 'Lahore', 'Islamabad',
            'Sydney', 'Melbourne', 'Auckland',
            'Toronto', 'Vancouver',
            'São Paulo', 'Buenos Aires', 'Santiago', 'Bogotá',
            'Johannesburg', 'Cape Town', 'Addis Ababa'
        ],
        'country': [
            'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA',
            'UK', 'France', 'Germany', 'Netherlands', 'Spain', 'Italy', 'Switzerland', 'Austria',
            'UAE', 'Qatar', 'UAE', 'Saudi Arabia', 'Egypt', 'Turkey',
            'Singapore', 'Hong Kong', 'Japan', 'South Korea', 'China', 'China', 'Thailand', 'Malaysia',
            'India', 'India', 'India', 'Pakistan', 'Pakistan', 'Pakistan',
            'Australia', 'Australia', 'New Zealand',
            'Canada', 'Canada',
            'Brazil', 'Argentina', 'Chile', 'Colombia',
            'South Africa', 'South Africa', 'Ethiopia'
        ],
        'lat': [
            40.6413, 33.9416, 41.9742, 32.8998, 33.6407, 25.7959, 37.6213, 47.4502,
            51.4700, 49.0097, 50.0379, 52.3105, 40.4983, 41.8003, 47.4582, 48.1103,
            25.2532, 25.2731, 24.4330, 21.6796, 30.1219, 41.2753,
            1.3644, 22.3080, 35.7720, 37.4602, 31.1443, 40.0799, 13.6900, 2.7456,
            28.5562, 19.0895, 13.1979, 24.9056, 31.5214, 33.6169,
            -33.9461, -37.6690, -37.0082,
            43.6777, 49.1967,
            -23.4356, -34.8222, -33.3930, 4.7016,
            -26.1392, -33.9715, 8.9779
        ],
        'lon': [
            -73.7781, -118.4085, -87.9073, -97.0403, -84.4277, -80.2870, -122.3790, -122.3088,
            -0.4543, 2.5479, 8.5622, 4.7683, -3.5676, 12.2389, 8.5492, 16.5697,
            55.3657, 51.6080, 54.6511, 39.1565, 31.4056, 28.7519,
            103.9915, 113.9185, 140.3929, 126.4407, 121.8083, 116.6031, 100.7501, 101.7099,
            77.1000, 72.8656, 77.7063, 67.1608, 74.4036, 73.0992,
            151.1772, 144.8410, 174.7850,
            -79.6248, -123.1815,
            -46.4731, -58.5358, -70.7859, -74.1469,
            28.2460, 18.6021, 38.7997
        ]
    }

    airports_df = pd.DataFrame(airports_data)

    # Create routes between major hubs
    # Format: (source, destination)
    major_routes = [
        # Trans-Atlantic
        ('JFK', 'LHR'), ('JFK', 'CDG'), ('JFK', 'FRA'), ('JFK', 'AMS'), ('JFK', 'MAD'),
        ('LAX', 'LHR'), ('ORD', 'LHR'), ('ORD', 'FRA'), ('ATL', 'LHR'), ('ATL', 'CDG'),
        ('MIA', 'MAD'), ('SFO', 'LHR'), ('SFO', 'FRA'),

        # Trans-Pacific
        ('LAX', 'NRT'), ('LAX', 'ICN'), ('LAX', 'HKG'), ('LAX', 'SYD'),
        ('SFO', 'NRT'), ('SFO', 'SIN'), ('SFO', 'HKG'), ('SEA', 'NRT'),
        ('ORD', 'NRT'), ('DFW', 'ICN'),

        # Europe Internal
        ('LHR', 'CDG'), ('LHR', 'FRA'), ('LHR', 'AMS'), ('LHR', 'MAD'), ('LHR', 'FCO'),
        ('CDG', 'FRA'), ('CDG', 'AMS'), ('FRA', 'ZRH'), ('FRA', 'VIE'),

        # Middle East Hubs
        ('LHR', 'DXB'), ('CDG', 'DXB'), ('FRA', 'DXB'), ('DXB', 'DOH'), ('DXB', 'AUH'),
        ('DXB', 'JED'), ('DXB', 'CAI'), ('IST', 'DXB'), ('IST', 'DOH'),

        # Middle East to Asia
        ('DXB', 'SIN'), ('DXB', 'HKG'), ('DXB', 'BKK'), ('DXB', 'KUL'),
        ('DXB', 'DEL'), ('DXB', 'BOM'), ('DOH', 'SIN'), ('DOH', 'HKG'),

        # Asia Internal
        ('SIN', 'HKG'), ('SIN', 'BKK'), ('SIN', 'KUL'), ('HKG', 'NRT'),
        ('HKG', 'ICN'), ('HKG', 'PVG'), ('HKG', 'PEK'), ('NRT', 'ICN'),
        ('BKK', 'SIN'), ('KUL', 'BKK'),

        # South Asia
        ('DEL', 'BOM'), ('DEL', 'BLR'), ('DEL', 'DXB'), ('BOM', 'SIN'),
        ('DEL', 'KHI'), ('DEL', 'LHE'), ('KHI', 'DXB'), ('LHE', 'DXB'),
        ('KHI', 'ISB'), ('ISB', 'DXB'), ('ISB', 'LHR'),

        # Oceania
        ('SYD', 'SIN'), ('SYD', 'HKG'), ('SYD', 'AKL'), ('MEL', 'SIN'),
        ('SYD', 'LAX'), ('AKL', 'LAX'),

        # North America Internal
        ('JFK', 'LAX'), ('JFK', 'ORD'), ('JFK', 'MIA'), ('LAX', 'SFO'),
        ('ORD', 'DFW'), ('ATL', 'MIA'), ('YYZ', 'JFK'), ('YVR', 'LAX'),

        # South America
        ('MIA', 'GRU'), ('MIA', 'BOG'), ('ATL', 'GRU'), ('JFK', 'GRU'),
        ('GRU', 'EZE'), ('GRU', 'SCL'), ('EZE', 'SCL'), ('BOG', 'GRU'),

        # Africa
        ('LHR', 'JNB'), ('CDG', 'JNB'), ('DXB', 'JNB'), ('JNB', 'CPT'),
        ('CAI', 'JNB'), ('ADD', 'DXB'), ('ADD', 'CAI'),

        # Europe to Middle East
        ('LHR', 'IST'), ('CDG', 'IST'), ('FRA', 'IST'), ('IST', 'CAI'),
    ]

    routes_df = pd.DataFrame({
        'source_airport': [r[0] for r in major_routes],
        'dest_airport': [r[1] for r in major_routes]
    })

    return airports_df, routes_df


def build_network_graph(airports_df, routes_df):
    """Build network graph with multi-weight edges"""
    G = nx.DiGraph()

    # Add airports as nodes
    for _, airport in airports_df.iterrows():
        G.add_node(
            airport['iata'],
            name=airport['name'],
            city=airport['city'],
            country=airport['country'],
            lat=airport['lat'],
            lon=airport['lon']
        )

    # Add bidirectional routes
    for _, route in routes_df.iterrows():
        src = route['source_airport']
        dst = route['dest_airport']

        if src in G.nodes and dst in G.nodes:
            src_node = G.nodes[src]
            dst_node = G.nodes[dst]

            # Calculate distance
            distance = haversine_distance(
                src_node['lat'], src_node['lon'],
                dst_node['lat'], dst_node['lon']
            )

            # Calculate time (average cruise speed: 800 km/h)
            flight_time = distance / 800

            # Calculate cost with complexity factors
            base_cost = distance * 0.15  # Base: $0.15 per km

            # Add variability factors (seeded for consistency)
            np.random.seed(hash(src + dst) % 2 ** 32)
            demand_factor = np.random.uniform(0.8, 1.6)
            fuel_surcharge = np.random.uniform(80, 250)
            airport_fees = np.random.uniform(50, 180)

            cost = (base_cost * demand_factor) + fuel_surcharge + airport_fees

            # Add layover penalties
            layover_time = np.random.choice([0, 1.5, 3, 5], p=[0.5, 0.3, 0.15, 0.05])
            total_time = flight_time + layover_time

            # Add edge in both directions with slightly different attributes
            G.add_edge(
                src, dst,
                distance=round(distance, 2),
                time=round(total_time, 2),
                cost=round(cost, 2),
                layover=layover_time,
                fuel_surcharge=round(fuel_surcharge, 2)
            )

            # Reverse direction with different cost/time
            np.random.seed(hash(dst + src) % 2 ** 32)
            reverse_demand = np.random.uniform(0.8, 1.6)
            reverse_cost = (base_cost * reverse_demand) + np.random.uniform(80, 250) + np.random.uniform(50, 180)
            reverse_layover = np.random.choice([0, 1.5, 3, 5], p=[0.5, 0.3, 0.15, 0.05])
            reverse_time = flight_time + reverse_layover

            G.add_edge(
                dst, src,
                distance=round(distance, 2),
                time=round(reverse_time, 2),
                cost=round(reverse_cost, 2),
                layover=reverse_layover,
                fuel_surcharge=round(np.random.uniform(80, 250), 2)
            )

    return G


def load_aviation_data():
    """Load aviation data - uses built-in comprehensive dataset"""
    return create_comprehensive_aviation_network()


def get_network_statistics(G):
    """Calculate network statistics"""
    if G.number_of_edges() == 0:
        return {
            'total_airports': G.number_of_nodes(),
            'total_routes': 0,
            'avg_distance': 0,
            'avg_cost': 0,
            'avg_time': 0
        }

    return {
        'total_airports': G.number_of_nodes(),
        'total_routes': G.number_of_edges(),
        'avg_distance': round(np.mean([d['distance'] for _, _, d in G.edges(data=True)]), 2),
        'avg_cost': round(np.mean([d['cost'] for _, _, d in G.edges(data=True)]), 2),
        'avg_time': round(np.mean([d['time'] for _, _, d in G.edges(data=True)]), 2)
    }