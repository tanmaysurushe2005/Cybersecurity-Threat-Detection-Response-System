"""
Performance tracking and measurement utilities for algorithm execution.
Provides timing, comparison, and reporting capabilities.
"""

import time
from typing import Dict, Optional


class PerformanceTracker:
    """
    Tracks and reports algorithm execution performance metrics.
    Records execution times for labeled operations and provides comparison utilities.
    """

    def __init__(self) -> None:
        """Initialize performance tracker with empty results."""
        self._timers: Dict[str, float] = {}
        self._results: Dict[str, float] = {}

    def start(self, label: str) -> None:
        """
        Start timing an operation.

        Args:
            label: Unique identifier for the operation being timed
        """
        self._timers[label] = time.perf_counter()

    def stop(self, label: str) -> float:
        """
        Stop timing an operation and record elapsed time.

        Args:
            label: Identifier matching a previous start() call

        Returns:
            Elapsed time in seconds since start() was called for this label

        Raises:
            KeyError: If label was not started
        """
        if label not in self._timers:
            raise KeyError(f"Timer '{label}' was not started")

        elapsed = time.perf_counter() - self._timers[label]
        self._results[label] = elapsed
        del self._timers[label]
        return elapsed

    def get_results(self) -> Dict[str, float]:
        """
        Retrieve all recorded timing results.

        Returns:
            Dictionary mapping operation label to elapsed time in seconds
        """
        return self._results.copy()

    def format_all(self) -> str:
        """
        Format all results as human-readable string.

        Returns:
            Multi-line string with one result per line, formatted as "  label: Xms" or "  label: X.XXs"
        """
        if not self._results:
            return "No timing results recorded"

        lines = []
        for label in sorted(self._results.keys()):
            elapsed = self._results[label]
            if elapsed < 1:
                formatted = f"  {label}: {elapsed * 1000:.0f}ms"
            else:
                formatted = f"  {label}: {elapsed:.2f}s"
            lines.append(formatted)

        return "\n".join(lines)

    def compare(self, other: "PerformanceTracker") -> Dict[str, tuple]:
        """
        Compare timing results with another tracker.

        Args:
            other: Another PerformanceTracker instance to compare against

        Returns:
            Dictionary mapping label to (self_time, other_time, diff_pct) tuples.
            diff_pct is positive if self is slower, negative if self is faster.
            Returns only labels present in both trackers.
        """
        comparison = {}
        common_labels = set(self._results.keys()) & set(other._results.keys())

        for label in common_labels:
            self_time = self._results[label]
            other_time = other._results[label]

            if other_time == 0:
                diff_pct = 0.0 if self_time == 0 else float("inf")
            else:
                diff_pct = ((self_time - other_time) / other_time) * 100

            comparison[label] = (self_time, other_time, diff_pct)

        return comparison

    def reset(self) -> None:
        """Clear all recorded results."""
        self._results.clear()
        self._timers.clear()

    def get(self, label: str) -> Optional[float]:
        """
        Get timing result for a specific label.

        Args:
            label: Operation label

        Returns:
            Elapsed time in seconds, or None if not recorded
        """
        return self._results.get(label)

    def __repr__(self) -> str:
        return f"PerformanceTracker(results={len(self._results)}, active={len(self._timers)})"

    def __str__(self) -> str:
        return self.format_all()
