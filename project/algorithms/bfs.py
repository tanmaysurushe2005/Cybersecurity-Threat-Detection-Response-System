"""
Breadth-First Search (BFS) algorithm implementation for network scanning.
Visits all reachable nodes from a starting point in breadth-first order.
"""

from typing import List, Set
from collections import deque

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData


class BFS:
    """
    Breadth-First Search algorithm for network scanning and threat detection.
    Explores all reachable nodes level by level from a starting node.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize BFS algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.visited: Set[str] = set()
        self.frontier: deque = deque()
        self.step_number = 0
    
    def execute(self, start_node: str) -> None:
        """
        Execute BFS algorithm starting from a given node.
        
        Args:
            start_node: Starting node ID
            
        Raises:
            ValueError: If start_node does not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        
        # Initialize
        self.visited.clear()
        self.frontier.clear()
        self.step_number = 0
        
        # Add start node to frontier
        self.frontier.append(start_node)
        self.visited.add(start_node)
        
        # Record initial step
        self._record_step(start_node)
        
        # Process frontier
        while self.frontier:
            current_node = self.frontier.popleft()
            
            # Get neighbors
            neighbors = self.graph.get_neighbors(current_node)
            
            # Process each neighbor
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.frontier.append(neighbor)
                    self._record_step(neighbor)
    
    def _record_step(self, current_node: str) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            current_node: Currently processing node
        """
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="BFS",
            current_node=current_node,
            visited_nodes=list(self.visited),
            frontier_nodes=list(self.frontier),
            cost=len(self.visited),
            metadata={
                "frontier_size": len(self.frontier),
                "visited_size": len(self.visited)
            }
        )
        
        self.step_tracker.record_step(step_data)
        self.step_number += 1
    
    def get_visited_nodes(self) -> List[str]:
        """
        Get all visited nodes.
        
        Returns:
            List of visited node IDs
        """
        return list(self.visited)
    
    def __repr__(self) -> str:
        return f"BFS(visited={len(self.visited)}, frontier={len(self.frontier)})"
