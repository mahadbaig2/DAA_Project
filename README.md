# ✈️ Global Aviation Route Optimizer

Interactive web application comparing **Dijkstra**, **Bellman-Ford**, and **Floyd-Warshall** algorithms on real-world aviation networks with geographic map visualization.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Features

- **Real Aviation Data**: 47+ major international airports with 100+ routes
- **Multi-Objective Optimization**: Each algorithm optimizes for different criteria (distance/cost/time)
- **Interactive Maps**: Folium-based geographic visualization with color-coded routes
- **Performance Comparison**: Side-by-side metrics, charts, and execution time analysis
- **Academic Ready**: Complete complexity analysis for DAA course projects

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/aviation-route-optimizer.git
cd aviation-route-optimizer

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run main.py
```

Visit `http://localhost:8501` in your browser.

## 📊 Algorithm Overview

| Algorithm | Optimizes | Time Complexity | Use Case |
|-----------|-----------|-----------------|----------|
| **Dijkstra** | Shortest Distance | O((V+E) log V) | Direct routes, fuel efficiency |
| **Bellman-Ford** | Cheapest Cost | O(V×E) | Budget travel, dynamic pricing |
| **Floyd-Warshall** | Fastest Time | O(V³) | Time-critical, multi-hop optimization |

## 🗺️ Example Routes

Try these routes to see different algorithm behaviors:
- **JFK → LHR**: Trans-Atlantic (direct vs. hub routing)
- **LAX → SYD**: Long-haul Pacific (multiple path options)
- **KHI → LHR**: Pakistan to UK (Middle East hub comparison)
- **ORD → HKG**: Complex multi-hop route

## 📁 Project Structure

```
aviation-route-optimizer/
├── main.py                    # Streamlit web application
├── data_loader.py             # Network construction & airport data
├── aviation_algorithms.py     # Algorithm implementations
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎓 Educational Value

Perfect for:
- ✅ Design & Analysis of Algorithms courses
- ✅ Graph theory projects
- ✅ Algorithm comparison studies
- ✅ Viva defense demonstrations
- ✅ Portfolio showcase

## 📸 Highlights

**Interactive Map View**
- Color-coded routes per algorithm
- Real-time path visualization
- Airport markers with tooltips

**Comparison Dashboard**
- Metric tables and charts
- Performance analysis
- Winner highlights

**Academic Analysis**
- Complexity breakdown
- Trade-off discussions
- Viva Q&A preparation

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Folium, Plotly
- **Graph Processing**: NetworkX
- **Data**: Pandas, NumPy

## 📝 Key Insights

**Why different results?**

Each algorithm uses different edge weights:
- Dijkstra: `weight = distance` (km)
- Bellman-Ford: `weight = cost + layover_penalty` ($)
- Floyd-Warshall: `weight = flight_time + layover_hours` (hrs)

This ensures genuinely different optimal paths, demonstrating multi-objective optimization trade-offs.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional airports and routes
- Real-time flight data integration
- More optimization algorithms (A*, Yen's K-shortest paths)
- Enhanced cost models (seasonal pricing, airline alliances)

## 🙏 Acknowledgments

- Airport coordinates and routing inspired by real aviation networks
- Built for educational purposes in Design and Analysis of Algorithms coursework

## 📧 Contact

For questions or suggestions, please open an issue or submit a pull request.

---

**⭐ Star this repo if you find it helpful for your studies!**
