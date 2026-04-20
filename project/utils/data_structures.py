"""
Data structures and models for the cybersecurity threat detection system.
Includes NetworkNode, NetworkEdge, Threat, StepData, and ThreatState models.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


@dataclass
class NetworkNode:
    """
    Represents a device/node in the network.
    
    Attributes:
        node_id: Unique identifier for the node
        device_type: Type of device (server, workstation, router, firewall)
        risk_level: Risk level from 0.0 to 1.0
        is_compromised: Whether the node is currently compromised
        security_patches: Number of security patches applied
        cpu_usage: CPU usage percentage (0-100)
        network_traffic: Network traffic volume
    """
    node_id: str
    device_type: str
    risk_level: float
    is_compromised: bool = False
    security_patches: int = 0
    cpu_usage: float = 0.0
    network_traffic: float = 0.0
    
    def __post_init__(self):
        """Validate node attributes after initialization."""
        if not 0.0 <= self.risk_level <= 1.0:
            raise ValueError(f"risk_level must be between 0.0 and 1.0, got {self.risk_level}")
        if not 0.0 <= self.cpu_usage <= 100.0:
            raise ValueError(f"cpu_usage must be between 0.0 and 100.0, got {self.cpu_usage}")
        if self.network_traffic < 0:
            raise ValueError(f"network_traffic must be non-negative, got {self.network_traffic}")
    
    def __repr__(self) -> str:
        return (f"NetworkNode(id={self.node_id}, type={self.device_type}, "
                f"risk={self.risk_level:.2f}, compromised={self.is_compromised})")
    
    def __str__(self) -> str:
        status = "COMPROMISED" if self.is_compromised else "NORMAL"
        return f"Node {self.node_id} ({self.device_type}) - {status}"


@dataclass
class NetworkEdge:
    """
    Represents a connection between two nodes in the network.
    
    Attributes:
        source: Source node ID
        target: Target node ID
        bandwidth: Bandwidth capacity in Mbps
        latency: Latency in milliseconds
        is_monitored: Whether the edge is monitored
        traffic_volume: Current traffic volume
    """
    source: str
    target: str
    bandwidth: float
    latency: float
    is_monitored: bool = False
    traffic_volume: float = 0.0
    
    def __post_init__(self):
        """Validate edge attributes after initialization."""
        if self.bandwidth <= 0:
            raise ValueError(f"bandwidth must be positive, got {self.bandwidth}")
        if self.latency <= 0:
            raise ValueError(f"latency must be positive, got {self.latency}")
        if self.traffic_volume < 0:
            raise ValueError(f"traffic_volume must be non-negative, got {self.traffic_volume}")
    
    def __repr__(self) -> str:
        return (f"NetworkEdge({self.source}->{self.target}, "
                f"bw={self.bandwidth}Mbps, lat={self.latency}ms)")
    
    def __str__(self) -> str:
        return f"Edge {self.source} -> {self.target} ({self.bandwidth}Mbps, {self.latency}ms)"


@dataclass
class Threat:
    """
    Represents a cyber threat in the network.
    
    Attributes:
        threat_id: Unique identifier for the threat
        threat_type: Type of threat (DDoS, Intrusion, Malware)
        origin_node: Node where threat originated
        severity: Severity level from 0.0 to 1.0
        propagation_speed: Speed of threat propagation
        affected_nodes: List of currently affected nodes
        timestamp: When the threat was created
        status: Current status (active, contained, resolved)
    """
    threat_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    threat_type: str = ""
    origin_node: str = ""
    severity: float = 0.0
    propagation_speed: float = 0.0
    affected_nodes: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "active"
    
    def __post_init__(self):
        """Validate threat attributes after initialization."""
        if not 0.0 <= self.severity <= 1.0:
            raise ValueError(f"severity must be between 0.0 and 1.0, got {self.severity}")
        if not 0.0 <= self.propagation_speed <= 1.0:
            raise ValueError(f"propagation_speed must be between 0.0 and 1.0, got {self.propagation_speed}")
        if self.status not in ["active", "contained", "resolved"]:
            raise ValueError(f"status must be 'active', 'contained', or 'resolved', got {self.status}")
    
    def __repr__(self) -> str:
        return (f"Threat(id={self.threat_id}, type={self.threat_type}, "
                f"severity={self.severity:.2f}, status={self.status})")
    
    def __str__(self) -> str:
        return f"Threat {self.threat_id} ({self.threat_type}) - {self.status.upper()}"


@dataclass
class StepData:
    """
    Represents a single step in algorithm execution.
    
    Attributes:
        step_number: Step number in the execution sequence
        algorithm_name: Name of the algorithm being executed
        description: Description of what happened in this step
        current_node: Currently processing node
        visited_nodes: List of visited nodes
        frontier_nodes: List of frontier nodes awaiting processing
        distances: Dictionary of distances to nodes (for Dijkstra)
        parent_map: Dictionary mapping nodes to their parents (for path reconstruction)
        cost: Current cost/distance value
        metadata: Algorithm-specific metadata
        timestamp: When this step was recorded
    """
    step_number: int
    algorithm_name: str
    description: str = ""
    current_node: Optional[str] = None
    visited_nodes: List[str] = field(default_factory=list)
    frontier_nodes: List[str] = field(default_factory=list)
    distances: Dict[str, float] = field(default_factory=dict)
    parent_map: Dict[str, str] = field(default_factory=dict)
    cost: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def __repr__(self) -> str:
        return (f"StepData(step={self.step_number}, algo={self.algorithm_name}, "
                f"current={self.current_node}, visited={len(self.visited_nodes)})")
    
    def __str__(self) -> str:
        return (f"Step {self.step_number}: {self.algorithm_name} - "
                f"Current: {self.current_node}, Visited: {len(self.visited_nodes)}")


@dataclass
class ThreatState:
    """
    Represents the state of threats in the network at a point in time.
    
    Attributes:
        timestamp: When this state was recorded
        active_threats: List of active threats
        compromised_nodes: List of currently compromised nodes
        network_risk_score: Overall network risk score
        propagation_paths: Paths through which threats propagate
        mitigation_actions: Actions taken to mitigate threats
    """
    timestamp: datetime = field(default_factory=datetime.now)
    active_threats: List[Threat] = field(default_factory=list)
    compromised_nodes: List[str] = field(default_factory=list)
    network_risk_score: float = 0.0
    propagation_paths: List[List[str]] = field(default_factory=list)
    mitigation_actions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate threat state attributes after initialization."""
        if not 0.0 <= self.network_risk_score <= 1.0:
            raise ValueError(f"network_risk_score must be between 0.0 and 1.0, got {self.network_risk_score}")
    
    def __repr__(self) -> str:
        return (f"ThreatState(threats={len(self.active_threats)}, "
                f"compromised={len(self.compromised_nodes)}, "
                f"risk={self.network_risk_score:.2f})")
    
    def __str__(self) -> str:
        return (f"Threat State: {len(self.active_threats)} active threats, "
                f"{len(self.compromised_nodes)} compromised nodes, "
                f"Risk: {self.network_risk_score:.2f}")
