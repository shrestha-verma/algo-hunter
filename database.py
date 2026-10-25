import sqlite3
import json
import os

DB_FILE = "algo_hunter.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problem_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            problem_name TEXT NOT NULL,
            topic TEXT NOT NULL,
            subtopic_pattern TEXT NOT NULL,
            time_complexity TEXT,
            space_complexity TEXT,
            code_snippet TEXT,
            problem_context TEXT,
            hints_json TEXT,
            final_solution_json TEXT,
            execution_trace_json TEXT,
            mastery_status TEXT DEFAULT 'Mastered',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    
    # 1. Register default demo user
    cursor.execute("INSERT OR IGNORE INTO users (username) VALUES ('shrestha')")
    
    # 2. Check if shrestha already has history, agar nahi hai toh 5 demo questions seed kar do
    cursor.execute("SELECT COUNT(*) as cnt FROM problem_history WHERE username = 'shrestha'")
    count = cursor.fetchone()["cnt"]
    
    if count == 0:
        demo_problems = [
            (
                "shrestha", "Two Sum II (Input array is sorted)", "Arrays", "Two Pointers",
                "O(N)", "O(1)",
                "vector<int> twoSum(vector<int>& numbers, int target) {\n    int left = 0, right = numbers.size() - 1;\n    while (left < right) {\n        int sum = numbers[left] + numbers[right];\n        if (sum == target) return {left + 1, right + 1};\n        else if (sum < target) left++;\n        else right--;\n    }\n    return {};\n}",
                "numbers = [2, 7, 11, 15], target = 9",
                json.dumps({"hint_1": "Sorted array allows shrinking search boundaries.", "hint_2": "If sum < target, advance left. If sum > target, decrease right."}),
                json.dumps({"explanation": "Optimal two pointers approach eliminates search space in O(N).", "code": "// Optimal O(N) Two Pointers"}),
                json.dumps([{"step": 1, "line": 2, "state_description": "Initial setup", "data_elements": [2, 7, 11, 15], "active_indices": {"left": 0, "right": 3}, "variables": {"left": 0, "right": 3}, "action_explanation": "[Observation]: Left pointer at 0 (val 2), right pointer at 3 (val 15). [The Conflict / Bottleneck]: Sum is 17 which exceeds target 9. [The Action]: Right pointer decrements inward."}]),
                "Mastered"
            ),
            (
                "shrestha", "Binary Search", "Searching", "Divide and Conquer",
                "O(log N)", "O(1)",
                "def binary_search(nums, target):\n    low, high = 0, len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
                "nums = [-1, 0, 3, 5, 9, 12], target = 9",
                json.dumps({"hint_1": "Divide search window in half at each iteration.", "hint_2": "Monotonicity guarantees target position relative to mid."}),
                json.dumps({"explanation": "Halves search interval each step in logarithmic time.", "code": "# Binary Search Optimal"}),
                json.dumps([{"step": 1, "line": 2, "state_description": "Middle inspection", "data_elements": [-1, 0, 3, 5, 9, 12], "active_indices": {"low": 0, "mid": 2, "high": 5}, "variables": {"low": 0, "mid": 2, "high": 5}, "action_explanation": "[Observation]: Low is 0, High is 5, Mid calculates to 2 (val 3). [The Conflict / Bottleneck]: Target 9 is greater than mid value 3. [The Action]: Eliminate lower half by shifting low to mid + 1."}]),
                "Mastered"
            ),
            (
                "shrestha", "Spiral Matrix", "Matrix", "Boundary Simulation",
                "O(M*N)", "O(1)",
                "vector<int> spiralOrder(vector<vector<int>>& matrix) {\n    int top = 0, bottom = matrix.size() - 1, left = 0, right = matrix[0].size() - 1;\n    vector<int> res;\n    while (top <= bottom && left <= right) {\n        for (int c = left; c <= right; ++c) res.push_back(matrix[top][c]);\n        top++;\n        for (int r = top; r <= bottom; ++r) res.push_back(matrix[r][right]);\n        right--;\n    }\n    return res;\n}",
                "matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
                json.dumps({"hint_1": "Peel matrix boundaries layer by layer clockwise.", "hint_2": "Shrink top, right, bottom, and left boundaries monotonically."}),
                json.dumps({"explanation": "Simulate 4 perimeter walls contracting inward.", "code": "// Spiral Matrix Optimal"}),
                json.dumps([{"step": 1, "line": 5, "state_description": "Top row traversal", "data_elements": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "active_indices": {"top": 0, "bottom": 2, "left": 0, "right": 2, "row": 0, "col": 0}, "variables": {"top": 0, "bottom": 2, "left": 0, "right": 2}, "action_explanation": "[Observation]: Inspecting top row elements from column left to right. [The Conflict / Bottleneck]: Traversing boundary wall. [The Action]: Include matrix values and contract top wall down by 1."}]),
                "Mastered"
            ),
            (
                "shrestha", "Trapping Rain Water", "Arrays", "Two Pointers",
                "O(N)", "O(1)",
                "def trap(height):\n    left, right = 0, len(height) - 1\n    left_max = right_max = water = 0\n    while left < right:\n        if height[left] < height[right]:\n            if height[left] >= left_max: left_max = height[left]\n            else: water += left_max - height[left]\n            left += 1\n        else:\n            if height[right] >= right_max: right_max = height[right]\n            else: water += right_max - height[right]\n            right -= 1\n    return water",
                "height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]",
                json.dumps({"hint_1": "Water trapped depends on shorter boundary wall.", "hint_2": "Advance pointer with smaller height inwards."}),
                json.dumps({"explanation": "Two pointers inward scan maintains max heights in single pass.", "code": "# Trapping Rain Water Optimal"}),
                json.dumps([{"step": 1, "line": 4, "state_description": "Outer boundary check", "data_elements": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], "active_indices": {"left": 0, "right": 11}, "variables": {"left": 0, "right": 11, "water": 0}, "action_explanation": "[Observation]: Left index 0 (height 0), Right index 11 (height 1). [The Conflict / Bottleneck]: Left wall is strictly shorter. [The Action]: Shift left pointer inward to check next cavity."}]),
                "Mastered"
            ),
            (
                "shrestha", "Three Sum", "Arrays", "Two Pointers",
                "O(N^2)", "O(1)",
                "vector<vector<int>> threeSum(vector<int>& nums) {\n    sort(nums.begin(), nums.end());\n    // 3Sum optimal two-pointer scan\n    return {};\n}",
                "nums = [-1, 0, 1, 2, -1, -4]",
                json.dumps({"hint_1": "Fix first element and run Two Sum II on the rest.", "hint_2": "Skip duplicate elements to guarantee unique triplets."}),
                json.dumps({"explanation": "Sort array first, then use outer loop with two-pointer inner scan.", "code": "// 3Sum Optimal"}),
                json.dumps([{"step": 1, "line": 3, "state_description": "Pivot selection", "data_elements": [-4, -1, -1, 0, 1, 2], "active_indices": {"i": 1, "left": 2, "right": 5}, "variables": {"i": 1, "left": 2, "right": 5}, "action_explanation": "[Observation]: Pivot i at index 1 (val -1), left at 2 (val -1), right at 5 (val 2). [The Conflict / Bottleneck]: Sum -1 + -1 + 2 equals 0. [The Action]: Triplet found; record answer and contract both pointers."}]),
                "Mastered"
            )
        ]
        cursor.executemany("""
            INSERT INTO problem_history (
                username, problem_name, topic, subtopic_pattern,
                time_complexity, space_complexity, code_snippet,
                problem_context, hints_json, final_solution_json,
                execution_trace_json, mastery_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_problems)
    
    conn.commit()
    conn.close()

def get_or_create_user(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    clean_user = username.strip().lower()
    cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (clean_user,))
    conn.commit()
    conn.close()
    return clean_user

def get_all_users() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [r["username"] for r in rows]

def save_problem_record(username: str, data: dict, code_snippet: str, problem_context: str):
    conn = get_connection()
    cursor = conn.cursor()
    clean_user = username.strip().lower()
    
    cursor.execute("""
        INSERT INTO problem_history (
            username, problem_name, topic, subtopic_pattern,
            time_complexity, space_complexity, code_snippet,
            problem_context, hints_json, final_solution_json,
            execution_trace_json, mastery_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        clean_user,
        data.get("problem_name", "DSA Problem"),
        data.get("topic", "Data Structures"),
        data.get("subtopic_pattern", "Simulation"),
        data.get("time_complexity", "O(N)"),
        data.get("space_complexity", "O(1)"),
        code_snippet,
        problem_context,
        json.dumps(data.get("hints", {})),
        json.dumps(data.get("final_solution", {})),
        json.dumps(data.get("execution_trace", [])),
        data.get("mindmap_node", {}).get("mastery_status", "Mastered")
    ))
    
    conn.commit()
    conn.close()

def get_user_history(username: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    clean_user = username.strip().lower()
    
    cursor.execute("""
        SELECT * FROM problem_history
        WHERE username = ?
        ORDER BY id ASC
    """, (clean_user,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "username": r["username"],
            "problem_name": r["problem_name"],
            "topic": r["topic"],
            "subtopic_pattern": r["subtopic_pattern"],
            "time_complexity": r["time_complexity"],
            "space_complexity": r["space_complexity"],
            "code_snippet": r["code_snippet"],
            "problem_context": r["problem_context"],
            "hints": json.loads(r["hints_json"]) if r["hints_json"] else {},
            "final_solution": json.loads(r["final_solution_json"]) if r["final_solution_json"] else {},
            "execution_trace": json.loads(r["execution_trace_json"]) if r["execution_trace_json"] else [],
            "mastery_status": r["mastery_status"],
            "created_at": r["created_at"]
        })
    return history