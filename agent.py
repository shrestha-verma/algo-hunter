import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient
import json_repair

load_dotenv()

NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

nebius_client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=NEBIUS_API_KEY
)

tavily_client = None
if TAVILY_API_KEY:
    try:
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    except Exception:
        tavily_client = None

def get_tavily_target_companies(pattern: str, topic: str) -> list:
    default_companies = ["Google", "Amazon", "Meta", "Uber"]
    if not tavily_client:
        return default_companies

    try:
        res = tavily_client.search(
            query=f"LeetCode interview companies hiring {pattern} {topic}",
            max_results=2
        )
        raw_text = " ".join([r.get("content", "") for r in res.get("results", [])])
        detected = [c for c in ["Google", "Meta", "Amazon", "Microsoft", "Uber", "Apple"] if c.lower() in raw_text.lower()]
        return list(set(detected))[:4] if detected else default_companies
    except Exception:
        return default_companies

SYSTEM_PROMPT = """You are Algo Hunter, the ultimate visual algorithmic mentor powered by NVIDIA Nemotron on Nebius Token Factory.
Your core teaching philosophy: "Intuitive physical workflow comes FIRST, code syntax comes second."

STRICT PEDAGOGICAL DIRECTIVES:

1. MANDATORY 5 TO 7 EXECUTION STEPS:
   - "execution_trace" MUST contain 5 to 7 sequential steps simulating loop progression.
   - For 1D Arrays & Lists: "data_elements" is the array/list values.
   - For Strings: "data_elements" is the list of individual characters.
   - For 2D Matrices: "data_elements" is the entire 2D matrix (list of lists).
   - "active_indices" MUST map pointer names strictly to ZERO-BASED integer indices (e.g., first element is 0, second is 1). NEVER use 1-based indices!
   - "variables" MUST NEVER BE EMPTY {}. Include live snapshot of all pointers, cell values, and boolean flags (e.g. {"first": 0, "second": 3, "first_val": 1, "second_val": 1, "match": true}).

2. DETAILED 3-PART SOCRATIC STEP REASONING:
   In EVERY step's "action_explanation", reference exact variable names, numbers, characters, indices, and decisions:
   - [Observation]: State current pointer positions, active indices, values under inspection, and accumulators.
   - [The Conflict / Bottleneck]: State the exact conditional check, while-loop bound, or comparison evaluated at this step.
   - [The Action]: Explain why a specific pointer shifts, why search space safely reduces, or why items match/mismatch.

3. AUTONOMOUS INPUT SYNTHESIS:
   - If user input context is empty or blank, synthesize a canonical realistic test array/string/matrix and trace it.
   - If user provides custom input, strictly run the trace on their provided data!

4. FULL AND UNTRUNCATED CODE RESOLUTION:
   - In "final_solution", provide complete, clean, compilable implementation in "code", plus conceptual intuition in "explanation". NEVER truncate the code.

5. DYNAMIC INTERVIEW CHALLENGES WITH LEETCODE EXAMPLES:
   - Provide 2 relevant interview challenges in "suggested_questions".
   - In "description", include clear problem statement AND canonical example: e.g. "Example 1: Input: head = [1, 2, 2, 1] -> Output: true".
   - "context" MUST be the exact input test string to run immediately: e.g. "head = [1, 2, 2, 1]".
   - "starter_code": A clean starter function template.
   - "constraints": Exact bounds.

OUTPUT SCHEMA (RAW JSON ONLY, DO NOT USE MARKDOWN TICKS):
{
  "problem_name": "Accurate Problem Title",
  "topic": "Primary Category (e.g., Linked Lists, Arrays, Matrix)",
  "subtopic_pattern": "Specific Pattern (e.g., Two Pointers, Fast & Slow Pointers)",
  "time_complexity": "O(...)",
  "space_complexity": "O(...)",
  "hints": {
    "hint_1": "Intuitive physical analogy nudge.",
    "hint_2": "The mathematical invariant or decision boundary."
  },
  "final_solution": {
    "explanation": "Deep intuitive conceptual breakdown explaining the visual workflow.",
    "code": "// Clean complete optimal production-grade code"
  },
  "mindmap_node": {
    "category": "Topic",
    "pattern": "Pattern",
    "mastery_status": "Mastered"
  },
  "execution_trace": [
    {
      "step": 1,
      "line": 5,
      "state_description": "Comparing symmetry of elements",
      "data_elements": [1, 2, 2, 1],
      "active_indices": {"first": 0, "second": 3},
      "variables": {"first": 0, "second": 3, "val1": 1, "val2": 1, "match": true},
      "action_explanation": "[Observation]: First pointer at index 0 (val 1), second pointer at index 3 (val 1). [The Conflict / Bottleneck]: Checking if first->val == second->val. [The Action]: Values match; advance first to index 1 and retreat second to index 2."
    }
  ],
  "suggested_questions": [
    {
      "title": "Palindrome Linked List",
      "company": "Amazon",
      "difficulty": "Easy",
      "description": "Given head of singly linked list, return true if it is a palindrome.\\nExample: Input: head = [1, 2, 2, 1] -> Output: true",
      "constraints": "1 <= Node.val <= 9, O(n) time, O(1) space",
      "starter_code": "bool isPalindrome(ListNode* head) {\\n    // your logic\\n}",
      "context": "head = [1, 2, 2, 1]"
    }
  ]
}
"""

def call_nemotron(messages: list) -> dict:
    response = nebius_client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=8192
    )
    msg_content = response.choices[0].message.content
    raw_content = (msg_content or "{}").strip()
    return json_repair.loads(raw_content)

def analyze_dsa_code(code_snippet: str, problem_context: str = "") -> dict:
    try:
        if not code_snippet or len(code_snippet.strip()) < 5:
            return {"error": "Code snippet is too short or empty. Please enter valid code."}

        ctx = (problem_context or "").strip()
        if not ctx:
            ctx_instruction = "No input array provided by user. Autonomously synthesize a canonical test array/string/matrix for this algorithm and trace it."
        else:
            ctx_instruction = f"User provided input context & constraints:\n{ctx}"

        user_content = (
            f"Algorithm Code to Trace:\n{code_snippet}\n\n"
            f"Input Context:\n{ctx_instruction}\n\n"
            f"MANDATORY REQUIREMENT:\n"
            f"1. Generate between 5 and 7 sequential execution steps in 'execution_trace'.\n"
            f"2. For strings, 'data_elements' MUST be the list of characters (e.g. ['r', 'a', 'c', 'e', ...]), NEVER numbers.\n"
            f"3. In every step's 'action_explanation', use [Observation], [The Conflict / Bottleneck], and [The Action] with exact variable values and indices.\n"
            f"4. In 'final_solution', output the COMPLETE optimal implementation in 'code' without truncating."
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
        
        data = call_nemotron(messages)

        # STRICT AGENTIC SELF-CORRECTION
        trace = data.get("execution_trace", [])
        if not trace or len(trace) < 5:
            retry_prompt = (
                f"CRITICAL ERROR: Your 'execution_trace' only returned {len(trace)} steps! "
                "The system requires between 5 and 7 steps minimum to properly visualize algorithm execution. "
                "Simulate the loop iterations across 5 to 7 steps with full [Observation], [The Conflict / Bottleneck], [The Action]. "
                "Regenerate the JSON immediately with at least 5 steps."
            )
            messages.append({"role": "assistant", "content": json.dumps(data)})
            messages.append({"role": "user", "content": retry_prompt})
            data = call_nemotron(messages)

        if not data.get("problem_name"):
            fn_match = re.search(r'(?:def|void|int|vector<[^>]+>|bool)\s+([a-zA-Z0-9_]+)\s*\(', code_snippet)
            data["problem_name"] = fn_match.group(1).replace("_", " ").title() if fn_match else "DSA Algorithm"

        if not data.get("topic"):
            data["topic"] = "Data Structures"

        if not data.get("subtopic_pattern"):
            data["subtopic_pattern"] = "Algorithm Simulation"

        data["company_tags"] = get_tavily_target_companies(
            data.get("subtopic_pattern", "Algorithm"),
            data.get("topic", "Data Structures")
        )
        
        return data

    except Exception as e:
        print(f"[Engine Error in analyze_dsa_code]: {e}")
        return {"error": f"Engine Error: {str(e)}"}