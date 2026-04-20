"""
Depth-First Search (DFS) algorithm implementation for threat propagation analysis.
Visits all reachable nodes from a starting point in depth-first order.
"""

from typing import List, Set

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData


class DFS:
    """
    Depth-First Search algorithm for threat propagation analysis.
    Explores deep into the network before backtracking.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize DFS algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.visited: Set[str] = set()
        self.stack: List[str] = []
        self.step_number = 0
    
    def execute(self, start_node: str) -> None:
        """
        Execute DFS algorithm starting from a given node.
        
        Args:
            start_node: Starting node ID
            
        Raises:
            ValueError: If start_node does not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        
        # Initialize
        self.visited.clear()
        self.stack.clear()
        self.step_number = 0
        
        # Start DFS
        self._dfs_recursive(start_node)
    
    def _dfs_recursive(self, node: str) -> None:
        """
        Recursive DFS helper function.
        
        Args:
            node: Current node to process
        """
        if node in self.visited:
            return
        
        # Mark as visited
        self.visited.add(node)
        self._record_step(node)
        
        # Visit neighbors
        neighbors = self.graph.get_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in self.visited:
                self._dfs_recursive(neighbor)
    
    def _record_step(self, current_node: str) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            current_node: Currently processing node
        """
        # Get frontier nodes (unvisited neighbors of visited nodes)
        frontier = set()
        for visited_node in self.visited:
            neighbors = self.graph.get_neighbors(visited_node)
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    frontier.add(neighbor)
        
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="DFS",
            current_node=current_node,
            visited_nodes=list(self.visited),
            frontier_nodes=list(frontier),
            cost=len(self.visited),
            metadata={
                "frontier_size": len(frontier),
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
        return f"DFS(visited={len(self.visited)})"
