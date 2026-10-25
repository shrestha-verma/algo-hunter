# Algo Hunter 
> Autonomous Algorithmic Reasoning Engine & Interactive Visual Memory Stepper
> Built for the Devpost Coding & Agentic Engineering Track

---

##  The Genesis & Why We Built This

Let’s be honest: the traditional way software engineers prepare for Data Structures & Algorithms interviews is fundamentally broken. 

You open LeetCode, pick a medium Two-Pointer or Dynamic Programming problem, get stuck within 10 minutes, and immediately jump to the "Solutions" tab or watch a video explanation. What happens? You passively memorize the syntax. You convince yourself you understand the problem because the solution compiles. But the second an interviewer tweaks a boundary condition or asks you to dry-run an edge case on a whiteboard, your mental model completely collapses. 

Traditional platforms suffer from two major flaws:
1. Spoon-feeding code editors that dump complete code solutions right in front of you, killing the struggle where actual learning happens.
2. Abstract theoretical explanations that tell you what the algorithm does at a high level, but fail to show you where memory pointers are actually moving in physical space across each loop iteration.

We built Algo Hunter to bridge this exact gap. Our vision was simple: Intuitive physical workflow must come first; syntax comes second. 

Algo Hunter acts as an autonomous visual engineering mentor. When you feed it custom code or a standard algorithm, it doesn't just evaluate syntax. Instead, it extracts the loop invariants, simulates runtime memory frames step-by-step, highlights pointers directly on live data structures (1D arrays, strings, 2D matrices, linked lists), and prompts you with calibrated hints so you reach the solution through your own reasoning.

---

##  Architectural Philosophy & How It Works

Rather than executing raw untrusted code inside an unsafe local sandbox, Algo Hunter uses an LLM-driven Abstract Syntax Tree (AST) & runtime state synthesis pipeline.

Execution Flow:
[User Code / Buggy Logic] + [Optional Custom Context]
          │
          ▼
[FastAPI Backend Orchestrator]
          │
  ┌───────┴───────────────────────┐
  ▼                               ▼
[Nebius Token Factory]    [Tavily Search Engine]
(NVIDIA Nemotron 120B)    (Live Company Radar)
  │                               │
  ▼                               ▼
[Structured JSON State Machine]   [Real-time Interview Insights]
(Visual Tracing & Socratic Hints)
  │
  ▼
[Frontend: Monaco Editor + Interactive Memory Stepper + Mermaid.js Brain]

1. Autonomous Input Synthesis: If an engineer pastes raw logic without test inputs, the agent synthesizes canonical inputs (e.g., sorted arrays, palindromic strings, boundary-tested matrices) automatically. If custom input is provided, the agent strictly runs the simulation against that data.
2. Memory Frame Stepping: The engine breaks down the algorithm into 5 to 7 sequential logical milestones, capturing exact variable values, active indices, and pointer states at each frame.
3. Continuous Knowledge Construction: Every tackled problem is indexed into a persistent SQLite database, automatically updating the learner’s visual Mind Map without manual note-taking.

---

##  Tech Stack & Implementation Details

1. Nebius Token Factory & NVIDIA Nemotron (nvidia/nemotron-3-super-120b-a12b):
The backbone of Algo Hunter's reasoning is NVIDIA Nemotron 120B, accessed via Nebius Token Factory.
- Why Nebius? When building an interactive visual stepper, latency is everything. If the user waits 20 seconds for an analysis to generate, the fluid learning loop breaks. Nebius Token Factory provided ultra-low inference latency with a clean OpenAI-compatible SDK endpoint, letting us stream and parse heavy reasoning workloads seamlessly.
- Why NVIDIA Nemotron? Simulating pointer mechanics requires strict spatial reasoning and zero hallucination on index bounds (keeping track of low, high, mid, top, bottom, left, right across complex loops). Nemotron excelled at following strict structured JSON output schemas without corrupting arrays or truncating production-grade code snippets.

2. Tavily Search API:
Algorithms don't exist in a vacuum; hiring bars differ across companies. We integrated Tavily Web Search API to fetch live interview relevance on the fly. When a user solves a problem like "Spiral Matrix" or "Palindrome Linked List", Tavily pulls actual historical interview trends from firms like Google, Amazon, and Meta, presenting targeted challenges with canonical constraints directly in the UI.

3. FastAPI & SQLite3 (Backend Orchestration):
- FastAPI: Delivers lightning-fast asynchronous request handling and clean REST endpoints (/analyze, /user/{username}/history).
- SQLite Persistence: Stores comprehensive problem records, mastery statuses, user workspaces, and complexity benchmarks locally without the overhead of heavy external database clusters.

4. Monaco Editor, Tailwind CSS & Mermaid.js (Frontend):
- Monaco Editor: We brought the exact code engine that powers VS Code directly into the browser, complete with syntax highlighting and automatic language detection across C++, Python, and Java.
- Mermaid.js: Powering our Cumulative Knowledge Graph. It converts historical problem sets into an interactive, multi-layered visual DAG representing the learner's evolving mental map.

---

##  Deep Dive Into Core Components

1. Monaco Code Arena:
A full-featured code environment allowing learners to paste raw algorithms, buggy prototypes, or clean solutions. It automatically detects C++, Python, and Java syntax, and features an autonomous test input box capable of handling 1D arrays, string literals, and nested 2D matrices.

2. Visual Execution Tracer (Memory Stepper):
The crown jewel of Algo Hunter. Instead of reading standard terminal logs or debugger dumps:
- For 1D Arrays & Strings: Renders visual memory boxes with live pointer tags (LEFT, RIGHT, SLOW, FAST, MID) floating above elements.
- For 2D Matrices: Renders an interactive coordinate grid tracking boundary shrinking (TOP, BOTTOM, LEFT, RIGHT) in real time.
- Navigation Controls: Frame-by-frame forward and backward stepping allowing users to observe pointer movement and loop termination at their own pace.

3. Three-Part Algorithmic Step Reasoning:
Every single frame in the memory stepper is paired with structured, color-coded cognitive reasoning:
- [1. Observation]: What pointers and memory values are currently under inspection.
- [2. The Conflict / Bottleneck]: The explicit conditional check, loop boundary, or invariant being evaluated.
- [3. The Action]: Why a pointer shifts, why the search window safely halves, or why elements are swapped.

4. Guided Hints & Progressive Resolution Drawer:
To prevent passive answer-copying:
- Hint 1: An intuitive real-world analogy to trigger mental visual models.
- Hint 2: The underlying mathematical invariant or loop boundary condition.
- Optimal Solution Drawer: Kept intentionally collapsed. When revealed, it displays both the conceptual workflow breakdown and production-grade, optimal code with complete time and space complexity audits.

5. Persistent Cognitive Knowledge Graph ("DSA Brain"):
Learning DSA is cumulative. The mind map dynamically connects problems into Topic -> Pattern -> Concrete Problem hierarchies. It provides multi-user workspace isolation (via a workspace switcher), meaning multiple learners can maintain their distinct knowledge graphs on the same machine.

6. Tavily Interview Question Radar:
Presents real-world interview context cards showing company tags, problem descriptions, and test constraints. Clicking "Load Challenge & Inputs" instantly populates both the Monaco Editor with a starter template and the input box with target test cases.

---

## Getting Started Locally

Prerequisites:
- Python 3.10 or higher
- Git

Installation Steps:
1. Clone the repository:
   git clone https://github.com/shrestha-verma/algo-hunter.git
   cd algo-hunter

2. Install Python dependencies:
   pip install -r requirements.txt

3. Configure Environment Keys:
   Create a .env file in the root directory:
   NEBIUS_API_KEY=your_nebius_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here

4. Run the server:
   python main.py
   Open your browser and navigate to http://localhost:8000

---

## 🛡️ Security Architecture Note

Algo Hunter does not rely on unsafe client-side or server-side eval() or exec() calls. User-provided code is never executed directly on the host machine. Instead, the algorithm is analyzed symbolically via LLM simulation frames, mitigating arbitrary remote code execution risks while keeping system data completely isolated.

---

## 📜 Open Source License

This project is licensed under the MIT License - see the LICENSE file for details.