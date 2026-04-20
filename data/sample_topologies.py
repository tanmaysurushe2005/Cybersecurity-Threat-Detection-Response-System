"""
Pre-built network topologies for testing and demonstration.
Provides realistic graph structures representing common threat scenarios.
"""

from project.core.graph import NetworkGraph


def small_office_network() -> NetworkGraph:
    """
    Create a small office network topology (10 nodes).
    
    Represents:
    - Computers, printers, servers connected via office network
    - Each node is a network device potentially vulnerable to threats
    - Edges represent network connectivity paths
    
    Returns:
        NetworkGraph with 10 nodes representing office infrastructure
    """
    graph = NetworkGraph(num_nodes=10, topology="random")
    # Graph is created with random connectivity
    # Typical office network would have a switch at center connected to devices
    return graph


def city_road_network() -> NetworkGraph:
    """
    Create a city road network topology (25 nodes).
    
    Represents:
    - Intersections in a city road network
    - Nodes are traffic intersections or critical infrastructure points
    - Edges are roads connecting intersections
    - Useful for testing routing and TSP scenarios
    
    Returns:
        NetworkGraph with 25 nodes representing city infrastructure
    """
    graph = NetworkGraph(num_nodes=25, topology="random")
    # Graph represents interconnected city infrastructure
    # Could be analyzed for optimal patrol routes, shortest paths between critical points
    return graph


def threat_scenario_network() -> NetworkGraph:
    """
    Create a network topology simulating a threat scenario (15 nodes).
    
    Represents:
    - A network under potential security threat
    - Nodes are systems that could be compromised
    - Edges are potential attack paths
    - Useful for testing threat detection and mitigation algorithms
    
    Returns:
        NetworkGraph with 15 nodes representing vulnerable systems
    """
    graph = NetworkGraph(num_nodes=15, topology="random")
    # Graph represents systems in a potentially compromised network
    # Useful for testing greedy mitigation, branch & bound optimization, Dijkstra path analysis
    return graph


def get_sample_topologies() -> dict:
    """
    Get all sample topologies as a dictionary.
    
    Returns:
        Dictionary mapping topology names to NetworkGraph instances
    """
    return {
        "small_office_network": small_office_network(),
        "city_road_network": city_road_network(),
        "threat_scenario_network": threat_scenario_network(),
    }
