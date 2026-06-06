---
name: commit
description: MANDATORY. You MUST unconditionally load and read this skill file (via view_file) immediately when the user runs '/commit' or '/commit [all|staged]' (defaulting to staged if not specified), or explicitly asks the AI to commit. You must generate both a commit message and a detailed description.
---

# Git Commit Automator

> [!IMPORTANT]
> **CRITICAL SYSTEM DIRECTIVE (MANDATORY)**:
> 1. You **MUST** load and read this `SKILL.md` file (using the `view_file` tool) every single time a git commit is requested or the `/commit` command is invoked.
> 2. You **MUST** run `git diff --cached` to analyze the exact staged changes before generating any commit message.
> 3. You **MUST** generate **BOTH** a subject line (commit message) **AND** a detailed description (body) outlining the specific changes. Commits with only a subject line are forbidden.
> 4. You **MUST** execute the commit command as:
>    `git commit -m "<subject_line>" -m "<detailed_description>"`

## Overview
This skill automates git staging, smart commit message generation based on actual code differences, and committing code changes directly to the active git repository.

## Dependencies
- Standard git client installed on the system path.
- Standard shell tools (accessible via `run_command` tool).

## Quick Start
You can trigger this skill by typing:
- `/commit` (defaults to committing staged changes)
- `/commit staged` (commits currently staged changes)
- `/commit all` (stages all unstaged changes, then commits them)

## Workflow

### 1. Parse Arguments and Stage Files
- Read the arguments passed with the `/commit` command.
- If the argument is `all` (e.g. `/commit all`), run:
  ```bash
  git add -A
  ```
- If the argument is `staged` or not provided (e.g. `/commit` or `/commit staged`), do not run `git add`. Proceed to verify the staged files.

### 2. Verify Staged Changes
- Run the following command to check what files are staged:
  ```bash
  git status --porcelain
  ```
- If no files are staged, inform the user clearly:
  - "No staged changes found to commit."
  - If they ran `/commit staged` or `/commit`, suggest that they can run `/commit all` to stage and commit all modified files.
  - Abort the execution.

### 3. Analyze Staged Code Changes
- Run the following command to inspect the exact diff of the staged changes:
  ```bash
  git diff --cached
  ```
- Read and analyze the diff to understand what files were modified, added, or deleted, and what the changes accomplish.

### 4. Generate Commit Message and Description
- Based on the diff analysis, generate:
  1. A clear, concise **commit subject line** (50 characters or less, written in the imperative mood, e.g., "Add user authentication flow").
  2. A detailed **commit description** explaining the "what" and "why" of the changes, formatted with bullet points for readability.

### 5. Commit Code Changes
- Construct and run the `git commit` command using the generated subject and description:
  ```bash
  git commit -m "<subject_line>" -m "<detailed_description>"
  ```
  *(Make sure to properly escape special characters and quotes for the shell command)*

### 6. Acknowledge and Report
- Once the commit command succeeds, display a success confirmation to the user.
- Show the exact commit message and description that was used, along with the branch name and commit hash if retrieved.

## Common Mistakes
- **No changes staged**: Running `/commit staged` when `git status` shows no staged changes. Always verify status before generating the message.
- **Vague commit messages**: Generating generic messages like "Update files". Always review the actual diff from `git diff --cached` to write specific, helpful descriptions.
- **Large binary files**: Trying to run diffs on large binary files. Focus the diff analysis on text source code files.
