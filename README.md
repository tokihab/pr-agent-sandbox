# Agent Build Log: Code Review Assistant

## Phase 1: Configuration & Connection
*   **Goal:** Connect Claude Desktop to the GitHub API using the official MCP server to act as a live tool connection.
*   **Obstacle 1 (Pathing Error):** Initial configuration used `"command": "npx"` in the `claude_desktop_config.json`. This failed to launch on Windows, returning a `FileNotFoundError` because the system needed the Windows-specific executable. 
    *   *Fix:* Changed the command to `"command": "npx.cmd"`.
*   **Obstacle 2 (UI Quirk):** Even after fixing the executable path, the tool icon (plug/hammer) did not visually appear in the Claude UI chat bar. 
    *   *Fix:* Navigated to Claude's Developer Settings -> Local MCP servers to verify the connection. Confirmed the `github` server was showing a blue "running" badge, proving the UI was just visually hiding the icon but the backend connection was live.
*   **Obstacle 3 (Security Incident):** Accidentally pasted the live GitHub Personal Access Token (PAT) into a chat prompt while debugging the JSON file. 
    *   *Fix:* Immediately went to GitHub Developer settings, revoked the compromised token, generated a new restricted token, and updated the config. 

## Phase 2: Spec Deviations from FL-06
*   **Tool Names:** My original design spec proposed custom, plain-English tool names (`Read_Changes`, `Write_Comment`, `Combine_Code`). However, because I chose the official `@modelcontextprotocol/server-github` server to quickly achieve a live connection, I had to adapt to its hardcoded tool schema.
*   *Action:* I updated my system instructions to rely on the official tools (`get_pull_request_files`, `create_issue_comment`, `create_pull_request`, `merge_pull_request`).

## Phase 3: Sandbox Environment & Iteration 1
*   **Goal:** Create an isolated testing environment so experimental agent actions don't break main projects, and test the core loop.
*   **Action:** Created the `pr-reviewer-sandbox` repository with a baseline `calculator.py`.
*   **Run 1 (`feature/multiply-bug`):** 
    *   Introduced an unused `import os` and a flawed logic block (`def multiply(a, b): return a + b`).
    *   *Execution note:* Claude initially attempted to fetch the raw `.diff` URL directly via web search, which failed. It successfully recovered on its own by falling back to the official MCP tool `get_pull_request_files`.
    *   *Result:* Successfully flagged both bugs. Guardrail worked perfectly—it halted and refused to merge until I typed exactly "Looks Good To Me."

## Phase 4: Final End-to-End Run (Video Capture)
*   **Goal:** Record a raw, unedited screen capture of the agent completing its core job on a fresh PR.
*   **Run 2 (`feature/divide-by-zero`):** 
    *   Introduced a critical `return a / 0` error and an unused `temp_val` variable.
    *   *Execution note:* Triggered the agent using the established core prompt. 
    *   *Result:* The agent fetched the diff, analyzed the code, accurately documented the zero-division error and unused variable in a formatted GitHub comment, and waited. Upon receiving the "Looks Good To Me." command, it successfully executed `merge_pull_request`. The video captures this full loop.
