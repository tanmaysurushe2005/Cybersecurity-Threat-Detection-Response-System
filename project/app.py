"""
Streamlit dashboard for the Cybersecurity Threat Detection & Response System.
Provides interactive visualization and control of network simulation and algorithms.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time
from typing import Dict, List, Tuple, Optional
import threading

import sys
import os

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import from project package
from project.core.graph import NetworkGraph
from project.core.simulation import ThreatSimulator
from project.core.algorithm_engine import AlgorithmEngine
from project.core.step_tracker import StepTracker
from project.utils.helpers import format_execution_time


# Page configuration
st.set_page_config(
    page_title="Cybersecurity Threat Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .threat-high {
        color: #ff0000;
        font-weight: bold;
    }
    .threat-medium {
        color: #ff9900;
        font-weight: bold;
    }
    .threat-low {
        color: #00cc00;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'network' not in st.session_state:
        st.session_state.network = None
    if 'threat_simulator' not in st.session_state:
        st.session_state.threat_simulator = None
    if 'algorithm_engine' not in st.session_state:
        st.session_state.algorithm_engine = None
    if 'current_algorithm' not in st.session_state:
        st.session_state.current_algorithm = None
    if 'algorithm_running' not in st.session_state:
        st.session_state.algorithm_running = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'algorithm_results' not in st.session_state:
        st.session_state.algorithm_results = {}
    if 'threat_history' not in st.session_state:
        st.session_state.threat_history = []
    if 'animation_speed' not in st.session_state:
        st.session_state.animation_speed = 1.0
    if 'is_playing' not in st.session_state:
        st.session_state.is_playing = False
    if 'last_play_time' not in st.session_state:
        st.session_state.last_play_time = 0


def create_network_visualization(graph: NetworkGraph, step_data: Optional[Dict] = None) -> go.Figure:
    """
    Create a Plotly visualization of the network graph.
    
    Args:
        graph: NetworkGraph object
        step_data: Optional step data for highlighting nodes
        
    Returns:
        Plotly Figure object
    """
    import networkx as nx
    
    # Create NetworkX graph for layout
    G = nx.Graph()
    
    # Add nodes
    for node_id in graph.get_all_nodes():
        G.add_node(node_id)
    
    # Add edges
    for source, target in graph.get_all_edges():
        G.add_edge(source, target)
    
    # Calculate layout
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    
    # Extract coordinates
    x_coords = []
    y_coords = []
    node_ids = []
    node_colors = []
    node_sizes = []
    
    for node_id in G.nodes():
        x, y = pos[node_id]
        x_coords.append(x)
        y_coords.append(y)
        node_ids.append(node_id)
        
        # Determine node color based on algorithm step data (if available)
        if step_data:
            visited_nodes = step_data.get('visited_nodes', [])
            current_node = step_data.get('current_node')
            
            # Color priority: Current (yellow) > Visited (red) > Unvisited (green)
            if node_id == current_node:
                node_colors.append('#FFFF00')  # Yellow for current
            elif node_id in visited_nodes:
                node_colors.append('#FF0000')  # Red for visited
            else:
                node_colors.append('#00CC00')  # Green for unvisited
        else:
            # No step data: use network's compromise status
            node_data = graph.get_node_data(node_id)
            if node_data.is_compromised:
                node_colors.append('#FF0000')  # Red for compromised
            else:
                node_colors.append('#00CC00')  # Green for normal
        
        # Size based on risk level
        node_data = graph.get_node_data(node_id)
        node_sizes.append(20 + node_data.risk_level * 30)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    
    for source, target in G.edges():
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        showlegend=False
    )
    
    # Create node trace
    node_trace = go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        text=node_ids,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='#000')
        ),
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title='Network Topology',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#f8f9fa',
        height=600
    )
    
    return fig


def render_network_panel():
    """Render the network visualization panel."""
    st.subheader("Network Visualization & Creation")
    
    # Network creation section
    if st.session_state.network is None:
        st.info("Create a network below to get started")
        
        with st.expander("Network Configuration", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                num_nodes = st.slider("Number of Nodes", 5, 100, 20, key="nn_num_nodes")
                topology = st.selectbox("Topology", ["random", "scale-free", "small-world"], key="nn_topology")
            
            with col2:
                st.write("")
                st.write("")
                if st.button("Create Network", key="nn_create_network", use_container_width=True):
                    with st.spinner("Creating network..."):
                        st.session_state.network = NetworkGraph(num_nodes, topology)
                        st.session_state.threat_simulator = ThreatSimulator(st.session_state.network)
                        st.session_state.algorithm_engine = AlgorithmEngine(st.session_state.network)
                        st.success(f"Network created: {num_nodes} nodes, {topology} topology")
                        st.rerun()
        
        return
    
    # Display visualization
    # Get step data if algorithm is running
    step_data = None
    if st.session_state.algorithm_running and st.session_state.current_algorithm:
        step_tracker = st.session_state.current_algorithm.step_tracker
        if step_tracker:
            step_history = step_tracker.get_all_steps()
            if step_history and st.session_state.current_step < len(step_history):
                step_data = step_history[st.session_state.current_step].__dict__
    
    # Create and display visualization
    fig = create_network_visualization(st.session_state.network, step_data)
    st.plotly_chart(fig, use_container_width=True, key="network_viz")
    
    # Display network metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = st.session_state.network.get_graph_metrics()
    
    with col1:
        st.metric("Nodes", metrics['num_nodes'])
    with col2:
        st.metric("Edges", metrics['num_edges'])
    with col3:
        st.metric("Density", f"{metrics['density']:.3f}")
    with col4:
        st.metric("Avg Degree", f"{metrics['avg_degree']:.2f}")
    
    # Reset button
    if st.button("Reset Network", key="reset_network"):
        st.session_state.network = None
        st.session_state.threat_simulator = None
        st.session_state.algorithm_engine = None
        st.session_state.algorithm_running = False
        st.rerun()


def render_control_panel():
    """Render the control panel for algorithm selection and execution."""
    st.subheader("Control Panel - Algorithm Execution")
    
    # Check if network exists
    if st.session_state.network is None:
        st.error("No network created yet!")
        st.info("Go to the **Network** tab to create a network first")
        return
    
    # Quick actions
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Network Status", "Active")
    with col2:
        if st.button("Reset All", key="reset_all_ctrl"):
            st.session_state.network = None
            st.session_state.threat_simulator = None
            st.session_state.algorithm_engine = None
            st.session_state.algorithm_running = False
            st.session_state.current_step = 0
            st.success("System reset - Go to Network tab to create a new network")
            st.rerun()
    
    # Algorithm selection
    st.write("---")
    st.write("**Select and Run Algorithm**")
    algorithm = st.selectbox(
        "Select Algorithm",
        ["BFS", "DFS", "Dijkstra", "Greedy", "TSP", "BranchAndBound"],
        key="algorithm_select"
    )
    
    # Algorithm-specific parameters
    st.write("**Algorithm Parameters**")
    
    if algorithm in ["BFS", "DFS"]:
        start_node = st.selectbox("Start Node", st.session_state.network.get_all_nodes(), key="start_node")
        if st.button("Run Algorithm", key="run_algo"):
            st.session_state.current_algorithm = st.session_state.algorithm_engine
            st.session_state.algorithm_running = True
            st.session_state.current_step = 0
            
            with st.spinner(f"Running {algorithm}..."):
                if algorithm == "BFS":
                    st.session_state.algorithm_engine.execute_bfs(start_node)
                else:
                    st.session_state.algorithm_engine.execute_dfs(start_node)
            
            st.success(f"{algorithm} completed")
    
    elif algorithm == "Dijkstra":
        col1, col2 = st.columns(2)
        with col1:
            start_node = st.selectbox("Start Node", st.session_state.network.get_all_nodes(), key="dijkstra_start")
        with col2:
            end_node = st.selectbox("End Node", st.session_state.network.get_all_nodes(), key="dijkstra_end")
        
        if st.button("Run Algorithm", key="run_dijkstra"):
            st.session_state.current_algorithm = st.session_state.algorithm_engine
            st.session_state.algorithm_running = True
            st.session_state.current_step = 0
            
            with st.spinner("Running Dijkstra..."):
                st.session_state.algorithm_engine.execute_dijkstra(start_node, end_node)
            
            st.success("Dijkstra completed")
    
    elif algorithm == "Greedy":
        budget = st.slider("Budget", 100, 10000, 1000, key="greedy_budget")
        
        if st.button("Run Algorithm", key="run_greedy"):
            st.session_state.current_algorithm = st.session_state.algorithm_engine
            st.session_state.algorithm_running = True
            st.session_state.current_step = 0
            
            threat_nodes = st.session_state.network.get_all_nodes()[:5]
            
            with st.spinner("Running Greedy..."):
                st.session_state.algorithm_engine.execute_greedy(threat_nodes, budget)
            
            st.success("Greedy completed")
    
    elif algorithm == "TSP":
        start_node = st.selectbox("Start Node", st.session_state.network.get_all_nodes(), key="tsp_start")
        
        if st.button("Run Algorithm", key="run_tsp"):
            st.session_state.current_algorithm = st.session_state.algorithm_engine
            st.session_state.algorithm_running = True
            st.session_state.current_step = 0
            
            with st.spinner("Running TSP..."):
                st.session_state.algorithm_engine.execute_tsp(start_node)
            
            st.success("TSP completed")
    
    elif algorithm == "BranchAndBound":
        budget = st.slider("Budget", 100, 10000, 1000, key="bb_budget")
        
        if st.button("Run Algorithm", key="run_bb"):
            st.session_state.current_algorithm = st.session_state.algorithm_engine
            st.session_state.algorithm_running = True
            st.session_state.current_step = 0
            
            threat_nodes = st.session_state.network.get_all_nodes()[:5]
            
            with st.spinner("Running Branch and Bound..."):
                st.session_state.algorithm_engine.execute_branch_and_bound(threat_nodes, budget)
            
            st.success("Branch and Bound completed")


def render_animation_panel():
    """Render the algorithm animation panel with network visualization."""
    st.subheader("Algorithm Animation")
    
    if not st.session_state.algorithm_running or st.session_state.current_algorithm is None:
        st.info("Run an algorithm from the Control Panel to see animation here")
        return
    
    step_tracker = st.session_state.current_algorithm.step_tracker
    total_steps = step_tracker.get_step_count()
    
    if total_steps == 0:
        st.warning("No steps recorded")
        return
    
    # Step navigation with slider only
    st.write("### Navigate Through Steps")
    st.session_state.current_step = st.slider(
        "Step",
        0, total_steps - 1,
        st.session_state.current_step,
        key="step_slider"
    )
    
    # Display current step info
    current_step_data = step_tracker.get_step(st.session_state.current_step)
    st.write(f"**Step {st.session_state.current_step + 1} of {total_steps}**")
    
    # MAIN LAYOUT: Two columns - Network visualization and Metrics
    viz_col, metrics_col = st.columns([2, 1])
    
    with viz_col:
        # Create network visualization with current step data
        step_data_dict = current_step_data.__dict__ if current_step_data else None
        fig = create_network_visualization(st.session_state.network, step_data_dict)
        st.plotly_chart(fig, use_container_width=True, key="animation_network_viz")
    
    with metrics_col:
        st.write("### Step Metrics")
        
        # Display metrics in a column format
        st.metric("Current Node", current_step_data.current_node or "N/A")
        st.metric("Visited Nodes", len(current_step_data.visited_nodes))
        st.metric("Frontier Nodes", len(current_step_data.frontier_nodes))
        st.metric("Cost", f"{current_step_data.cost:.2f}")
        
        # Additional info
        st.divider()
        st.write("**Algorithm Progress**")
        progress = (st.session_state.current_step + 1) / total_steps
        st.progress(progress)
        st.caption(f"{(progress * 100):.1f}% Complete")


def render_threat_monitor():
    """Render the threat monitor panel."""
    st.subheader("Threat Monitor")
    
    if st.session_state.network is None:
        st.info("Create a network first")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Generate Threat**")
        threat_type = st.selectbox("Threat Type", ["DDoS", "Intrusion", "Malware"], key="threat_type")
        origin_node = st.selectbox("Origin Node", st.session_state.network.get_all_nodes(), key="threat_origin")
        severity = st.slider("Severity", 0.0, 1.0, 0.7, key="threat_severity")
        
        if st.button("Generate Threat", key="generate_threat"):
            threat = st.session_state.threat_simulator.generate_threat(threat_type, origin_node, severity)
            st.session_state.threat_history.append(threat)
            st.success(f"Threat generated: {threat.threat_id}")
    
    with col2:
        st.write("**Threat Statistics**")
        st.metric("Active Threats", len(st.session_state.threat_history))
        compromised = st.session_state.network.get_compromised_nodes()
        st.metric("Compromised Nodes", len(compromised))
    
    # Display active threats
    if st.session_state.threat_history:
        st.write("**Active Threats**")
        threat_data = []
        for threat in st.session_state.threat_history:
            threat_data.append({
                "ID": threat.threat_id,
                "Type": threat.threat_type,
                "Severity": f"{threat.severity:.2f}",
                "Status": threat.status,
                "Affected": len(threat.affected_nodes)
            })
        
        df = pd.DataFrame(threat_data)
        st.dataframe(df, use_container_width=True)


def render_analytics_panel():
    """Render the performance analytics panel."""
    st.subheader("Performance Analytics")
    
    if not st.session_state.algorithm_running or st.session_state.current_algorithm is None:
        st.info("Run an algorithm first to see analytics")
        return
    
    step_tracker = st.session_state.current_algorithm.step_tracker
    all_steps = step_tracker.get_all_steps()
    
    if not all_steps:
        st.warning("No step data available")
        return
    
    # Extract metrics
    step_numbers = [s.step_number for s in all_steps]
    costs = [s.cost for s in all_steps]
    visited_counts = [len(s.visited_nodes) for s in all_steps]
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Steps", len(all_steps))
    with col2:
        st.metric("Final Cost", f"{costs[-1]:.2f}" if costs else "N/A")
    with col3:
        st.metric("Nodes Visited", visited_counts[-1] if visited_counts else 0)
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost progression chart
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Scatter(
            x=step_numbers, y=costs,
            mode='lines+markers',
            name='Cost',
            line=dict(color='#FF6B6B')
        ))
        fig_cost.update_layout(
            title='Cost Progression',
            xaxis_title='Step',
            yaxis_title='Cost',
            height=400
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    
    with col2:
        # Visited nodes progression chart
        fig_visited = go.Figure()
        fig_visited.add_trace(go.Scatter(
            x=step_numbers, y=visited_counts,
            mode='lines+markers',
            name='Visited Nodes',
            line=dict(color='#4ECDC4')
        ))
        fig_visited.update_layout(
            title='Visited Nodes Progression',
            xaxis_title='Step',
            yaxis_title='Visited Nodes',
            height=400
        )
        st.plotly_chart(fig_visited, use_container_width=True)


def main():
    """Main application entry point."""
    st.title("🛡️ Cybersecurity Threat Detection & Response System")
    st.markdown("Interactive visualization and analysis of network threats and algorithmic responses")
    
    # Initialize session state
    initialize_session_state()
    
    # Create tabs for different panels
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Network", "Control", "Animation", "Threats", "Analytics"
    ])
    
    with tab1:
        render_network_panel()
    
    with tab2:
        render_control_panel()
    
    with tab3:
        render_animation_panel()
    
    with tab4:
        render_threat_monitor()
    
    with tab5:
        render_analytics_panel()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Cybersecurity Threat Detection System** | "
        "Demonstrating DAA concepts through interactive visualization"
    )


if __name__ == "__main__":
    main()
