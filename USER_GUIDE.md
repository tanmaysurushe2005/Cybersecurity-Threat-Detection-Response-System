# How to Use the Cybersecurity Threat Detection System - Complete User Guide

## What is This Project?

This project demonstrates 7 different graph algorithms through an interactive cybersecurity threat simulation. Instead of just learning algorithms from textbooks, you can:
- Create a network (nodes = computers, edges = connections)
- Run different algorithms on this network
- Watch step-by-step how each algorithm works
- See which algorithm is best for different scenarios

Think of it like a network of connected computers, and we're trying to find threats, optimal paths, or best mitigation strategies using different algorithmic approaches.

---

## Getting Started - 3 Easy Steps

### Step 1: Install & Launch
```
cd daa
python run.py
```
This opens the application in your browser at http://localhost:8502

### Step 2: Create a Network
Go to the **Network** tab → Click "✨ Create Network" button

### Step 3: Run an Algorithm
Go to the **Control** tab → Select an algorithm → Click "Run Algorithm"

---

## Tab-by-Tab Explanation

---

## 📍 TAB 1: NETWORK (Create & Visualize)

### Purpose
This is where you create and visualize your network of computers/nodes.

### What You See
- **Network Visualization:** A graph showing all computers (green dots) connected by lines (network connections)
- **Network Metrics:** 
  - Nodes: Number of computers
  - Edges: Number of connections
  - Density: How connected the network is (0-1, higher = more connected)
  - Avg Degree: Average connections per computer

### How to Use

#### Step 1: Set Network Parameters
```
Number of Nodes: 20 (try 10-50 for good visualization)
Topology: Choose from:
  - "random": Computers randomly connected
  - "scale-free": Few powerful computers, many weak ones (like real networks)
  - "small-world": Connected clusters (like real social networks)
```

#### Step 2: Create Network
Click **"✨ Create Network"** button → Wait for creation → You'll see the network graph

#### Step 3: View Network Stats
Below the graph, you'll see:
- Total computers in network
- Total connections
- Network connectivity (0.3 = 30% possible connections exist)
- Average number of connections per computer

#### Step 4: Reset When Needed
Click **"🔄 Reset Network"** to delete the current network and create a new one

### Example
```
"I want to simulate a company with 25 computers in a realistic structure"
→ Nodes: 25
→ Topology: small-world (realistic - departments are clusters)
→ Click Create Network
→ You see 25 computers with realistic connections visualized
```

---

## ⚙️ TAB 2: CONTROL (Run Algorithms)

### Purpose
This is where you SELECT which algorithm to run and CONFIGURE its parameters.

### What Happens
1. Check if network exists (must create network first)
2. Choose an algorithm
3. Set algorithm-specific parameters
4. Run the algorithm

### Available Algorithms

#### A) BFS (Breadth-First Search) - "Spreading in Waves"

**What it does:** Explores the network level-by-level, like a virus spreading in waves of distance.

**Parameters:**
- Start Node: Which computer is the origin? (e.g., "node_0")

**Real-world use:** 
- "How far can a virus spread from computer X?"
- "What computers are within 3 hops from this one?"

**How to use:**
```
Select: BFS
Start Node: node_0 (choose from dropdown)
Click: Run Algorithm
→ BFS explores starting from node_0, checking all neighbors, 
  then their neighbors, layer by layer
→ Results show which computers were reached
```

#### B) DFS (Depth-First Search) - "Deep Exploration"

**What it does:** Goes deep into one path before backtracking, like digging deep to find hidden threats.

**Parameters:**
- Start Node: Which computer to start from?

**Real-world use:**
- "Find all paths from one computer to another"
- "Detect cycles in network (could indicate attack loops)"

**How to use:**
```
Select: DFS
Start Node: node_5
Click: Run Algorithm
→ DFS goes deep into one branch, explores completely,
  then backtracks and explores another branch
→ Results show visited order
```

#### C) Dijkstra - "Optimal Path Finder"

**What it does:** Finds the SHORTEST PATH between two computers, considering distance/cost.

**Parameters:**
- Start Node: Where to start from?
- End Node: Where to reach?

**Real-world use:**
- "What's the fastest route for data to travel from server A to server B?"
- "Route incident response team through network optimally"

**How to use:**
```
Select: Dijkstra
Start Node: node_0
End Node: node_15
Click: Run Algorithm
→ Dijkstra finds the best path from node_0 to node_15
→ Results show: shortest distance, optimal path, steps taken
```

#### D) Greedy - "Fastest Decision Making"

**What it does:** Makes quick local decisions to mitigate threats. Not always perfect, but very fast.

**Parameters:**
- Budget: How much money/resources to spend? (e.g., 5000)

**Real-world use:**
- "During an active attack, patch the highest-risk vulnerabilities first"
- "With limited budget, which systems to protect first?"

**How to use:**
```
Select: Greedy
Budget: 5000
Click: Run Algorithm
→ Greedy algorithm selects highest-priority threats within budget
→ Results show: which systems patched, total cost, risk reduced
→ NOTE: Fast but not guaranteed optimal
```

#### E) Knapsack - "Perfect Optimization"

**What it does:** Finds the OPTIMAL selection of items that maximizes value within capacity. Like perfect packing.

**Parameters:**
- Capacity: Maximum resources available? (e.g., 2000)

**Real-world use:**
- "Choose security patches that give maximum protection within storage limit"
- "Select tools to install within budget for maximum security value"

**How to use:**
```
Select: Knapsack
Capacity: 2000
Click: Run Algorithm
→ Knapsack finds the perfect set of security tools/patches
→ Results show: best selections, total value, total cost
→ NOTE: Guaranteed optimal but slower than Greedy
```

#### F) TSP (Traveling Salesman Problem) - "Route Planning"

**What it does:** Finds a good route visiting all locations exactly once with minimum distance.

**Parameters:**
- Start Node: Which computer to start security audit from?

**Real-world use:**
- "Security team needs to physically visit all data centers. What's best route?"
- "Optimal order to audit all systems to minimize travel time"

**How to use:**
```
Select: TSP
Start Node: node_0
Click: Run Algorithm
→ TSP finds a good order to visit all computers starting from node_0
→ Results show: route order, total distance, path visualization
→ NOTE: Uses "nearest neighbor" heuristic - fast but not perfect
```

#### G) Branch & Bound - "Exact Optimization with Pruning"

**What it does:** Searches for the PERFECT solution by being smart about which options to explore.

**Parameters:**
- Budget: Resources available? (e.g., 3000)

**Real-world use:**
- "Find the absolute best way to contain a spreading attack with resource limits"
- "Optimal system isolation strategy"

**How to use:**
```
Select: BranchAndBound
Budget: 3000
Click: Run Algorithm
→ B&B finds the absolute optimal solution
→ Results show: best strategy, systems affected, cost
→ NOTE: Guaranteed optimal but slower, best for important decisions
```

---

## ▶️ TAB 3: ANIMATION (Watch Step-by-Step)

### Purpose
Watch the algorithm execute STEP BY STEP to understand exactly what it's doing.

### What You See
- **Network Graph:** Shows current algorithm state with colored nodes:
  - Green: Normal nodes
  - Yellow: Currently processing node
  - Red: Already visited/processed nodes
- **Step Navigation:**
  - Step number (e.g., "Step 5 of 23")
  - Navigation buttons: First, Previous, Next, Last
  - Slider to jump to any step

### Step Information Display
For each step, you see:
- **Current Node:** Which computer is being processed right now
- **Visited Nodes:** Count of computers already explored
- **Frontier Nodes:** Count of computers waiting to be explored
- **Cost:** Current cost/distance accumulated

### How to Use

#### Option 1: Manual Step-Through
```
1. Click "⏮️ First" to go to step 1
2. Click "Step Slider" and drag to any step
3. Click "⏭️ Last" to jump to final step
→ At each step, see what the algorithm is doing
→ Perfect for understanding the logic
```

#### Option 2: Animated Playback
```
1. Set "Animation Speed" slider (0.5 = slow, 2.0 = fast)
2. Click "▶️ Play" button
→ Watch the algorithm execute automatically
→ Node colors change as it progresses
→ Metrics update in real-time
```

#### Option 3: Stop and Inspect
```
1. Click "▶️ Play" to start animation
2. Click "⏸️ Stop" to pause
3. Move slider to inspect specific step
→ Pause at any point to analyze
```

### Example
```
I ran BFS on a 20-node network starting at node_0

Watching the animation:
Step 1: node_0 is current (yellow), 0 visited, 5 in frontier
Step 2: node_2 is current, 2 visited, 7 in frontier
Step 3: node_5 is current, 3 visited, 6 in frontier
...
Step 15: DONE - All connected nodes visited

I can see exactly how BFS spreads level-by-level!
```

---

## ⚠️ TAB 4: THREATS (Simulate & Monitor)

### Purpose
Simulate cyber threats in the network and track their spread.

### What You Can Do

#### Generate a Threat
```
Threat Type: Choose from DDoS, Intrusion, or Malware
Origin Node: Which computer is attacked? (e.g., node_3)
Severity: How serious? (0.0 = light, 1.0 = critical)
Click: "Generate Threat"
```

#### Watch Threat Statistics
```
Active Threats: How many ongoing threats?
Compromised Nodes: How many computers are affected?
```

#### See Threat List
```
A table showing all active threats with:
- Threat ID (unique identifier)
- Type (DDoS/Intrusion/Malware)
- Severity (0.00 to 1.00)
- Status (Active/Contained)
- Affected Nodes (count of computers impacted)
```

### Example
```
Create network → Generate Threat
Type: Malware
Origin: node_1
Severity: 0.8

Table shows:
ID          Type     Severity  Status   Affected
threat_001  Malware  0.80      Active   7

This means: Malware started at node_1, now affecting 7 computers
```

---

## 📊 TAB 5: ANALYTICS (Performance Metrics)

### Purpose
View detailed performance metrics and visualizations of the algorithm's execution.

### What You See

#### Key Metrics
```
Total Steps: How many steps did algorithm take?
Final Cost: Total cost/distance at end
Nodes Visited: Total computers explored
```

#### Two Charts

**Chart 1: Cost Progression**
- X-axis: Step number (1 to total steps)
- Y-axis: Cost at each step
- Shows how cost changes over time
- Tells you: Is cost increasing/decreasing? How fast?

**Chart 2: Visited Nodes Progression**
- X-axis: Step number
- Y-axis: Count of visited nodes
- Shows how many computers explored at each step
- Tells you: When does exploration accelerate/slow down?

### Example
```
After running Dijkstra on 20-node network:

Total Steps: 25
Final Cost: 87.5
Nodes Visited: 18

Cost Progression Chart:
Step 1: Cost = 0
Step 5: Cost = 15
Step 10: Cost = 45
Step 15: Cost = 65
Step 20: Cost = 82
Step 25: Cost = 87.5
→ Cost increases as we explore more nodes

Visited Nodes Chart:
Step 1: 1 node
Step 5: 4 nodes
Step 10: 10 nodes
Step 15: 15 nodes
Step 25: 18 nodes
→ Explores quickly at first, then slows down
```

---

## Complete Workflow Example

### Scenario: "Test BFS Algorithm on Company Network"

**Step 1: Create Network**
- Go to **Network** tab
- Set: 20 nodes, "small-world" topology
- Click: "✨ Create Network"
- Result: See network visualization with 20 computers

**Step 2: Run Algorithm**
- Go to **Control** tab
- Select: BFS
- Choose Start Node: node_0 (central server)
- Click: "Run Algorithm"
- Result: Algorithm runs and completes

**Step 3: Watch Animation**
- Go to **Animation** tab
- See step info: Step 5 of 20
- Current Node: node_2
- Visited: 5 nodes
- Frontier: 8 nodes
- Click "▶️ Play" to watch full animation
- Colors show: yellow = current, red = visited, green = unvisited

**Step 4: See Results**
- Go to **Analytics** tab
- Total Steps: 20
- Nodes Visited: 18
- View charts showing progression

**Step 5: Create New Test**
- Go back to **Network** tab
- Click "🔄 Reset Network"
- Try different network or algorithm

---

## Quick Reference: Which Algorithm When?

### Need SHORTEST PATH? → Use **Dijkstra**
"I need the fastest route to reach a critical server"

### Need QUICK DECISION? → Use **Greedy**
"Under attack - patch highest-risk items NOW within $5000"

### Need PERFECT SOLUTION? → Use **Knapsack** or **Branch & Bound**
"Choose security tools for maximum protection within $2000"

### Need OPTIMAL ROUTE? → Use **TSP**
"Audit all 15 data centers with minimum travel time"

### Need TO UNDERSTAND SPREAD? → Use **BFS**
"How far does virus spread from this computer?"

### Need DEEP EXPLORATION? → Use **DFS**
"Find all hidden connections and paths"

---

## Tips for Teachers

### Tip 1: Start Simple
```
First lesson: Create 10-node network, run BFS
Students see simple spreading pattern
Easy to understand and visualize
```

### Tip 2: Compare Algorithms
```
Create same 20-node network
Run BFS → observe
Reset and run DFS → compare
Show that both visit all nodes but in different order
```

### Tip 3: Use Real-World Context
```
"This green node is our main server (node_0)"
"This red node is infected with malware"
"BFS shows how virus spreads from red node"
"Students learn algorithm AND cybersecurity concept"
```

### Tip 4: Demonstrate Performance
```
Run BFS on 20-node network → Takes 20 steps
Run same on 50-node network → Takes 50 steps
Show: Time grows with network size
Learn: O(V+E) complexity in practice
```

### Tip 5: Challenge Students
```
"Given this network and $2000 budget, use Knapsack to find
the best security patches to install. Which algorithm found
the most optimal solution?"
```

---

## Common Questions

### Q: Why do different algorithms visit nodes differently?
A: Different strategies:
- BFS: Level-by-level (breadth)
- DFS: Deep then backtrack (depth)
- Dijkstra: Always picks nearest unvisited
- Greedy: Always picks highest priority

### Q: Why does Greedy finish faster but Knapsack is better?
A: Speed vs Optimality trade-off
- Greedy: Quick decision, ~85% optimal
- Knapsack: Takes longer, 100% optimal
Real-world: Choose based on urgency

### Q: What do the node colors mean?
A: 
- Green: Not yet visited
- Yellow: Currently being processed
- Red: Already visited/processed

### Q: Why create different topologies?
A:
- Random: Completely random connections (chaos)
- Scale-free: Few hub servers + many edge servers (realistic)
- Small-world: Clustered communities (like departments)

### Q: Can I create larger networks?
A: Yes! Try 100 nodes, but animation gets slower. Best: 15-30 nodes for clarity.

---

## Troubleshooting

### Problem: "No network created yet!" error appears
Solution: Go to Network tab first and create a network

### Problem: Animation doesn't show colors
Solution: The color changes happen as you play the animation. Use Play button to see.

### Problem: Metrics show 0
Solution: Run an algorithm first by going to Control tab

### Problem: Algorithm takes a long time
Solution: Try smaller network (10 nodes instead of 50)

### Problem: Can't select End Node in Dijkstra
Solution: This means network wasn't created. Go to Network tab and create it first.

---

## Summary

This project teaches graph algorithms through:
1. **Network Tab**: Create and understand the network structure
2. **Control Tab**: Choose algorithms and set parameters
3. **Animation Tab**: Watch step-by-step algorithm execution
4. **Threats Tab**: Simulate real-world security scenarios
5. **Analytics Tab**: View performance metrics and comparisons

Each algorithm solves a different problem with different trade-offs between:
- Speed (how fast to run)
- Optimality (how good the solution is)
- Real-world applicability (does it solve real problems?)

By using this project, students learn not just algorithms, but WHEN to use each one!
