import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import load_aviation_data, build_network_graph, get_network_statistics
from aviation_algorithms import compare_all_algorithms

# Page configuration
st.set_page_config(
    page_title="✈️ Global Aviation Route Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .algo-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .dijkstra-badge {
        background-color: #EF4444;
        color: white;
    }
    .bellman-badge {
        background-color: #10B981;
        color: white;
    }
    .floyd-badge {
        background-color: #3B82F6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">✈️ Global Aviation Route Optimizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Compare Dijkstra, Bellman-Ford & Floyd-Warshall on Real Flight Data</div>',
            unsafe_allow_html=True)

# Initialize session state
if 'graph' not in st.session_state:
    with st.spinner("🌍 Loading global aviation data..."):
        airports_df, routes_df = load_aviation_data()
        st.session_state.airports_df = airports_df
        st.session_state.routes_df = routes_df
        st.session_state.graph = build_network_graph(airports_df, routes_df)

graph = st.session_state.graph
airports_df = st.session_state.airports_df

# Sidebar
with st.sidebar:
    st.header("🎯 Route Configuration")

    # Network stats
    stats = get_network_statistics(graph)
    st.metric("Total Airports", stats['total_airports'])
    st.metric("Total Routes", stats['total_routes'])
    st.metric("Avg Distance", f"{stats['avg_distance']} km")

    st.divider()

    # Airport selection
    available_airports = sorted(list(graph.nodes()))

    source_airport = st.selectbox(
        "🛫 Departure Airport",
        available_airports,
        index=available_airports.index('JFK') if 'JFK' in available_airports else 0
    )

    destination_airport = st.selectbox(
        "🛬 Arrival Airport",
        available_airports,
        index=available_airports.index('LHR') if 'LHR' in available_airports else (
            1 if len(available_airports) > 1 else 0)
    )

    st.divider()

    # Display airport info
    if source_airport in graph.nodes:
        src_info = graph.nodes[source_airport]
        st.markdown(f"**{src_info['name']}**")
        st.caption(f"{src_info['city']}, {src_info['country']}")

    st.markdown("✈️ ➜")

    if destination_airport in graph.nodes:
        dst_info = graph.nodes[destination_airport]
        st.markdown(f"**{dst_info['name']}**")
        st.caption(f"{dst_info['city']}, {dst_info['country']}")

    st.divider()

    run_button = st.button("🚀 Compare All Algorithms", type="primary", use_container_width=True)

    st.divider()

    st.markdown("### 📚 Algorithm Info")
    st.markdown("""
    <div style="font-size: 0.85rem;">
    <span class="algo-badge dijkstra-badge">Dijkstra</span><br>
    Shortest Distance<br><br>

    <span class="algo-badge bellman-badge">Bellman-Ford</span><br>
    Cheapest Cost<br><br>

    <span class="algo-badge floyd-badge">Floyd-Warshall</span><br>
    Fastest Time
    </div>
    """, unsafe_allow_html=True)

# Main content
if run_button and source_airport != destination_airport:
    with st.spinner("🔍 Running all algorithms..."):
        results = compare_all_algorithms(graph, source_airport, destination_airport)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Interactive Map", "📊 Comparison Dashboard", "🎓 Academic Analysis"])

    with tab1:
        st.subheader("Global Route Visualization")

        # Create base map
        src_node = graph.nodes[source_airport]
        dst_node = graph.nodes[destination_airport]

        center_lat = (src_node['lat'] + dst_node['lat']) / 2
        center_lon = (src_node['lon'] + dst_node['lon']) / 2

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=3,
            tiles='CartoDB positron'
        )

        # Add all routes (faded)
        for u, v, data in graph.edges(data=True):
            u_node = graph.nodes[u]
            v_node = graph.nodes[v]

            folium.PolyLine(
                locations=[[u_node['lat'], u_node['lon']], [v_node['lat'], v_node['lon']]],
                color='gray',
                weight=1,
                opacity=0.2
            ).add_to(m)

        # Color mapping
        colors = {
            'Dijkstra': '#EF4444',
            'Bellman-Ford': '#10B981',
            'Floyd-Warshall': '#3B82F6'
        }

        # Add algorithm-specific routes
        for algo_name, result in results.items():
            if result and result.path and len(result.path) > 1:
                path_coords = []
                for airport in result.path:
                    node = graph.nodes[airport]
                    path_coords.append([node['lat'], node['lon']])

                folium.PolyLine(
                    locations=path_coords,
                    color=colors[algo_name],
                    weight=4,
                    opacity=0.8,
                    popup=f"{algo_name}: {result.details['optimization_target']}"
                ).add_to(m)

        # Add airport markers
        for airport in graph.nodes():
            node = graph.nodes[airport]

            if airport == source_airport:
                icon = folium.Icon(color='green', icon='plane-departure', prefix='fa')
            elif airport == destination_airport:
                icon = folium.Icon(color='red', icon='plane-arrival', prefix='fa')
            else:
                icon = folium.Icon(color='lightgray', icon='plane', prefix='fa', icon_size=(10, 10))

            folium.Marker(
                location=[node['lat'], node['lon']],
                popup=f"<b>{node['name']}</b><br>{node['city']}, {node['country']}",
                tooltip=airport,
                icon=icon
            ).add_to(m)

        # Display map
        st_folium(m, width=1400, height=600)

        # Legend
        st.markdown("### 🎨 Route Legend")
        cols = st.columns(3)

        for idx, (algo_name, color) in enumerate(colors.items()):
            with cols[idx]:
                result = results[algo_name]
                if result and result.path:
                    target = result.details['optimization_target']
                    st.markdown(f"""
                    <div style="background-color: {color}; padding: 10px; border-radius: 5px; color: white; text-align: center;">
                        <b>{algo_name}</b><br>
                        {target}<br>
                        {len(result.path) - 1} hops
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.subheader("📊 Detailed Performance Comparison")

        # Create comparison table
        comparison_data = []

        for algo_name, result in results.items():
            if result and result.path:
                comparison_data.append({
                    'Algorithm': algo_name,
                    'Target': result.details['optimization_target'],
                    'Distance (km)': result.details['total_distance'],
                    'Time (hrs)': result.details['total_time'],
                    'Cost ($)': result.details['total_cost'],
                    'Hops': result.details['hops'],
                    'Execution (ms)': round(result.execution_time * 1000, 4)
                })

        df = pd.DataFrame(comparison_data)

        # Display styled table
        st.dataframe(
            df.style.background_gradient(subset=['Distance (km)', 'Time (hrs)', 'Cost ($)'], cmap='RdYlGn_r')
            .format({
                'Distance (km)': '{:.1f}',
                'Time (hrs)': '{:.2f}',
                'Cost ($)': '{:.2f}',
                'Execution (ms)': '{:.4f}'
            }),
            use_container_width=True
        )

        # Visual comparisons
        col1, col2 = st.columns(2)

        with col1:
            # Distance comparison
            fig1 = px.bar(
                df, x='Algorithm', y='Distance (km)',
                title='Distance Comparison',
                color='Algorithm',
                color_discrete_map={
                    'Dijkstra': '#EF4444',
                    'Bellman-Ford': '#10B981',
                    'Floyd-Warshall': '#3B82F6'
                }
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Cost comparison
            fig3 = px.bar(
                df, x='Algorithm', y='Cost ($)',
                title='Cost Comparison',
                color='Algorithm',
                color_discrete_map={
                    'Dijkstra': '#EF4444',
                    'Bellman-Ford': '#10B981',
                    'Floyd-Warshall': '#3B82F6'
                }
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            # Time comparison
            fig2 = px.bar(
                df, x='Algorithm', y='Time (hrs)',
                title='Travel Time Comparison',
                color='Algorithm',
                color_discrete_map={
                    'Dijkstra': '#EF4444',
                    'Bellman-Ford': '#10B981',
                    'Floyd-Warshall': '#3B82F6'
                }
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Execution time
            fig4 = px.bar(
                df, x='Algorithm', y='Execution (ms)',
                title='Algorithm Execution Time',
                color='Algorithm',
                color_discrete_map={
                    'Dijkstra': '#EF4444',
                    'Bellman-Ford': '#10B981',
                    'Floyd-Warshall': '#3B82F6'
                }
            )
            st.plotly_chart(fig4, use_container_width=True)

        # Winner boxes
        st.markdown("### 🏆 Performance Winners")
        cols = st.columns(4)

        with cols[0]:
            shortest_dist = df.loc[df['Distance (km)'].idxmin()]
            st.success(f"**Shortest Distance**\n\n{shortest_dist['Algorithm']}\n\n{shortest_dist['Distance (km)']} km")

        with cols[1]:
            fastest_time = df.loc[df['Time (hrs)'].idxmin()]
            st.info(f"**Fastest Route**\n\n{fastest_time['Algorithm']}\n\n{fastest_time['Time (hrs)']} hrs")

        with cols[2]:
            cheapest = df.loc[df['Cost ($)'].idxmin()]
            st.warning(f"**Cheapest Route**\n\n{cheapest['Algorithm']}\n\n${cheapest['Cost ($)']}")

        with cols[3]:
            fastest_algo = df.loc[df['Execution (ms)'].idxmin()]
            st.error(f"**Fastest Algorithm**\n\n{fastest_algo['Algorithm']}\n\n{fastest_algo['Execution (ms)']} ms")

    with tab3:
        st.subheader("🎓 Academic Analysis: Algorithm Paradigms")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### Algorithm Characteristics")

            for algo_name, result in results.items():
                if result and result.path:
                    details = result.details

                    with st.expander(f"**{algo_name}** - {details['optimization_target']}", expanded=True):
                        st.markdown(f"**Paradigm:** {details['algorithm_type']}")

                        if algo_name == 'Dijkstra':
                            st.markdown("""
                            **Time Complexity:** O((V + E) log V)  
                            **Space Complexity:** O(V)  
                            **Approach:** Greedy - always expands nearest node  
                            **Best For:** Single-source, non-negative weights  
                            **Limitation:** Cannot handle negative weights
                            """)
                        elif algo_name == 'Bellman-Ford':
                            st.markdown("""
                            **Time Complexity:** O(V × E)  
                            **Space Complexity:** O(V)  
                            **Approach:** Dynamic Programming - relaxes all edges  
                            **Best For:** Negative weights, cycle detection  
                            **Advantage:** Handles cost penalties and adjustments
                            """)
                        else:
                            st.markdown("""
                            **Time Complexity:** O(V³)  
                            **Space Complexity:** O(V²)  
                            **Approach:** All-pairs - precomputes global solution  
                            **Best For:** Dense graphs, multiple queries  
                            **Trade-off:** High initial cost, fast lookups
                            """)

                        st.markdown(
                            f"**Route:** {' → '.join(result.path[:3])}{'...' if len(result.path) > 3 else ''} → {result.path[-1]}")

        with col2:
            st.markdown("### Why Different Results?")

            st.markdown("""
            Each algorithm optimizes a **different objective function**:

            1. **Dijkstra (Distance)**
               - Minimizes geographical distance
               - Ignores cost variations
               - May include expensive routes

            2. **Bellman-Ford (Cost)**
               - Incorporates ticket prices
               - Accounts for layover penalties
               - Handles dynamic pricing

            3. **Floyd-Warshall (Time)**
               - Optimizes total travel time
               - Considers cruise speed + layovers
               - Global perspective on connections

            **Key Insight:** Real-world optimization requires multi-objective analysis.
            No single "best" algorithm exists—choice depends on priorities.
            """)

            st.markdown("### 📝 Viva Defense Points")
            st.info("""
            **Q: Why do results differ?**  
            A: Each algorithm uses different weight functions (distance/cost/time) 
            and edge attributes (layover penalties, fuel surcharges).

            **Q: Which is most efficient?**  
            A: Dijkstra for this scale (O(E log V)), but Bellman-Ford handles 
            more complex cost models with penalties.

            **Q: When use Floyd-Warshall?**  
            A: When needing ALL pairs of shortest paths, or with frequent queries 
            on the same network (amortized efficiency).
            """)

elif run_button:
    st.warning("⚠️ Please select different airports for source and destination")

else:
    # Initial state - show network overview
    st.info("👆 Select airports from the sidebar and click 'Compare All Algorithms' to begin")

    # Show sample map
    st.subheader("🌍 Global Aviation Network Overview")

    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

    for airport in list(graph.nodes())[:50]:  # Show first 50 airports
        node = graph.nodes[airport]
        folium.CircleMarker(
            location=[node['lat'], node['lon']],
            radius=3,
            color='blue',
            fill=True,
            popup=f"{node['name']}<br>{node['city']}, {node['country']}",
            tooltip=airport
        ).add_to(m)

    st_folium(m, width=1400, height=500)