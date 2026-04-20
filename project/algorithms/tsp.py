"""
Traveling Salesman Problem (TSP) algorithm implementation for security patrol routes.
Finds the optimal route visiting all nodes exactly once with minimum total cost.
"""

from typing import List, Tuple
from itertools import permutations
import math

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData


class TSP:
    """
    Traveling Salesman Problem solver for finding optimal patrol routes.
    Uses exact algorithm for small graphs and nearest neighbor heuristic for large graphs.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize TSP algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.best_route: List[str] = []
        self.best_cost: float = float('inf')
        self.step_number = 0
    
    def execute(self, start_node: str) -> Tuple[List[str], float]:
        """
        Execute TSP algorithm starting from a given node.
        
        Args:
            start_node: Starting node ID
            
        Returns:
            Tuple of (best_route, best_cost)
            
        Raises:
            ValueError: If start_node does not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        
        nodes = self.graph.get_all_nodes()
        
        # Use exact algorithm for small graphs, heuristic for large
        if len(nodes) <= 12:
            return self._execute_exact(start_node, nodes)
        else:
            return self._execute_nearest_neighbor(start_node, nodes)
    
    def _execute_exact(self, start_node: str, nodes: List[str]) -> Tuple[List[str], float]:
        """
        Execute exact TSP algorithm using permutations.
        
        Args:
            start_node: Starting node ID
            nodes: List of all node IDs
            
        Returns:
            Tuple of (best_route, best_cost)
        """
        self.best_route = []
        self.best_cost = float('inf')
        self.step_number = 0
        
        # Generate all permutations starting with start_node
        other_nodes = [n for n in nodes if n != start_node]
        
        for perm in permutations(other_nodes):
            route = [start_node] + list(perm)
            cost = self._calculate_route_cost(route)
            
            # Record step
            self._record_step(route, cost)
            
            # Update best route if this is better
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_route = route
        
        return self.best_route, self.best_cost
    
    def _execute_nearest_neighbor(self, start_node: str, nodes: List[str]) -> Tuple[List[str], float]:
        """
        Execute TSP using nearest neighbor heuristic for large graphs.
        
        Args:
            start_node: Starting node ID
            nodes: List of all node IDs
            
        Returns:
            Tuple of (best_route, best_cost)
        """
        self.best_route = []
        self.best_cost = float('inf')
        self.step_number = 0
        
        # Nearest neighbor heuristic
        unvisited = set(nodes)
        current = start_node
        route = [current]
        unvisited.remove(current)
        
        while unvisited:
            # Find nearest unvisited node
            nearest = min(unvisited, key=lambda n: self._get_distance(current, n))
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
            
            # Record step
            cost = self._calculate_route_cost(route)
            self._record_step(route, cost)
        
        self.best_route = route
        self.best_cost = self._calculate_route_cost(route)
        
        return self.best_route, self.best_cost
    
    def _calculate_route_cost(self, route: List[str]) -> float:
        """
        Calculate the total cost of a route.
        
        Args:
            route: List of nodes in the route
            
        Returns:
            Total cost of the route
        """
        total_cost = 0.0
        
        for i in range(len(route) - 1):
            source = route[i]
            target = route[i + 1]
            distance = self._get_distance(source, target)
            total_cost += distance
        
        # Add distance back to start node
        if len(route) > 1:
            distance = self._get_distance(route[-1], route[0])
            total_cost += distance
        
        return total_cost
    
    def _get_distance(self, source: str, target: str) -> float:
        """
        Get the distance between two nodes.
        Uses latency as the distance metric.
        
        Args:
            source: Source node ID
            target: Target node ID
            
        Returns:
            Distance between nodes
        """
        edge = self.graph.get_edge_data(source, target)
        if edge:
            return edge.latency
        
        # If no direct edge, use a large penalty
        return 1000.0
    
    def _record_step(self, route: List[str], cost: float) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            route: Current route
            cost: Current route cost
        """
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="TSP",
            current_node=route[-1] if route else None,
            visited_nodes=route,
            frontier_nodes=[],
            cost=cost,
            metadata={
                "route_length": len(route),
                "total_cost": cost
            }
        )
        
        self.step_tracker.record_step(step_data)
        self.step_number += 1
    
    def get_best_route(self) -> List[str]:
        """
        Get the best route found.
        
        Returns:
            List of nodes in the best route
        """
        return self.best_route
    
    def get_best_cost(self) -> float:
        """
        Get the cost of the best route.
        
        Returns:
            Cost of the best route
        """
        return self.best_cost
    
    def __repr__(self) -> str:
        return f"TSP(best_cost={self.best_cost:.2f}, route_length={len(self.best_route)})"
