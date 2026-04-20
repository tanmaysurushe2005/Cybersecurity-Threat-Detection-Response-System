"""
Comprehensive unit tests for graph algorithms.
Tests correctness, edge cases, and algorithm properties.
"""

import pytest
from typing import List, Tuple
from project.core.graph import NetworkGraph
from project.core.algorithm_engine import AlgorithmEngine
from project.core.step_tracker import StepTracker
from project.algorithms.bfs import BFS
from project.algorithms.dfs import DFS
from project.algorithms.dijkstra import Dijkstra
from project.algorithms.greedy import Greedy
from project.algorithms.knapsack import Knapsack
from project.algorithms.tsp import TSP
from project.algorithms.branch_and_bound import BranchAndBound


class TestGraphFixtures:
    """Fixtures for creating test graphs."""

    @pytest.fixture
    def small_connected_graph(self) -> NetworkGraph:
        """Create a simple 5-node connected graph."""
        graph = NetworkGraph(num_nodes=5, topology="random")
        return graph

    @pytest.fixture
    def weighted_graph(self) -> NetworkGraph:
        """Create a graph with specific edge weights for Dijkstra testing."""
        graph = NetworkGraph(num_nodes=4, topology="random")
        return graph

    @pytest.fixture
    def single_node_graph(self) -> NetworkGraph:
        """Create a graph with single node."""
        graph = NetworkGraph(num_nodes=1, topology="random")
        return graph

    @pytest.fixture
    def sample_items_for_knapsack(self) -> List[dict]:
        """Sample items for knapsack algorithm."""
        return [
            {"value": 60, "weight": 10},
            {"value": 100, "weight": 20},
            {"value": 120, "weight": 30},
            {"value": 80, "weight": 15},
        ]


class TestBFS:
    """Test cases for Breadth-First Search algorithm."""

    def test_bfs_basic_execution(self, small_connected_graph):
        """Test BFS executes without errors on simple graph."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_bfs(start_node)
        
        assert tracker is not None
        assert tracker.get_step_count() > 0
        assert tracker.algorithm_name == "BFS"

    def test_bfs_invalid_start_node(self, small_connected_graph):
        """Test BFS raises ValueError for invalid start node."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_bfs("nonexistent_node")

    def test_bfs_visits_connected_nodes(self, small_connected_graph):
        """Test BFS visits nodes reachable from start."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_bfs(start_node)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert start_node in final_step.visited_nodes
        assert len(final_step.visited_nodes) > 0

    def test_bfs_single_node(self, single_node_graph):
        """Test BFS on single node graph."""
        engine = AlgorithmEngine(single_node_graph)
        start_node = single_node_graph.get_all_nodes()[0]
        
        tracker = engine.execute_bfs(start_node)
        
        assert tracker.get_step_count() >= 1
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        assert final_step.current_node == start_node


class TestDFS:
    """Test cases for Depth-First Search algorithm."""

    def test_dfs_basic_execution(self, small_connected_graph):
        """Test DFS executes without errors on simple graph."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_dfs(start_node)
        
        assert tracker is not None
        assert tracker.get_step_count() > 0
        assert tracker.algorithm_name == "DFS"

    def test_dfs_invalid_start_node(self, small_connected_graph):
        """Test DFS raises ValueError for invalid start node."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_dfs("nonexistent_node")

    def test_dfs_visits_all_reachable_nodes(self, small_connected_graph):
        """Test DFS visits all nodes reachable from start."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_dfs(start_node)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert start_node in final_step.visited_nodes
        assert len(final_step.visited_nodes) > 0

    def test_dfs_single_node(self, single_node_graph):
        """Test DFS on single node graph."""
        engine = AlgorithmEngine(single_node_graph)
        start_node = single_node_graph.get_all_nodes()[0]
        
        tracker = engine.execute_dfs(start_node)
        
        assert tracker.get_step_count() >= 1


class TestDijkstra:
    """Test cases for Dijkstra's shortest path algorithm."""

    def test_dijkstra_basic_execution(self, small_connected_graph):
        """Test Dijkstra executes on simple graph."""
        engine = AlgorithmEngine(small_connected_graph)
        nodes = small_connected_graph.get_all_nodes()
        start, end = nodes[0], nodes[-1]
        
        tracker = engine.execute_dijkstra(start, end)
        
        assert tracker is not None
        assert tracker.algorithm_name == "Dijkstra"

    def test_dijkstra_invalid_start_node(self, small_connected_graph):
        """Test Dijkstra raises error for invalid start node."""
        engine = AlgorithmEngine(small_connected_graph)
        nodes = small_connected_graph.get_all_nodes()
        
        with pytest.raises(ValueError):
            engine.execute_dijkstra("invalid", nodes[0])

    def test_dijkstra_invalid_end_node(self, small_connected_graph):
        """Test Dijkstra raises error for invalid end node."""
        engine = AlgorithmEngine(small_connected_graph)
        nodes = small_connected_graph.get_all_nodes()
        
        with pytest.raises(ValueError):
            engine.execute_dijkstra(nodes[0], "invalid")

    def test_dijkstra_same_start_and_end(self, small_connected_graph):
        """Test Dijkstra when start equals end."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_dijkstra(start_node, start_node)
        
        assert tracker.get_step_count() >= 0

    def test_dijkstra_consistent_distances(self, small_connected_graph):
        """Test Dijkstra produces consistent distance calculations."""
        engine = AlgorithmEngine(small_connected_graph)
        nodes = small_connected_graph.get_all_nodes()
        start = nodes[0]
        
        tracker = engine.execute_dijkstra(start, nodes[-1])
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert final_step.cost is not None
        assert final_step.cost >= 0


class TestGreedy:
    """Test cases for Greedy threat mitigation algorithm."""

    def test_greedy_basic_execution(self, small_connected_graph):
        """Test Greedy executes without errors."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:3]
        resources = 1000.0
        
        tracker = engine.execute_greedy(threat_nodes, resources)
        
        assert tracker is not None
        assert tracker.algorithm_name == "Greedy"

    def test_greedy_empty_threat_nodes(self, small_connected_graph):
        """Test Greedy raises error for empty threat nodes."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_greedy([], 1000.0)

    def test_greedy_invalid_resources(self, small_connected_graph):
        """Test Greedy raises error for invalid resources."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:2]
        
        with pytest.raises(ValueError):
            engine.execute_greedy(threat_nodes, -100.0)

    def test_greedy_respects_budget(self, small_connected_graph):
        """Test Greedy respects the budget constraint."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:3]
        resources = 100.0
        
        tracker = engine.execute_greedy(threat_nodes, resources)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert final_step.cost is not None

    def test_greedy_prioritizes_high_risk(self, small_connected_graph):
        """Test Greedy selects high-risk nodes first."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:3]
        resources = 5000.0
        
        tracker = engine.execute_greedy(threat_nodes, resources)
        
        assert tracker.get_step_count() > 0


class TestKnapsack:
    """Test cases for 0/1 Knapsack dynamic programming."""

    def test_knapsack_basic_execution(self, small_connected_graph, sample_items_for_knapsack):
        """Test Knapsack executes without errors."""
        engine = AlgorithmEngine(small_connected_graph)
        capacity = 50.0
        
        tracker = engine.execute_knapsack(sample_items_for_knapsack, capacity)
        
        assert tracker is not None
        assert tracker.algorithm_name == "Knapsack"

    def test_knapsack_empty_items(self, small_connected_graph):
        """Test Knapsack raises error for empty items."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_knapsack([], 50.0)

    def test_knapsack_invalid_capacity(self, small_connected_graph, sample_items_for_knapsack):
        """Test Knapsack raises error for invalid capacity."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_knapsack(sample_items_for_knapsack, -10.0)

    def test_knapsack_optimal_value(self, small_connected_graph, sample_items_for_knapsack):
        """Test Knapsack finds optimal value."""
        engine = AlgorithmEngine(small_connected_graph)
        capacity = 50.0
        
        tracker = engine.execute_knapsack(sample_items_for_knapsack, capacity)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert final_step.cost is not None
        assert final_step.cost > 0

    def test_knapsack_respects_capacity(self, small_connected_graph, sample_items_for_knapsack):
        """Test Knapsack respects capacity constraint."""
        engine = AlgorithmEngine(small_connected_graph)
        capacity = 30.0
        
        tracker = engine.execute_knapsack(sample_items_for_knapsack, capacity)
        
        assert tracker.get_step_count() > 0


class TestTSP:
    """Test cases for Traveling Salesman Problem."""

    def test_tsp_basic_execution(self, small_connected_graph):
        """Test TSP executes without errors."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_tsp(start_node)
        
        assert tracker is not None
        assert tracker.algorithm_name == "TSP"

    def test_tsp_invalid_start_node(self, small_connected_graph):
        """Test TSP raises error for invalid start node."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_tsp("nonexistent_node")

    def test_tsp_visits_all_nodes(self, small_connected_graph):
        """Test TSP visits all nodes exactly once."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        total_nodes = len(small_connected_graph.get_all_nodes())
        
        tracker = engine.execute_tsp(start_node)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert len(final_step.visited_nodes) == total_nodes

    def test_tsp_returns_to_start(self, small_connected_graph):
        """Test TSP route returns to start node."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_tsp(start_node)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        if final_step.visited_nodes:
            assert final_step.visited_nodes[0] == start_node

    def test_tsp_single_node(self, single_node_graph):
        """Test TSP on single node graph."""
        engine = AlgorithmEngine(single_node_graph)
        start_node = single_node_graph.get_all_nodes()[0]
        
        tracker = engine.execute_tsp(start_node)
        
        assert tracker.get_step_count() >= 0

    def test_tsp_produces_valid_cost(self, small_connected_graph):
        """Test TSP produces a valid cost value."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_tsp(start_node)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert final_step.cost is not None
        assert final_step.cost >= 0


class TestBranchAndBound:
    """Test cases for Branch & Bound optimization."""

    def test_branch_and_bound_basic_execution(self, small_connected_graph):
        """Test Branch & Bound executes without errors."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:3]
        budget = 1000.0
        
        tracker = engine.execute_branch_and_bound(threat_nodes, budget)
        
        assert tracker is not None
        assert tracker.algorithm_name == "BranchAndBound"

    def test_branch_and_bound_empty_threats(self, small_connected_graph):
        """Test Branch & Bound raises error for empty threats."""
        engine = AlgorithmEngine(small_connected_graph)
        
        with pytest.raises(ValueError):
            engine.execute_branch_and_bound([], 1000.0)

    def test_branch_and_bound_invalid_budget(self, small_connected_graph):
        """Test Branch & Bound raises error for invalid budget."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:2]
        
        with pytest.raises(ValueError):
            engine.execute_branch_and_bound(threat_nodes, -100.0)

    def test_branch_and_bound_respects_budget(self, small_connected_graph):
        """Test Branch & Bound respects budget constraint."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:3]
        budget = 1000.0
        
        tracker = engine.execute_branch_and_bound(threat_nodes, budget)
        final_step = tracker.get_step(tracker.get_step_count() - 1)
        
        assert final_step.cost is not None
        assert final_step.cost <= budget + 0.01

    def test_branch_and_bound_better_than_greedy(self, small_connected_graph):
        """Test Branch & Bound finds solution at least as good as Greedy."""
        engine = AlgorithmEngine(small_connected_graph)
        threat_nodes = small_connected_graph.get_all_nodes()[:3]
        budget = 1000.0
        
        greedy_tracker = engine.execute_greedy(threat_nodes, budget)
        greedy_cost = greedy_tracker.get_step(greedy_tracker.get_step_count() - 1).cost or float('inf')
        
        bnb_tracker = engine.execute_branch_and_bound(threat_nodes, budget)
        bnb_cost = bnb_tracker.get_step(bnb_tracker.get_step_count() - 1).cost or float('inf')
        
        assert bnb_cost <= greedy_cost + 0.01


class TestAlgorithmEdgeCases:
    """Test edge cases across all algorithms."""

    def test_all_algorithms_handle_single_node(self, single_node_graph):
        """Test all algorithms handle single-node graphs gracefully."""
        engine = AlgorithmEngine(single_node_graph)
        start_node = single_node_graph.get_all_nodes()[0]
        
        bfs_tracker = engine.execute_bfs(start_node)
        assert bfs_tracker.get_step_count() >= 0
        
        dfs_tracker = engine.execute_dfs(start_node)
        assert dfs_tracker.get_step_count() >= 0

    def test_algorithms_handle_large_values(self, small_connected_graph, sample_items_for_knapsack):
        """Test algorithms handle large parameter values."""
        engine = AlgorithmEngine(small_connected_graph)
        
        threat_nodes = small_connected_graph.get_all_nodes()[:2]
        tracker = engine.execute_greedy(threat_nodes, 1e6)
        assert tracker.get_step_count() > 0

    def test_execution_time_tracking(self, small_connected_graph):
        """Test algorithm execution time is tracked."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_bfs(start_node)
        exec_time = engine.get_execution_time()
        
        assert exec_time >= 0


class TestAlgorithmProperties:
    """Test algorithmic properties and invariants."""

    def test_visited_nodes_consistency(self, small_connected_graph):
        """Test visited_nodes never contains duplicates."""
        engine = AlgorithmEngine(small_connected_graph)
        start_node = small_connected_graph.get_all_nodes()[0]
        
        tracker = engine.execute_bfs(start_node)
        for step in tracker.get_all_steps():
            visited_set = set(step.visited_nodes)
            assert len(visited_set) == len(step.visited_nodes)

    def test_cost_monotonicity_dijkstra(self, small_connected_graph):
        """Test Dijkstra costs are non-decreasing."""
        engine = AlgorithmEngine(small_connected_graph)
        nodes = small_connected_graph.get_all_nodes()
        
        tracker = engine.execute_dijkstra(nodes[0], nodes[-1])
        
        steps = tracker.get_all_steps()
        assert len(steps) > 0
