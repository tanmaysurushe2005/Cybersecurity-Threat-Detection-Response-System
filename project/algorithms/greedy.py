"""
Greedy threat mitigation algorithm for resource allocation.
Selects highest-risk threats first within budget constraints.
"""

from typing import Dict, List

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData
from ..utils.helpers import calculate_mitigation_cost


class Greedy:
    """
    Greedy algorithm for threat mitigation resource allocation.
    Prioritizes high-risk nodes for mitigation within budget constraints.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize Greedy algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.selected_nodes: List[str] = []
        self.step_number = 0
    
    def execute(self, threat_nodes: List[str], resources: float) -> None:
        """
        Execute greedy threat mitigation algorithm.
        
        Args:
            threat_nodes: List of threat node IDs
            resources: Available resources for mitigation
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not threat_nodes:
            raise ValueError("threat_nodes cannot be empty")
        if resources <= 0:
            raise ValueError("resources must be positive")
        
        # Initialize
        self.selected_nodes.clear()
        self.step_number = 0
        
        # Calculate risk scores for each threat node
        node_risks = []
        for node_id in threat_nodes:
            if node_id in self.graph.nodes_data:
                node = self.graph.get_node_data(node_id)
                risk_score = node.risk_level
                node_risks.append((node_id, risk_score))
        
        # Sort by risk score (descending)
        node_risks.sort(key=lambda x: x[1], reverse=True)
        
        # Greedily select nodes
        remaining_resources = resources
        
        for node_id, risk_score in node_risks:
            node = self.graph.get_node_data(node_id)
            mitigation_cost = calculate_mitigation_cost(node)
            
            if mitigation_cost <= remaining_resources:
                self.selected_nodes.append(node_id)
                remaining_resources -= mitigation_cost
                self._record_step(node_id, remaining_resources)
    
    def _record_step(self, current_node: str, remaining_resources: float) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            current_node: Currently selected node
            remaining_resources: Remaining resources after selection
        """
        total_cost = sum(
            calculate_mitigation_cost(self.graph.get_node_data(node))
            for node in self.selected_nodes
        )
        
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="Greedy",
            current_node=current_node,
            visited_nodes=self.selected_nodes.copy(),
            frontier_nodes=[],
            cost=total_cost,
            metadata={
                "selected_count": len(self.selected_nodes),
                "remaining_resources": remaining_resources
            }
        )
        
        self.step_tracker.record_step(step_data)
        self.step_number += 1
    
    def get_selected_nodes(self) -> List[str]:
        """
        Get all selected nodes for mitigation.
        
        Returns:
            List of selected node IDs
        """
        return self.selected_nodes.copy()
    
    def __repr__(self) -> str:
        return f"Greedy(selected={len(self.selected_nodes)})"
