"""
Dijkstra's shortest path algorithm implementation for optimal threat response paths.
Finds the shortest path between two nodes in a weighted graph.
"""

from typing import Dict, List, Optional, Set
import heapq

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData


class Dijkstra:
    """
    Dijkstra's algorithm for finding optimal threat response paths.
    Computes shortest paths from a source to all reachable nodes.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize Dijkstra algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.distances: Dict[str, float] = {}
        self.parent_map: Dict[str, Optional[str]] = {}
        self.visited: Set[str] = set()
        self.step_number = 0
    
    def execute(self, start_node: str, end_node: str) -> None:
        """
        Execute Dijkstra algorithm from start to end node.
        
        Args:
            start_node: Starting node ID
            end_node: Ending node ID
            
        Raises:
            ValueError: If nodes do not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        if end_node not in self.graph.nodes_data:
            raise ValueError(f"End node {end_node} does not exist")
        
        # Initialize
        self.distances.clear()
        self.parent_map.clear()
        self.visited.clear()
        self.step_number = 0
        
        # Initialize distances
        for node in self.graph.get_all_nodes():
            self.distances[node] = float('inf')
            self.parent_map[node] = None
        
        self.distances[start_node] = 0
        
        # Priority queue: (distance, node)
        pq = [(0, start_node)]
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # Skip if already visited
            if current_node in self.visited:
                continue
            
            # Mark as visited
            self.visited.add(current_node)
            self._record_step(current_node)
            
            # Stop if we reached the end node
            if current_node == end_node:
                break
            
            # Skip if distance is outdated
            if current_distance > self.distances[current_node]:
                continue
            
            # Process neighbors
            neighbors = self.graph.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    # Get edge weight (latency)
                    edge_data = self.graph.get_edge_data(current_node, neighbor)
                    if edge_data:
                        weight = edge_data.latency
                    else:
                        weight = 1.0
                    
                    new_distance = self.distances[current_node] + weight
                    
                    # Update if we found a shorter path
                    if new_distance < self.distances[neighbor]:
                        self.distances[neighbor] = new_distance
                        self.parent_map[neighbor] = current_node
                        heapq.heappush(pq, (new_distance, neighbor))
    
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
        
        # Get current cost
        current_cost = self.distances.get(current_node, float('inf'))
        
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="Dijkstra",
            current_node=current_node,
            visited_nodes=list(self.visited),
            frontier_nodes=list(frontier),
            distances=self.distances.copy(),
            parent_map=self.parent_map.copy(),
            cost=current_cost,
            metadata={
                "frontier_size": len(frontier),
                "visited_size": len(self.visited)
            }
        )
        
        self.step_tracker.record_step(step_data)
        self.step_number += 1
    
    def get_shortest_path(self, end_node: str) -> List[str]:
        """
        Get the shortest path to a node.
        
        Args:
            end_node: Target node ID
            
        Returns:
            List of node IDs representing the shortest path
        """
        if end_node not in self.parent_map:
            return []
        
        path = []
        current = end_node
        
        while current is not None:
            path.append(current)
            current = self.parent_map[current]
        
        return list(reversed(path))
    
    def get_distance(self, node: str) -> float:
        """
        Get the shortest distance to a node.
        
        Args:
            node: Node ID
            
        Returns:
            Shortest distance or infinity if unreachable
        """
        return self.distances.get(node, float('inf'))
    
    def __repr__(self) -> str:
        return f"Dijkstra(visited={len(self.visited)}, distances={len(self.distances)})"
