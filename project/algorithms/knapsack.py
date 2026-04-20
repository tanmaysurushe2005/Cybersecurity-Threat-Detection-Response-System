"""
0/1 Knapsack algorithm implementation for resource allocation optimization.
Maximizes value within capacity constraints using dynamic programming.
"""

from typing import Dict, List, Any

from ..core.graph import NetworkGraph
from ..core.step_tracker import StepTracker
from ..utils.data_structures import StepData


class Knapsack:
    """
    0/1 Knapsack algorithm for optimal resource allocation.
    Uses dynamic programming to maximize value within capacity constraints.
    """
    
    def __init__(self, graph: NetworkGraph, step_tracker: StepTracker):
        """
        Initialize Knapsack algorithm.
        
        Args:
            graph: NetworkGraph object
            step_tracker: StepTracker for recording steps
        """
        self.graph = graph
        self.step_tracker = step_tracker
        self.dp_table: List[List[float]] = []
        self.selected_items: List[int] = []
        self.step_number = 0
    
    def execute(self, items: List[Dict[str, float]], capacity: float) -> None:
        """
        Execute 0/1 Knapsack algorithm.
        
        Args:
            items: List of items with 'value' and 'weight' keys
            capacity: Knapsack capacity
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not items:
            raise ValueError("items cannot be empty")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        # Initialize
        self.selected_items.clear()
        self.step_number = 0
        
        n = len(items)
        capacity_int = int(capacity)
        
        # Create DP table
        self.dp_table = [[0.0 for _ in range(capacity_int + 1)] for _ in range(n + 1)]
        
        # Fill DP table
        for i in range(1, n + 1):
            item = items[i - 1]
            value = item.get('value', 0.0)
            weight = int(item.get('weight', 0.0))
            
            for w in range(capacity_int + 1):
                # Don't include item
                self.dp_table[i][w] = self.dp_table[i - 1][w]
                
                # Include item if it fits
                if weight <= w:
                    include_value = value + self.dp_table[i - 1][w - weight]
                    if include_value > self.dp_table[i][w]:
                        self.dp_table[i][w] = include_value
                
                # Record step
                if i % max(1, n // 10) == 0 or i == n:  # Record every 10% or at end
                    self._record_step(i, w)
        
        # Backtrack to find selected items
        self._backtrack_solution(items, capacity_int)
    
    def _backtrack_solution(self, items: List[Dict[str, float]], capacity: int) -> None:
        """
        Backtrack through DP table to find selected items.
        
        Args:
            items: List of items
            capacity: Knapsack capacity
        """
        n = len(items)
        w = capacity
        
        for i in range(n, 0, -1):
            # If value comes from including this item
            if self.dp_table[i][w] != self.dp_table[i - 1][w]:
                self.selected_items.append(i - 1)
                weight = int(items[i - 1].get('weight', 0.0))
                w -= weight
        
        self.selected_items.reverse()
    
    def _record_step(self, item_index: int, capacity_index: int) -> None:
        """
        Record a step in the algorithm execution.
        
        Args:
            item_index: Current item index
            capacity_index: Current capacity index
        """
        current_value = self.dp_table[item_index][capacity_index] if item_index < len(self.dp_table) else 0.0
        
        step_data = StepData(
            step_number=self.step_number,
            algorithm_name="Knapsack",
            current_node=f"item_{item_index}",
            visited_nodes=[f"item_{i}" for i in range(item_index)],
            frontier_nodes=[],
            cost=current_value,
            metadata={
                "item_index": item_index,
                "capacity_index": capacity_index,
                "current_value": current_value,
                "dp_table_size": len(self.dp_table)
            }
        )
        
        self.step_tracker.record_step(step_data)
        self.step_number += 1
    
    def get_selected_items(self) -> List[int]:
        """
        Get indices of selected items.
        
        Returns:
            List of selected item indices
        """
        return self.selected_items.copy()
    
    def get_total_value(self) -> float:
        """
        Get the total value of selected items.
        
        Returns:
            Total value
        """
        if not self.dp_table:
            return 0.0
        return self.dp_table[-1][-1]
    
    def __repr__(self) -> str:
        return f"Knapsack(selected={len(self.selected_items)}, value={self.get_total_value():.2f})"
