"""
Branch and Bound algorithm implementation for threat containment optimization.
Explores solution space with pruning to find optimal containment strategy.
"""

from typing import List, Dict, Tuple, Optional

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData


class BranchAndBound:
    """
    Branch and Bound algorithm for optimal threat containment strategy.
    Explores solution space using depth-first search with pruning.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize Branch and Bound algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.best_solution: List[str] = []
        self.best_cost: float = float('inf')
        self.step_number = 0
        self.nodes_explored = 0
        self.nodes_pruned = 0
    
    def execute(self, threat_nodes: List[str], budget: float) -> Tuple[List[str], float]:
        """
        Execute Branch and Bound algorithm to find optimal containment strategy.
        
        Args:
            threat_nodes: List of nodes to contain
            budget: Maximum budget for containment
            
        Returns:
            Tuple of (best_solution, best_cost)
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not threat_nodes:
            raise ValueError("threat_nodes cannot be empty")
        if budget <= 0:
            raise ValueError("budget must be positive")
        
        # Validate all threat nodes exist
        for node in threat_nodes:
            if node not in self.graph.nodes_data:
                raise ValueError(f"Threat node {node} does not exist")
        
        self.best_solution = []
        self.best_cost = float('inf')
        self.step_number = 0
        self.nodes_explored = 0
        self.nodes_pruned = 0
        
        # Start DFS with branch and bound
        self._dfs_branch_and_bound([], threat_nodes, budget, 0)
        
        return self.best_solution, self.best_cost
    
    def _dfs_branch_and_bound(self, current_solution: List[str], threat_nodes: List[str],
                              remaining_budget: float, depth: int) -> None:
        """
        Depth-first search with branch and bound pruning.
        
        Args:
            current_solution: Current partial solution
            threat_nodes: List of threat nodes to address
            remaining_budget: Remaining budget
            depth: Current depth in the search tree
        """
        self.nodes_explored += 1
        
        # Base case: all threat nodes have been considered
        if depth == len(threat_nodes):
            cost = self._calculate_solution_cost(current_solution)
            
            # Record step
            self._record_step(current_solution, cost)
            
            # Update best solution if this is better
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_solution = current_solution.copy()
            
            return
        
        # Calculate lower bound for pruning
        lower_bound = self._calculate_lower_bound(current_solution, threat_nodes[depth:], remaining_budget)
        
        # Prune if lower bound exceeds best cost found so far
        if lower_bound >= self.best_cost:
            self.nodes_pruned += 1
            return
        
        # Try including the current threat node
        current_threat = threat_nodes[depth]
        cost_to_contain = self._calculate_containment_cost(current_threat)
        
        if cost_to_contain <= remaining_budget:
            current_solution.append(current_threat)
            self._dfs_branch_and_bound(
                current_solution,
                threat_nodes,
                remaining_budget - cost_to_contain,
                depth + 1
            )
            current_solution.pop()
        
        # Try excluding the current threat node
        self._dfs_branch_and_bound(
            current_solution,
            threat_nodes,
            remaining_budget,
            depth + 1
        )
    
    def _calculate_containment_cost(self, node_id: str) -> float:
        """
        Calculate the cost to contain a threat on a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Cost to contain the threat
        """
        node = self.graph.get_node_data(node_id)
        
        # Cost is based on risk level and device type
        base_cost = node.risk_level * 100
        
        # Device type multiplier
        device_multipliers = {
            "server": 1.5,
            "workstation": 1.0,
            "router": 2.0,
            "firewall": 0.5
        }
        
        multiplier = device_multipliers.get(node.device_type, 1.0)
        
        return base_cost * multiplier
    
    def _calculate_solution_cost(self, solution: List[str]) -> float:
        """
        Calculate the total cost of a solution.
        
        Args:
            solution: List of nodes in the solution
            
        Returns:
            Total cost of the solution
        """
        total_cost = 0.0
        
        for node_id in solution:
            total_cost += self._calculate_containment_cost(node_id)
        
        return total_cost
    
    def _calculate_lower_bound(self, current_solution: List[str], remaining_threats: List[str],
                               remaining_budget: float) -> float:
        """
        Calculate a lower bound for the remaining solution.
        Uses the minimum cost of remaining threats as lower bound.
        
        Args:
            current_solution: Current partial solution
            remaining_threats: Remaining threats to address
            remaining_budget: Remaining budget
            
        Returns:
            Lower bound estimate
        """
        current_cost = self._calculate_solution_cost(current_solution)
        
        if not remaining_threats:
            return current_cost
        
        # Minimum cost is the cheapest remaining threat
        min_remaining_cost = min(
            self._calculate_containment_cost(node) for node in remaining_threats
        )
        
        return current_cost + min_remaining_cost
    
    def _record_step(self, solution: List[str], cost: float) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            solution: Current solution
            cost: Current solution cost
        """
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="BranchAndBound",
            current_node=solution[-1] if solution else None,
            visited_nodes=solution,
            frontier_nodes=[],
            cost=cost,
            metadata={
                "solution_size": len(solution),
                "total_cost": cost,
                "nodes_explored": self.nodes_explored,
                "nodes_pruned": self.nodes_pruned
            }
        )
        
        self.step_tracker.record_step(step_data)
        self.step_number += 1
    
    def get_best_solution(self) -> List[str]:
        """
        Get the best solution found.
        
        Returns:
            List of nodes in the best solution
        """
        return self.best_solution
    
    def get_best_cost(self) -> float:
        """
        Get the cost of the best solution.
        
        Returns:
            Cost of the best solution
        """
        return self.best_cost
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get algorithm execution statistics.
        
        Returns:
            Dictionary with nodes_explored and nodes_pruned
        """
        return {
            "nodes_explored": self.nodes_explored,
            "nodes_pruned": self.nodes_pruned
        }
    
    def __repr__(self) -> str:
        return (f"BranchAndBound(best_cost={self.best_cost:.2f}, "
                f"solution_size={len(self.best_solution)}, "
                f"explored={self.nodes_explored}, pruned={self.nodes_pruned})")
