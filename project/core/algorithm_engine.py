"""
Algorithm engine for executing graph algorithms with step-by-step tracking.
Implements 7 algorithms: BFS, DFS, Dijkstra, Greedy, Knapsack, TSP, Branch & Bound.
"""

from typing import Dict, List, Optional, Any, Tuple
import time
from abc import ABC, abstractmethod

from .graph import NetworkGraph
from .step_tracker import StepTracker
from ..utils.data_structures import StepData


class AlgorithmEngine:
    """
    Executes graph algorithms with complete step tracking for visualization.
    Supports pause/resume functionality and algorithm-specific metrics.
    """
    
    def __init__(self, graph: NetworkGraph):
        """
        Initialize the algorithm engine with a network graph.
        
        Args:
            graph: NetworkGraph object
        """
        self.graph = graph
        self.current_tracker: Optional[StepTracker] = None
        self.is_paused = False
        self.pause_step = -1
        self.execution_start_time = 0.0
        self.execution_end_time = 0.0
    
    @property
    def step_tracker(self) -> Optional[StepTracker]:
        """
        Get the current step tracker.
        
        Returns:
            The current StepTracker object or None if no execution
        """
        return self.current_tracker
    
    def execute_bfs(self, start_node: str) -> StepTracker:
        """
        Execute Breadth-First Search algorithm.
        
        Args:
            start_node: Starting node ID
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If start_node does not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        
        self.current_tracker = StepTracker("BFS")
        self.execution_start_time = time.time()
        
        from project.algorithms.bfs import BFS
        bfs = BFS(self.graph, self.current_tracker)
        bfs.execute(start_node)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def execute_dfs(self, start_node: str) -> StepTracker:
        """
        Execute Depth-First Search algorithm.
        
        Args:
            start_node: Starting node ID
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If start_node does not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        
        self.current_tracker = StepTracker("DFS")
        self.execution_start_time = time.time()
        
        from project.algorithms.dfs import DFS
        dfs = DFS(self.graph, self.current_tracker)
        dfs.execute(start_node)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def execute_dijkstra(self, start_node: str, end_node: str) -> StepTracker:
        """
        Execute Dijkstra's shortest path algorithm.
        
        Args:
            start_node: Starting node ID
            end_node: Ending node ID
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If nodes do not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        if end_node not in self.graph.nodes_data:
            raise ValueError(f"End node {end_node} does not exist")
        
        self.current_tracker = StepTracker("Dijkstra")
        self.execution_start_time = time.time()
        
        from project.algorithms.dijkstra import Dijkstra
        dijkstra = Dijkstra(self.graph, self.current_tracker)
        dijkstra.execute(start_node, end_node)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def execute_greedy(self, threat_nodes: List[str], resources: float) -> StepTracker:
        """
        Execute Greedy threat mitigation algorithm.
        
        Args:
            threat_nodes: List of threat node IDs
            resources: Available resources for mitigation
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not threat_nodes:
            raise ValueError("threat_nodes cannot be empty")
        if resources <= 0:
            raise ValueError("resources must be positive")
        
        self.current_tracker = StepTracker("Greedy")
        self.execution_start_time = time.time()
        
        from project.algorithms.greedy import Greedy
        greedy = Greedy(self.graph, self.current_tracker)
        greedy.execute(threat_nodes, resources)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def execute_knapsack(self, items: List[Dict[str, float]], capacity: float) -> StepTracker:
        """
        Execute 0/1 Knapsack resource allocation algorithm.
        
        Args:
            items: List of items with 'value' and 'weight' keys
            capacity: Knapsack capacity
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not items:
            raise ValueError("items cannot be empty")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        self.current_tracker = StepTracker("Knapsack")
        self.execution_start_time = time.time()
        
        from project.algorithms.knapsack import Knapsack
        knapsack = Knapsack(self.graph, self.current_tracker)
        knapsack.execute(items, capacity)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def execute_tsp(self, start_node: str) -> StepTracker:
        """
        Execute Traveling Salesman Problem patrol route algorithm.
        
        Args:
            start_node: Starting node ID
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If start_node does not exist
        """
        if start_node not in self.graph.nodes_data:
            raise ValueError(f"Start node {start_node} does not exist")
        
        self.current_tracker = StepTracker("TSP")
        self.execution_start_time = time.time()
        
        from project.algorithms.tsp import TSP
        tsp = TSP(self.graph, self.current_tracker)
        tsp.execute(start_node)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def execute_branch_and_bound(self, threat_nodes: List[str], budget: float) -> StepTracker:
        """
        Execute Branch and Bound threat containment algorithm.
        
        Args:
            threat_nodes: List of threat node IDs
            budget: Budget constraint
            
        Returns:
            StepTracker with complete execution history
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not threat_nodes:
            raise ValueError("threat_nodes cannot be empty")
        if budget <= 0:
            raise ValueError("budget must be positive")
        
        self.current_tracker = StepTracker("BranchAndBound")
        self.execution_start_time = time.time()
        
        from project.algorithms.branch_and_bound import BranchAndBound
        bnb = BranchAndBound(self.graph, self.current_tracker)
        bnb.execute(threat_nodes, budget)
        
        self.execution_end_time = time.time()
        return self.current_tracker
    
    def get_current_step(self) -> int:
        """
        Get the current step number.
        
        Returns:
            Current step number or -1 if no execution
        """
        if self.current_tracker:
            return self.current_tracker.current_step_index
        return -1
    
    def get_total_steps(self) -> int:
        """
        Get the total number of steps in current execution.
        
        Returns:
            Total steps or 0 if no execution
        """
        if self.current_tracker:
            return self.current_tracker.get_step_count()
        return 0
    
    def pause_execution(self) -> None:
        """Pause the current algorithm execution."""
        self.is_paused = True
        self.pause_step = self.get_current_step()
    
    def resume_execution(self) -> None:
        """Resume the paused algorithm execution."""
        self.is_paused = False
    
    def get_execution_time(self) -> float:
        """
        Get the execution time in seconds.
        
        Returns:
            Execution time in seconds
        """
        if self.execution_end_time > 0 and self.execution_start_time > 0:
            return self.execution_end_time - self.execution_start_time
        return 0.0
    
    def get_algorithm_metrics(self) -> Dict[str, Any]:
        """
        Get metrics for the current algorithm execution.
        
        Returns:
            Dictionary containing execution metrics
        """
        if not self.current_tracker:
            return {}
        
        metrics = self.current_tracker.get_algorithm_metrics()
        metrics["execution_time_ms"] = self.get_execution_time() * 1000
        
        return metrics
    
    def __repr__(self) -> str:
        algo_name = self.current_tracker.algorithm_name if self.current_tracker else "None"
        return f"AlgorithmEngine(current_algorithm={algo_name})"
    
    def __str__(self) -> str:
        if self.current_tracker:
            return (f"Algorithm Engine: {self.current_tracker.algorithm_name} - "
                    f"{self.get_total_steps()} steps")
        return "Algorithm Engine: No execution"
