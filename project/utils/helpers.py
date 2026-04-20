"""
Helper functions and utilities for the cybersecurity threat detection system.
Includes graph metrics, data conversion, and validation utilities.
"""

from typing import Dict, List, Tuple, Any
import math
import networkx as nx
from project.utils.data_structures import NetworkNode, NetworkEdge, Threat, StepData


def format_execution_time(seconds: float) -> str:
    """
    Convert seconds to readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted string: '45ms' under 1s, '1.23s' above
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    return f"{seconds:.2f}s"


def calculate_graph_density(graph: nx.Graph) -> float:
    """
    Calculate the density of a graph.
    Density = 2 * |E| / (|V| * (|V| - 1)) for undirected graphs.
    
    Args:
        graph: NetworkX graph object
        
    Returns:
        Graph density value between 0 and 1
    """
    if len(graph) < 2:
        return 0.0
    return nx.density(graph)


def calculate_graph_diameter(graph: nx.Graph) -> float:
    """
    Calculate the diameter of a graph (longest shortest path).
    
    Args:
        graph: NetworkX graph object
        
    Returns:
        Diameter value, or infinity if graph is disconnected
    """
    if not nx.is_connected(graph):
        # For disconnected graphs, return the maximum diameter of connected components
        components = nx.connected_components(graph)
        max_diameter = 0
        for component in components:
            subgraph = graph.subgraph(component)
            if len(subgraph) > 1:
                diameter = nx.diameter(subgraph)
                max_diameter = max(max_diameter, diameter)
        return max_diameter if max_diameter > 0 else float('inf')
    return nx.diameter(graph)


def calculate_clustering_coefficient(graph: nx.Graph) -> float:
    """
    Calculate the average clustering coefficient of a graph.
    
    Args:
        graph: NetworkX graph object
        
    Returns:
        Average clustering coefficient value between 0 and 1
    """
    if len(graph) < 3:
        return 0.0
    return nx.average_clustering(graph)


def calculate_node_degree_distribution(graph: nx.Graph) -> Dict[int, int]:
    """
    Calculate the degree distribution of a graph.
    
    Args:
        graph: NetworkX graph object
        
    Returns:
        Dictionary mapping degree to count of nodes with that degree
    """
    degree_dist = {}
    for node in graph.nodes():
        degree = graph.degree(node)
        degree_dist[degree] = degree_dist.get(degree, 0) + 1
    return degree_dist


def calculate_network_risk_score(nodes: List[NetworkNode], 
                                 compromised_nodes: List[str]) -> float:
    """
    Calculate overall network risk score based on compromised nodes.
    
    Args:
        nodes: List of all network nodes
        compromised_nodes: List of compromised node IDs
        
    Returns:
        Network risk score between 0.0 and 1.0
    """
    if not nodes:
        return 0.0
    
    total_risk = 0.0
    for node in nodes:
        if node.node_id in compromised_nodes:
            total_risk += node.risk_level
    
    return min(total_risk / len(nodes), 1.0)


def calculate_mitigation_cost(node: NetworkNode, base_cost: float = 50.0) -> float:
    """
    Calculate mitigation cost for a node based on its risk level.
    
    Args:
        node: NetworkNode to calculate cost for
        base_cost: Base mitigation cost
        
    Returns:
        Mitigation cost as a float
    """
    return base_cost * (1.0 + node.risk_level)


def calculate_route_cost(graph: nx.Graph, route: List[str]) -> float:
    """
    Calculate total cost of a route through the graph.
    Uses edge weights if available, otherwise uses 1.0 as default.
    
    Args:
        graph: NetworkX graph object
        route: List of node IDs representing the route
        
    Returns:
        Total cost of the route
    """
    if len(route) < 2:
        return 0.0
    
    total_cost = 0.0
    for i in range(len(route) - 1):
        source = route[i]
        target = route[i + 1]
        
        if graph.has_edge(source, target):
            edge_data = graph.get_edge_data(source, target)
            weight = edge_data.get('weight', 1.0)
            total_cost += weight
        else:
            # If edge doesn't exist, add a large penalty
            total_cost += float('inf')
    
    return total_cost


def get_shortest_path(graph: nx.Graph, source: str, target: str) -> List[str]:
    """
    Get the shortest path between two nodes using BFS.
    
    Args:
        graph: NetworkX graph object
        source: Source node ID
        target: Target node ID
        
    Returns:
        List of node IDs representing the shortest path, or empty list if no path exists
    """
    try:
        return nx.shortest_path(graph, source, target)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []


def get_all_shortest_paths(graph: nx.Graph, source: str, target: str) -> List[List[str]]:
    """
    Get all shortest paths between two nodes.
    
    Args:
        graph: NetworkX graph object
        source: Source node ID
        target: Target node ID
        
    Returns:
        List of all shortest paths
    """
    try:
        return list(nx.all_shortest_paths(graph, source, target))
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []


def validate_node_id(node_id: str) -> bool:
    """
    Validate that a node ID is properly formatted.
    
    Args:
        node_id: Node ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    return isinstance(node_id, str) and len(node_id) > 0


def validate_device_type(device_type: str, valid_types: List[str]) -> bool:
    """
    Validate that a device type is in the list of valid types.
    
    Args:
        device_type: Device type to validate
        valid_types: List of valid device types
        
    Returns:
        True if valid, False otherwise
    """
    return device_type in valid_types


def validate_risk_level(risk_level: float) -> bool:
    """
    Validate that a risk level is between 0.0 and 1.0.
    
    Args:
        risk_level: Risk level to validate
        
    Returns:
        True if valid, False otherwise
    """
    return isinstance(risk_level, (int, float)) and 0.0 <= risk_level <= 1.0


def validate_graph_parameters(num_nodes: int, topology: str, 
                             valid_topologies: List[str]) -> Tuple[bool, str]:
    """
    Validate graph creation parameters.
    
    Args:
        num_nodes: Number of nodes
        topology: Topology type
        valid_topologies: List of valid topology types
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if num_nodes <= 0:
        return False, "num_nodes must be greater than 0"
    if num_nodes > 1000:
        return False, "num_nodes must not exceed 1000"
    if topology not in valid_topologies:
        return False, f"topology must be one of {valid_topologies}"
    return True, ""


def convert_step_data_to_dict(step_data: StepData) -> Dict[str, Any]:
    """
    Convert StepData object to dictionary for JSON serialization.
    
    Args:
        step_data: StepData object to convert
        
    Returns:
        Dictionary representation of StepData
    """
    return {
        "step_number": step_data.step_number,
        "algorithm_name": step_data.algorithm_name,
        "current_node": step_data.current_node,
        "visited_nodes": step_data.visited_nodes,
        "frontier_nodes": step_data.frontier_nodes,
        "distances": step_data.distances,
        "parent_map": step_data.parent_map,
        "cost": step_data.cost,
        "metadata": step_data.metadata,
        "timestamp": step_data.timestamp
    }


def convert_threat_to_dict(threat: Threat) -> Dict[str, Any]:
    """
    Convert Threat object to dictionary for JSON serialization.
    
    Args:
        threat: Threat object to convert
        
    Returns:
        Dictionary representation of Threat
    """
    return {
        "threat_id": threat.threat_id,
        "threat_type": threat.threat_type,
        "origin_node": threat.origin_node,
        "severity": threat.severity,
        "propagation_speed": threat.propagation_speed,
        "affected_nodes": threat.affected_nodes,
        "timestamp": threat.timestamp.isoformat(),
        "status": threat.status
    }


def calculate_euclidean_distance(pos1: Tuple[float, float], 
                                pos2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two 2D positions.
    
    Args:
        pos1: First position as (x, y) tuple
        pos2: Second position as (x, y) tuple
        
    Returns:
        Euclidean distance
    """
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def normalize_value(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize a value to the range [0, 1].
    
    Args:
        value: Value to normalize
        min_val: Minimum value in the range
        max_val: Maximum value in the range
        
    Returns:
        Normalized value between 0 and 1
    """
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)
