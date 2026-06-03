---
name: agentspec
description: >-
  Use this skill immediately when the user types the slash command '/agentspec' or '/agents', OR when they ask in natural language to 'document agents', 'generate agent spec', 'create AGENTS.md', 'list agent architecture', or 'setup codebase agents'.
---

# Agent Specification Generator (`/agentspec`)

## Overview
This skill scans the active workspace codebase and documentation files (respecting ignore rules), analyzes where specialized AI agents could be utilized, and creates a comprehensive `AGENTS.md` file detailing the suggested agent architecture, tools, triggers, and prompts.

## Dependencies
- Standard filesystem tools.
- Git (for analyzing tracked files and honoring `.gitignore`).

## Quick Start
You can trigger this skill by typing:
- `/agentspec`
- `/agents`
- Saying "document the agents for this project" or "create an AGENTS.md"

## Workflow

### 1. Scan Repository Files
- Identify the repository files using git (honoring `.gitignore` and `.git/info/exclude`):
  ```bash
  git ls-files
  ```
- If git is not initialized, run a recursive directory search, filtering out standard build/dependency folders (e.g. `node_modules`, `build`, `dist`, `.gradle`, `venv`, `target`, `bin`).

### 2. Analyze Codebase and Identify Agent Roles
- Read code samples, configs, and documentation to understand the project structure, tech stack, and workflow.
- Identify areas where specialized agents can contribute. Examples of roles:
  - **`Architect Agent`**: Understands full-system design and coordinates subagents.
  - **`Code Reviewer / Linter Agent`**: Analyzes code styles, patterns, and errors.
  - **`Database / SQL Agent`**: Manages migrations, schemas, and queries.
  - **`UI / Layout Agent`**: Validates CSS, accessibility, and visual layouts.
  - **`Science / Research Agent`**: Interface for literature searching or specialized APIs.
- For each role, determine its:
  - **System prompt / Instructions**: Specific constraints and behavior.
  - **Tools**: Required MCP servers, command line tools, or file read/write scopes.
  - **Triggers**: How and when this agent is invoked (e.g., file changes, commands, delegation).

### 3. Generate `AGENTS.md`
Create a standard `AGENTS.md` in the root of the project with the following format:
```markdown
# Agent Architecture & Specifications

This document defines the specialized AI agent roles, tools, and protocols configured or designed for this codebase.

## Agent Team Overview

| Agent Role | Primary Responsibility | Triggers | Tool Access |
| :--- | :--- | :--- | :--- |
| [Role Name] | [Brief summary of duties] | [Commands/Triggers] | [MCP / Shell Tools] |

---

## Agent Details

### 1. [Role Name]
* **System Prompt / Instructions**:
  ```
  [Exact system prompt describing constraints and goals]
  ```
* **Tool Permissions**:
  - `mcp_server/*`
  - `read_file`, `write_file` (limited to specific paths)
* **Interaction / Collaboration Flow**:
  - Explains how this agent interacts with other subagents or the user.
```

### 4. Code Generation (Optional)
- If the project has an active agent system configuration (e.g., using the Google Antigravity SDK with Python or configuration jsons), generate the appropriate Python Agent definitions or system prompt config files as needed.

### 5. Report Progress
- Inform the user of the created/modified `AGENTS.md` and display a summary of the designed agent topology.

## Common Mistakes
- **Ignoring Project Context**: Suggesting a standard set of generic agents without analyzing what the codebase actually does.
- **Exposing Secrets**: Suggesting prompts or scripts that hardcode API keys or credentials.
- **Over-complicating**: Suggesting a 10-agent network for a simple script when 1 or 2 focused agents would do.
