"""
Configuration file for Cybersecurity Threat Detection & Response System.
Contains system-wide parameters and constants.
"""

# Network Configuration
MAX_NODES = 1000
DEFAULT_NODES = 20
TOPOLOGY_TYPES = ["random", "scale-free", "small-world"]
DEFAULT_TOPOLOGY = "random"

# Algorithm Configuration
ALGORITHMS = ["BFS", "DFS", "Dijkstra", "Greedy", "Knapsack", "TSP", "BranchAndBound"]
MAX_STEP_HISTORY = 10000

# Threat Configuration
THREAT_TYPES = ["DDoS", "Intrusion", "Malware"]
THREAT_SEVERITY_RANGE = (0.0, 1.0)
THREAT_PROPAGATION_SPEED_RANGE = (0.1, 1.0)

# Visualization Configuration
VISUALIZATION_UPDATE_TIME_MS = 500
MAX_VISUALIZATION_NODES = 1000
NODE_COLORS = {
    "normal": "#90EE90",      # Green
    "infected": "#FF0000",    # Red
    "processing": "#FFFF00",  # Yellow
    "secured": "#0000FF"      # Blue
}

# Performance Configuration
NETWORK_INIT_TIMEOUT_SEC = 5
BFS_DFS_TIMEOUT_SEC = 2
DIJKSTRA_TIMEOUT_SEC = 5
VISUALIZATION_RENDER_TIMEOUT_MS = 500

# Device Types
DEVICE_TYPES = ["server", "workstation", "router", "firewall"]

# Risk Level Range
RISK_LEVEL_RANGE = (0.0, 1.0)

# Bandwidth and Latency Ranges
BANDWIDTH_RANGE = (10, 1000)  # Mbps
LATENCY_RANGE = (1, 100)      # ms

# Mitigation Cost Range
MITIGATION_COST_RANGE = (10, 100)

# Animation Speed Range
ANIMATION_SPEED_RANGE = (0.5, 2.0)
DEFAULT_ANIMATION_SPEED = 1.0
