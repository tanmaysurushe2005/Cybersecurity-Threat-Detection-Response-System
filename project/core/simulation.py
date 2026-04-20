"""
Threat simulation engine for modeling cyber threats and their propagation through networks.
Supports DDoS, intrusion, and malware threat types with dynamic risk scoring.
"""

from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime
import networkx as nx

from .graph import NetworkGraph
from ..utils.data_structures import Threat, ThreatState, NetworkNode
from ..config import THREAT_TYPES, THREAT_SEVERITY_RANGE, THREAT_PROPAGATION_SPEED_RANGE


class ThreatSimulator:
    """
    Simulates cyber threats and their propagation through a network.
    Tracks threat states, affected nodes, and risk scores.
    """
    
    def __init__(self, graph: NetworkGraph):
        """
        Initialize the threat simulator with a network graph.
        
        Args:
            graph: NetworkGraph object representing the network
        """
        self.graph = graph
        self.active_threats: Dict[str, Threat] = {}
        self.threat_history: List[Threat] = []
        self.threat_states: List[ThreatState] = []
        self.affected_nodes: set = set()
    
    def generate_threat(self, threat_type: str, origin_node: str,
                       severity: Optional[float] = None,
                       propagation_speed: Optional[float] = None) -> Threat:
        """
        Generate a new threat in the network.
        
        Args:
            threat_type: Type of threat (DDoS, Intrusion, Malware)
            origin_node: Node where threat originates
            severity: Severity level (0.0-1.0), random if not specified
            propagation_speed: Propagation speed (0.0-1.0), random if not specified
            
        Returns:
            Generated Threat object
            
        Raises:
            ValueError: If parameters are invalid
        """
        if threat_type not in THREAT_TYPES:
            raise ValueError(f"Invalid threat_type: {threat_type}")
        
        if origin_node not in self.graph.nodes_data:
            raise ValueError(f"Origin node {origin_node} does not exist")
        
        if severity is None:
            severity = random.uniform(*THREAT_SEVERITY_RANGE)
        else:
            if not 0.0 <= severity <= 1.0:
                raise ValueError(f"severity must be between 0.0 and 1.0, got {severity}")
        
        if propagation_speed is None:
            propagation_speed = random.uniform(*THREAT_PROPAGATION_SPEED_RANGE)
        else:
            if not 0.0 <= propagation_speed <= 1.0:
                raise ValueError(f"propagation_speed must be between 0.0 and 1.0, got {propagation_speed}")
        
        threat = Threat(
            threat_type=threat_type,
            origin_node=origin_node,
            severity=severity,
            propagation_speed=propagation_speed,
            affected_nodes=[origin_node],
            status="active"
        )
        
        self.active_threats[threat.threat_id] = threat
        self.affected_nodes.add(origin_node)
        
        # Mark origin node as compromised
        self.graph.update_node_compromise_status(origin_node, True)
        
        return threat
    
    def simulate_propagation(self, threat: Threat, steps: int) -> List[ThreatState]:
        """
        Simulate threat propagation through the network for a specified number of steps.
        
        Args:
            threat: Threat object to propagate
            steps: Number of propagation steps to simulate
            
        Returns:
            List of ThreatState objects representing each step
            
        Raises:
            ValueError: If parameters are invalid
        """
        if steps <= 0:
            raise ValueError("steps must be greater than 0")
        
        if threat.threat_id not in self.active_threats:
            raise ValueError(f"Threat {threat.threat_id} is not active")
        
        threat_states = []
        current_affected = set(threat.affected_nodes)
        
        for step in range(steps):
            # Propagate threat to neighbors
            new_affected = set()
            
            for node_id in current_affected:
                neighbors = self.graph.get_neighbors(node_id)
                
                for neighbor in neighbors:
                    if neighbor not in current_affected:
                        # Propagate based on threat propagation speed and node risk
                        neighbor_node = self.graph.get_node_data(neighbor)
                        propagation_probability = (
                            threat.propagation_speed * neighbor_node.risk_level
                        )
                        
                        if random.random() < propagation_probability:
                            new_affected.add(neighbor)
                            self.graph.update_node_compromise_status(neighbor, True)
            
            # Update affected nodes
            current_affected.update(new_affected)
            threat.affected_nodes = list(current_affected)
            self.affected_nodes.update(new_affected)
            
            # Calculate network risk score
            network_risk = self._calculate_network_risk_score()
            
            # Create threat state for this step
            threat_state = ThreatState(
                timestamp=datetime.now(),
                active_threats=[threat],
                compromised_nodes=list(current_affected),
                network_risk_score=network_risk,
                propagation_paths=self._get_propagation_paths(threat),
                mitigation_actions=[]
            )
            
            threat_states.append(threat_state)
            self.threat_states.append(threat_state)
        
        return threat_states
    
    def calculate_risk_score(self, node_id: str) -> float:
        """
        Calculate the risk score for a specific node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Risk score between 0.0 and 1.0
            
        Raises:
            ValueError: If node does not exist
        """
        if node_id not in self.graph.nodes_data:
            raise ValueError(f"Node {node_id} does not exist")
        
        node = self.graph.get_node_data(node_id)
        base_risk = node.risk_level
        
        # Increase risk if node is compromised
        if node.is_compromised:
            base_risk = min(base_risk + 0.3, 1.0)
        
        # Increase risk based on threat proximity
        threat_proximity_risk = 0.0
        for threat in self.active_threats.values():
            if node_id in threat.affected_nodes:
                threat_proximity_risk = max(threat_proximity_risk, threat.severity)
        
        # Combine risks
        total_risk = min(base_risk + threat_proximity_risk, 1.0)
        
        return total_risk
    
    def get_affected_nodes(self) -> List[str]:
        """
        Get all currently affected nodes.
        
        Returns:
            List of affected node IDs
        """
        return list(self.affected_nodes)
    
    def get_threat_history(self) -> List[Threat]:
        """
        Get the complete threat history.
        
        Returns:
            List of all threats (active and resolved)
        """
        return self.threat_history + list(self.active_threats.values())
    
    def get_active_threats(self) -> List[Threat]:
        """
        Get all currently active threats.
        
        Returns:
            List of active Threat objects
        """
        return list(self.active_threats.values())
    
    def contain_threat(self, threat_id: str) -> bool:
        """
        Mark a threat as contained.
        
        Args:
            threat_id: ID of threat to contain
            
        Returns:
            True if threat was contained, False if threat not found
        """
        if threat_id in self.active_threats:
            threat = self.active_threats[threat_id]
            threat.status = "contained"
            self.threat_history.append(threat)
            del self.active_threats[threat_id]
            return True
        return False
    
    def resolve_threat(self, threat_id: str) -> bool:
        """
        Mark a threat as resolved.
        
        Args:
            threat_id: ID of threat to resolve
            
        Returns:
            True if threat was resolved, False if threat not found
        """
        if threat_id in self.active_threats:
            threat = self.active_threats[threat_id]
            threat.status = "resolved"
            self.threat_history.append(threat)
            del self.active_threats[threat_id]
            return True
        return False
    
    def reset_threats(self) -> None:
        """Reset all threats and clear affected nodes."""
        self.active_threats.clear()
        self.affected_nodes.clear()
        self.threat_states.clear()
        self.graph.reset_all_nodes()
    
    def _calculate_network_risk_score(self) -> float:
        """
        Calculate the overall network risk score.
        
        Returns:
            Network risk score between 0.0 and 1.0
        """
        if not self.affected_nodes:
            return 0.0
        
        total_risk = 0.0
        for node_id in self.affected_nodes:
            node = self.graph.get_node_data(node_id)
            total_risk += node.risk_level
        
        num_nodes = len(self.graph.get_all_nodes())
        return min(total_risk / num_nodes, 1.0)
    
    def _get_propagation_paths(self, threat: Threat) -> List[List[str]]:
        """
        Get the propagation paths for a threat.
        
        Args:
            threat: Threat object
            
        Returns:
            List of propagation paths (each path is a list of node IDs)
        """
        paths = []
        
        # Find paths from origin to all affected nodes using BFS
        origin = threat.origin_node
        visited = set()
        queue = [(origin, [origin])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current in threat.affected_nodes and current != origin:
                paths.append(path)
            
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited and neighbor in threat.affected_nodes:
                    queue.append((neighbor, path + [neighbor]))
        
        return paths
    
    def get_threat_states(self) -> List[ThreatState]:
        """
        Get all recorded threat states.
        
        Returns:
            List of ThreatState objects
        """
        return self.threat_states
    
    def get_latest_threat_state(self) -> Optional[ThreatState]:
        """
        Get the most recent threat state.
        
        Returns:
            Latest ThreatState or None if no states recorded
        """
        return self.threat_states[-1] if self.threat_states else None
    
    def __repr__(self) -> str:
        return (f"ThreatSimulator(active_threats={len(self.active_threats)}, "
                f"affected_nodes={len(self.affected_nodes)})")
    
    def __str__(self) -> str:
        return (f"Threat Simulator: {len(self.active_threats)} active threats, "
                f"{len(self.affected_nodes)} affected nodes")
