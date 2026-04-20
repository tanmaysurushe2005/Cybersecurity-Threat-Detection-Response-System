"""
Step tracking system for recording and replaying algorithm execution.
Provides step-by-step visualization data and execution history management.
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from ..utils.data_structures import StepData
from ..config import NODE_COLORS


class StepTracker:
    """
    Records and manages step-by-step execution data for algorithm visualization and replay.
    Supports forward/backward navigation and history export.
    """
    
    def __init__(self, algorithm_name: str):
        """
        Initialize the step tracker for an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm being tracked
        """
        self.algorithm_name = algorithm_name
        self.steps: List[StepData] = []
        self.current_step_index = -1
        self.start_time = datetime.now()
    
    def record_step(self, step_data: StepData) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            step_data: StepData object containing step information
        """
        if step_data.algorithm_name != self.algorithm_name:
            raise ValueError(
                f"Step algorithm {step_data.algorithm_name} does not match "
                f"tracker algorithm {self.algorithm_name}"
            )
        
        self.steps.append(step_data)
        self.current_step_index = len(self.steps) - 1
    
    def get_step(self, step_num: int) -> Optional[StepData]:
        """
        Get a specific step by step number.
        
        Args:
            step_num: Step number (0-indexed)
            
        Returns:
            StepData object or None if step does not exist
        """
        if 0 <= step_num < len(self.steps):
            return self.steps[step_num]
        return None
    
    def get_all_steps(self) -> List[StepData]:
        """
        Get all recorded steps.
        
        Returns:
            List of all StepData objects
        """
        return self.steps.copy()
    
    def get_step_count(self) -> int:
        """
        Get the total number of recorded steps.
        
        Returns:
            Total number of steps
        """
        return len(self.steps)
    
    def get_current_step(self) -> Optional[StepData]:
        """
        Get the current step.
        
        Returns:
            Current StepData object or None if no steps recorded
        """
        if self.current_step_index >= 0 and self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def next_step(self) -> Optional[StepData]:
        """
        Advance to the next step.
        
        Returns:
            Next StepData object or None if at end
        """
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            return self.steps[self.current_step_index]
        return None
    
    def previous_step(self) -> Optional[StepData]:
        """
        Go back to the previous step.
        
        Returns:
            Previous StepData object or None if at beginning
        """
        if self.current_step_index > 0:
            self.current_step_index -= 1
            return self.steps[self.current_step_index]
        return None
    
    def jump_to_step(self, step_num: int) -> Optional[StepData]:
        """
        Jump to a specific step.
        
        Args:
            step_num: Step number to jump to (0-indexed)
            
        Returns:
            StepData at the specified step or None if invalid
        """
        if 0 <= step_num < len(self.steps):
            self.current_step_index = step_num
            return self.steps[step_num]
        return None
    
    def get_visualization_data(self, step_num: int, graph_nodes: List[str]) -> Dict[str, Any]:
        """
        Generate visualization data for a specific step.
        
        Args:
            step_num: Step number to generate visualization for
            graph_nodes: List of all node IDs in the graph
            
        Returns:
            Dictionary containing visualization data with node colors and annotations
        """
        step_data = self.get_step(step_num)
        if not step_data:
            return {}
        
        # Initialize all nodes as normal (green)
        node_colors = {node: NODE_COLORS["normal"] for node in graph_nodes}
        node_annotations = {node: "" for node in graph_nodes}
        
        # Color visited nodes
        for node in step_data.visited_nodes:
            if node in node_colors:
                node_colors[node] = "#FFA500"  # Orange for visited
        
        # Color frontier nodes
        for node in step_data.frontier_nodes:
            if node in node_colors:
                node_colors[node] = "#FFD700"  # Gold for frontier
        
        # Color current node
        if step_data.current_node and step_data.current_node in node_colors:
            node_colors[step_data.current_node] = "#FF6347"  # Tomato for current
        
        # Add distance annotations for Dijkstra
        if step_data.distances:
            for node, distance in step_data.distances.items():
                if node in node_annotations:
                    node_annotations[node] = f"{distance:.1f}"
        
        return {
            "node_colors": node_colors,
            "node_annotations": node_annotations,
            "current_node": step_data.current_node,
            "visited_nodes": step_data.visited_nodes,
            "frontier_nodes": step_data.frontier_nodes,
            "cost": step_data.cost,
            "metadata": step_data.metadata
        }
    
    def export_history(self) -> Dict[str, Any]:
        """
        Export the complete execution history in a structured format.
        
        Returns:
            Dictionary containing all step data and metadata
        """
        steps_data = []
        for step in self.steps:
            steps_data.append({
                "step_number": step.step_number,
                "algorithm_name": step.algorithm_name,
                "current_node": step.current_node,
                "visited_nodes": step.visited_nodes,
                "frontier_nodes": step.frontier_nodes,
                "distances": step.distances,
                "parent_map": step.parent_map,
                "cost": step.cost,
                "metadata": step.metadata,
                "timestamp": step.timestamp
            })
        
        return {
            "algorithm_name": self.algorithm_name,
            "start_time": self.start_time.isoformat(),
            "total_steps": len(self.steps),
            "steps": steps_data
        }
    
    def export_to_json(self, filepath: str) -> None:
        """
        Export execution history to a JSON file.
        
        Args:
            filepath: Path to save the JSON file
        """
        history = self.export_history()
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
    
    def import_from_json(self, filepath: str) -> None:
        """
        Import execution history from a JSON file.
        
        Args:
            filepath: Path to the JSON file to import
        """
        with open(filepath, 'r') as f:
            history = json.load(f)
        
        self.algorithm_name = history.get("algorithm_name", self.algorithm_name)
        self.steps.clear()
        
        for step_dict in history.get("steps", []):
            step_data = StepData(
                step_number=step_dict["step_number"],
                algorithm_name=step_dict["algorithm_name"],
                current_node=step_dict.get("current_node"),
                visited_nodes=step_dict.get("visited_nodes", []),
                frontier_nodes=step_dict.get("frontier_nodes", []),
                distances=step_dict.get("distances", {}),
                parent_map=step_dict.get("parent_map", {}),
                cost=step_dict.get("cost", 0.0),
                metadata=step_dict.get("metadata", {}),
                timestamp=step_dict.get("timestamp", 0.0)
            )
            self.steps.append(step_data)
        
        self.current_step_index = len(self.steps) - 1 if self.steps else -1
    
    def reset(self) -> None:
        """Reset the step tracker to initial state."""
        self.steps.clear()
        self.current_step_index = -1
        self.start_time = datetime.now()
    
    def get_execution_time(self) -> float:
        """
        Get the total execution time in seconds.
        
        Returns:
            Execution time in seconds
        """
        if not self.steps:
            return 0.0
        
        first_step_time = self.steps[0].timestamp
        last_step_time = self.steps[-1].timestamp
        
        return last_step_time - first_step_time
    
    def get_step_metrics(self, step_num: int) -> Dict[str, Any]:
        """
        Get metrics for a specific step.
        
        Args:
            step_num: Step number
            
        Returns:
            Dictionary containing step metrics
        """
        step_data = self.get_step(step_num)
        if not step_data:
            return {}
        
        return {
            "step_number": step_data.step_number,
            "visited_count": len(step_data.visited_nodes),
            "frontier_count": len(step_data.frontier_nodes),
            "cost": step_data.cost,
            "current_node": step_data.current_node
        }
    
    def get_algorithm_metrics(self) -> Dict[str, Any]:
        """
        Get overall algorithm execution metrics.
        
        Returns:
            Dictionary containing algorithm metrics
        """
        if not self.steps:
            return {
                "algorithm_name": self.algorithm_name,
                "total_steps": 0,
                "execution_time": 0.0,
                "final_cost": 0.0
            }
        
        final_step = self.steps[-1]
        
        return {
            "algorithm_name": self.algorithm_name,
            "total_steps": len(self.steps),
            "execution_time": self.get_execution_time(),
            "final_cost": final_step.cost,
            "final_visited_count": len(final_step.visited_nodes)
        }
    
    def __repr__(self) -> str:
        return (f"StepTracker(algorithm={self.algorithm_name}, "
                f"steps={len(self.steps)}, current={self.current_step_index})")
    
    def __str__(self) -> str:
        return (f"Step Tracker: {self.algorithm_name} - "
                f"{len(self.steps)} steps recorded, "
                f"current step: {self.current_step_index}")
