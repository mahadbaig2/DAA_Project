import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from network import create_transport_network
from evaluator import evaluate_algorithms
from metrics import calculate_metrics

st.set_page_config("Transport Network Optimization", layout="wide")
st.title("🚦 Transport Network Optimization & Algorithm Comparison")

graph = create_transport_network()
cities = list(graph.nodes)

src = st.selectbox("Source City", cities)
dst = st.selectbox("Destination City", cities)

if st.button("Run All Algorithms"):
    results = evaluate_algorithms(graph, src, dst)

    st.subheader("📊 Algorithm Comparison")

    for algo, data in results.items():
        st.markdown(f"### {algo}")
        st.write("Execution Time:", round(data["time"], 6), "seconds")

        if isinstance(data["path"], list):
            st.write("Path:", " ➜ ".join(data["path"]))
            metrics = calculate_metrics(data["path"], graph)
            for k, v in metrics.items():
                st.metric(k, v)
        else:
            st.write("Path:", data["path"])

    st.subheader("🏆 Best Algorithm (Practical Verdict)")
    best = min(results.items(), key=lambda x: x[1]["time"])
    st.success(f"{best[0]} is fastest for this network")
