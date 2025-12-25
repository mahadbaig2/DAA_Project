import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from network import create_transport_network
from evaluator import evaluate_algorithms
from metrics import calculate_metrics

st.set_page_config("Transport Network Optimization", layout="wide")
st.title("🚦 Transport Network Optimization & Algorithm Comparison")

# Create consistent network
if 'graph' not in st.session_state:
    st.session_state.graph = create_transport_network()

graph = st.session_state.graph
cities = list(graph.nodes)

col1, col2 = st.columns(2)
with col1:
    src = st.selectbox("Source City", cities, index=0)
with col2:
    dst = st.selectbox("Destination City", cities, index=1 if len(cities) > 1 else 0)

if st.button("🔍 Run All Algorithms", type="primary"):
    with st.spinner("Computing shortest paths..."):
        results = evaluate_algorithms(graph, src, dst)

    # Network Visualization
    st.subheader("🗺️ Transport Network & Algorithm Paths")

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # Define colors for each algorithm
    algo_colors = {
        "Dijkstra": "#FF6B6B",
        "Bellman-Ford": "#4ECDC4",
        "Floyd-Warshall": "#95E1D3"
    }

    # Get positions for consistent layout
    pos = nx.spring_layout(graph, seed=42, k=2)

    # Plot 1: Full Network
    ax = axes[0, 0]
    nx.draw_networkx_nodes(graph, pos, node_color='lightblue',
                           node_size=800, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=8, ax=ax)
    nx.draw_networkx_edges(graph, pos, edge_color='gray',
                           arrows=True, arrowsize=15, ax=ax, alpha=0.3)

    # Add edge labels with distances
    edge_labels = {(u, v): f"{d['distance']}km"
                   for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels,
                                 font_size=6, ax=ax)

    ax.set_title("Complete Transport Network", fontsize=14, fontweight='bold')
    ax.axis('off')

    # Plot algorithm-specific paths
    algo_names = ["Dijkstra", "Bellman-Ford", "Floyd-Warshall"]
    positions = [(0, 1), (1, 0), (1, 1)]

    for idx, (algo_name, pos_idx) in enumerate(zip(algo_names, positions)):
        ax = axes[pos_idx]
        data = results[algo_name]
        path = data["path"]

        # Draw base network
        nx.draw_networkx_nodes(graph, pos, node_color='lightgray',
                               node_size=600, ax=ax, alpha=0.5)
        nx.draw_networkx_labels(graph, pos, font_size=7, ax=ax)
        nx.draw_networkx_edges(graph, pos, edge_color='lightgray',
                               arrows=True, arrowsize=10, ax=ax, alpha=0.2)

        # Highlight path if it exists
        if path and len(path) > 1:
            # Highlight nodes in path
            nx.draw_networkx_nodes(graph, pos, nodelist=path,
                                   node_color=algo_colors[algo_name],
                                   node_size=800, ax=ax)

            # Highlight edges in path
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges,
                                   edge_color=algo_colors[algo_name],
                                   arrows=True, arrowsize=20, width=3, ax=ax)

            # Highlight source and destination
            nx.draw_networkx_nodes(graph, pos, nodelist=[src],
                                   node_color='green', node_size=900, ax=ax)
            nx.draw_networkx_nodes(graph, pos, nodelist=[dst],
                                   node_color='red', node_size=900, ax=ax)

        title = f"{algo_name}\nDistance: {data['distance']:.1f}km | Time: {data['time'] * 1000:.2f}ms"
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.axis('off')

    plt.tight_layout()
    st.pyplot(fig)

    # Algorithm Comparison Table
    st.subheader("📊 Detailed Algorithm Comparison")

    cols = st.columns(3)

    for idx, (algo, data) in enumerate(results.items()):
        with cols[idx]:
            st.markdown(f"### {algo}")
            st.markdown(f"**⏱️ Execution Time:** `{data['time'] * 1000:.4f} ms`")
            st.markdown(f"**📏 Total Distance:** `{data['distance']:.1f} km`")

            if isinstance(data["path"], list) and len(data["path"]) > 0:
                path_str = " ➜ ".join(data["path"])
                st.markdown(f"**🛣️ Path:** {path_str}")
                st.markdown(f"**🏙️ Cities Visited:** `{len(data['path'])}`")

                # Calculate detailed metrics
                metrics = calculate_metrics(data["path"], graph)
                st.divider()
                for k, v in metrics.items():
                    st.metric(k, v)
            else:
                st.warning("No path found")

    # Best Algorithm Summary
    st.subheader("🏆 Performance Summary")

    valid_results = {k: v for k, v in results.items()
                     if isinstance(v["path"], list) and len(v["path"]) > 0}

    if valid_results:
        fastest = min(valid_results.items(), key=lambda x: x[1]["time"])
        shortest = min(valid_results.items(), key=lambda x: x[1]["distance"])

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**Fastest Execution:** {fastest[0]} ({fastest[1]['time'] * 1000:.4f}ms)")
        with col2:
            st.info(f"**Shortest Path:** {shortest[0]} ({shortest[1]['distance']:.1f}km)")

        # Algorithm characteristics
        st.markdown("### 🔬 Algorithm Characteristics")
        st.markdown("""
        - **Dijkstra**: Best for single-source shortest path with non-negative weights. Very efficient.
        - **Bellman-Ford**: Handles negative weights and detects negative cycles. Slower than Dijkstra.
        - **Floyd-Warshall**: Computes all-pairs shortest paths. Good for small graphs, overkill for single queries.
        """)
    else:
        st.error("No valid paths found between selected cities")

# Network Statistics in Sidebar
with st.sidebar:
    st.header("📈 Network Statistics")
    st.metric("Total Cities", len(graph.nodes))
    st.metric("Total Routes", len(graph.edges))
    st.metric("Avg. Route Distance",
              f"{sum(d['distance'] for _, _, d in graph.edges(data=True)) / len(graph.edges):.1f} km")

    if st.button("🔄 Regenerate Network"):
        st.session_state.graph = create_transport_network()
        st.rerun()