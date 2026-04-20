"""
Graph layer implementation using NetworkX.
Manages network representation as a directed/undirected graph with nodes and edges.
"""

from typing import Dict, List, Tuple, Optional, Any
import networkx as nx
import random

from ..utils.data_structures import NetworkNode, NetworkEdge
from ..utils.helpers import (
    calculate_graph_density, calculate_graph_diameter,
    calculate_clustering_coefficient, calculate_node_degree_distribution,
    validate_graph_parameters, validate_node_id, validate_device_type,
    validate_risk_level
)
from ..config import DEVICE_TYPES, RISK_LEVEL_RANGE, BANDWIDTH_RANGE, LATENCY_RANGE


class NetworkGraph:
    """
    Represents a computer network as a graph with nodes (devices) and edges (connections).
    Supports multiple topology types: random, scale-free, and small-world.
    """
    
    def __init__(self, num_nodes: int, topology: str = "random", directed: bool = False):
        """
        Initialize a network graph with specified topology.
        
        Args:
            num_nodes: Number of nodes in the network
            topology: Type of topology ("random", "scale-free", "small-world")
            directed: Whether the graph is directed
            
        Raises:
            ValueError: If parameters are invalid
        """
        is_valid, error_msg = validate_graph_parameters(
            num_nodes, topology, ["random", "scale-free", "small-world"]
        )
        if not is_valid:
            raise ValueError(error_msg)
        
        self.num_nodes = num_nodes
        self.topology = topology
        self.directed = directed
        
        # Create the underlying NetworkX graph
        if directed:
            self.graph = nx.DiGraph()
        else:
            self.graph = nx.Graph()
        
        # Store node and edge metadata
        self.nodes_data: Dict[str, NetworkNode] = {}
        self.edges_data: Dict[Tuple[str, str], NetworkEdge] = {}
        
        # Generate the topology
        self._generate_topology()
    
    def _generate_topology(self):
        """Generate the network topology based on the specified type."""
        if self.topology == "random":
            self._generate_random_topology()
        elif self.topology == "scale-free":
            self._generate_scale_free_topology()
        elif self.topology == "small-world":
            self._generate_small_world_topology()
    
    def _generate_random_topology(self):
        """Generate a random topology using Erdős-Rényi model."""
        # Create nodes
        for i in range(self.num_nodes):
            node_id = f"node_{i}"
            device_type = random.choice(DEVICE_TYPES)
            risk_level = random.uniform(*RISK_LEVEL_RANGE)
            self.add_node(node_id, device_type, risk_level)
        
        # Create edges with probability based on graph size
        # For small graphs, use higher probability to ensure connectivity
        edge_probability = max(0.1, 2.0 / self.num_nodes)
        
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < edge_probability:
                    source = f"node_{i}"
                    target = f"node_{j}"
                    bandwidth = random.uniform(*BANDWIDTH_RANGE)
                    latency = random.uniform(*LATENCY_RANGE)
                    self.add_edge(source, target, bandwidth, latency)
    
    def _generate_scale_free_topology(self):
        """Generate a scale-free topology using Barabási-Albert model."""
        # Create initial nodes
        for i in range(self.num_nodes):
            node_id = f"node_{i}"
            device_type = random.choice(DEVICE_TYPES)
            risk_level = random.uniform(*RISK_LEVEL_RANGE)
            self.add_node(node_id, device_type, risk_level)
        
        # Use NetworkX Barabási-Albert model for scale-free topology
        ba_graph = nx.barabasi_albert_graph(self.num_nodes, m=2)
        
        # Add edges from the BA model
        for source, target in ba_graph.edges():
            source_id = f"node_{source}"
            target_id = f"node_{target}"
            bandwidth = random.uniform(*BANDWIDTH_RANGE)
            latency = random.uniform(*LATENCY_RANGE)
            self.add_edge(source_id, target_id, bandwidth, latency)
    
    def _generate_small_world_topology(self):
        """Generate a small-world topology using Watts-Strogatz model."""
        # Create initial nodes
        for i in range(self.num_nodes):
            node_id = f"node_{i}"
            device_type = random.choice(DEVICE_TYPES)
            risk_level = random.uniform(*RISK_LEVEL_RANGE)
            self.add_node(node_id, device_type, risk_level)
        
        # Use NetworkX Watts-Strogatz model for small-world topology
        # k is the number of nearest neighbors (use 4 for reasonable connectivity)
        k = min(4, self.num_nodes - 1)
        ws_graph = nx.watts_strogatz_graph(self.num_nodes, k, p=0.3)
        
        # Add edges from the WS model
        for source, target in ws_graph.edges():
            source_id = f"node_{source}"
            target_id = f"node_{target}"
            bandwidth = random.uniform(*BANDWIDTH_RANGE)
            latency = random.uniform(*LATENCY_RANGE)
            self.add_edge(source_id, target_id, bandwidth, latency)
    
    def add_node(self, node_id: str, device_type: str, risk_level: float,
                 security_patches: int = 0, cpu_usage: float = 0.0,
                 network_traffic: float = 0.0) -> None:
        """
        Add a node to the network.
        
        Args:
            node_id: Unique identifier for the node
            device_type: Type of device (server, workstation, router, firewall)
            risk_level: Risk level from 0.0 to 1.0
            security_patches: Number of security patches applied
            cpu_usage: CPU usage percentage
            network_traffic: Network traffic volume
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not validate_node_id(node_id):
            raise ValueError(f"Invalid node_id: {node_id}")
        if not validate_device_type(device_type, DEVICE_TYPES):
            raise ValueError(f"Invalid device_type: {device_type}")
        if not validate_risk_level(risk_level):
            raise ValueError(f"Invalid risk_level: {risk_level}")
        
        node = NetworkNode(
            node_id=node_id,
            device_type=device_type,
            risk_level=risk_level,
            security_patches=security_patches,
            cpu_usage=cpu_usage,
            network_traffic=network_traffic
        )
        
        self.nodes_data[node_id] = node
        self.graph.add_node(node_id)
    
    def add_edge(self, source: str, target: str, bandwidth: float, latency: float,
                 is_monitored: bool = False, traffic_volume: float = 0.0) -> None:
        """
        Add an edge between two nodes.
        
        Args:
            source: Source node ID
            target: Target node ID
            bandwidth: Bandwidth capacity in Mbps
            latency: Latency in milliseconds
            is_monitored: Whether the edge is monitored
            traffic_volume: Current traffic volume
            
        Raises:
            ValueError: If parameters are invalid
        """
        if source not in self.nodes_data:
            raise ValueError(f"Source node {source} does not exist")
        if target not in self.nodes_data:
            raise ValueError(f"Target node {target} does not exist")
        
        edge = NetworkEdge(
            source=source,
            target=target,
            bandwidth=bandwidth,
            latency=latency,
            is_monitored=is_monitored,
            traffic_volume=traffic_volume
        )
        
        edge_key = (source, target)
        self.edges_data[edge_key] = edge
        
        # Add edge to NetworkX graph with weight as latency
        self.graph.add_edge(source, target, weight=latency)
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """
        Get all neighbors of a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            List of neighbor node IDs
            
        Raises:
            ValueError: If node does not exist
        """
        if node_id not in self.nodes_data:
            raise ValueError(f"Node {node_id} does not exist")
        
        return list(self.graph.neighbors(node_id))
    
    def get_node_data(self, node_id: str) -> NetworkNode:
        """
        Get data for a specific node.
        
        Args:
            node_id: Node ID
            
        Returns:
            NetworkNode object
            
        Raises:
            ValueError: If node does not exist
        """
        if node_id not in self.nodes_data:
            raise ValueError(f"Node {node_id} does not exist")
        
        return self.nodes_data[node_id]
    
    def get_edge_data(self, source: str, target: str) -> Optional[NetworkEdge]:
        """
        Get data for a specific edge.
        
        Args:
            source: Source node ID
            target: Target node ID
            
        Returns:
            NetworkEdge object or None if edge does not exist
        """
        edge_key = (source, target)
        return self.edges_data.get(edge_key)
    
    def get_all_nodes(self) -> List[str]:
        """
        Get all node IDs in the network.
        
        Returns:
            List of all node IDs
        """
        return list(self.nodes_data.keys())
    
    def get_all_edges(self) -> List[Tuple[str, str]]:
        """
        Get all edges in the network.
        
        Returns:
            List of tuples (source, target) representing edges
        """
        return list(self.edges_data.keys())
    
    def get_shortest_path(self, source: str, target: str) -> List[str]:
        """
        Get the shortest path between two nodes using Dijkstra's algorithm.
        
        Args:
            source: Source node ID
            target: Target node ID
            
        Returns:
            List of node IDs representing the shortest path, or empty list if no path exists
        """
        try:
            return nx.shortest_path(self.graph, source, target, weight='weight')
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
    
    def get_graph_metrics(self) -> Dict[str, float]:
        """
        Calculate and return graph statistics.
        
        Returns:
            Dictionary containing:
                - density: Graph density
                - diameter: Graph diameter
                - clustering_coefficient: Average clustering coefficient
                - num_nodes: Number of nodes
                - num_edges: Number of edges
                - avg_degree: Average node degree
        """
        num_edges = len(self.edges_data)
        avg_degree = 2 * num_edges / self.num_nodes if self.num_nodes > 0 else 0
        
        return {
            "density": calculate_graph_density(self.graph),
            "diameter": calculate_graph_diameter(self.graph),
            "clustering_coefficient": calculate_clustering_coefficient(self.graph),
            "num_nodes": self.num_nodes,
            "num_edges": num_edges,
            "avg_degree": avg_degree
        }
    
    def get_degree_distribution(self) -> Dict[int, int]:
        """
        Get the degree distribution of the network.
        
        Returns:
            Dictionary mapping degree to count of nodes with that degree
        """
        return calculate_node_degree_distribution(self.graph)
    
    def is_connected(self) -> bool:
        """
        Check if the network is connected.
        
        Returns:
            True if connected, False otherwise
        """
        return nx.is_connected(self.graph)
    
    def get_connected_components(self) -> List[List[str]]:
        """
        Get all connected components in the network.
        
        Returns:
            List of connected components, each as a list of node IDs
        """
        components = nx.connected_components(self.graph)
        return [list(component) for component in components]
    
    def update_node_compromise_status(self, node_id: str, is_compromised: bool) -> None:
        """
        Update the compromise status of a node.
        
        Args:
            node_id: Node ID
            is_compromised: New compromise status
            
        Raises:
            ValueError: If node does not exist
        """
        if node_id not in self.nodes_data:
            raise ValueError(f"Node {node_id} does not exist")
        
        self.nodes_data[node_id].is_compromised = is_compromised
    
    def get_compromised_nodes(self) -> List[str]:
        """
        Get all currently compromised nodes.
        
        Returns:
            List of compromised node IDs
        """
        return [node_id for node_id, node in self.nodes_data.items()
                if node.is_compromised]
    
    def reset_all_nodes(self) -> None:
        """Reset all nodes to non-compromised status."""
        for node in self.nodes_data.values():
            node.is_compromised = False
    
    def __repr__(self) -> str:
        return (f"NetworkGraph(nodes={self.num_nodes}, edges={len(self.edges_data)}, "
                f"topology={self.topology})")
    
    def __str__(self) -> str:
        return (f"Network Graph: {self.num_nodes} nodes, {len(self.edges_data)} edges, "
                f"topology={self.topology}")
