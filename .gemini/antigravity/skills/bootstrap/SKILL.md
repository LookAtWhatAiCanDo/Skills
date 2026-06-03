---
name: bootstrap
description: >-
  Use this skill immediately when the user types the slash command '/bootstrap' or '/bootstrap install', OR when they ask in natural language to 'install custom skills suite', 'bootstrap my developer skills', or 'initialize custom skills'.
---

# Developer Skills Bootstrapper (`/bootstrap`)

## Strict Git Constraints (MANDATORY)
- **Do not proactively run any mutating Git commands** (such as `git add`, `git commit`, `git reset`, `git checkout`, or `git push`) unless the user has explicitly and directly instructed you to run that specific command in their prompt.
- Always explain what changes you intend to stage or commit and let the user review and confirm before you execute any mutating command.

## Overview
This skill is a self-contained installer that recreates the entire suite of custom developer skills (including `commit`, `newskill`, `agentspec`, `skillpub`, `customskills`, and `bootstrap` itself) inside the user's local standalone skills directory: `~/.gemini/antigravity/skills/`.

## Quick Start
Trigger this skill by typing:
- `/bootstrap`
- `/bootstrap install`
- Saying "initialize my custom developer skills"

## Workflow

### 1. Ensure Target Directory
- Verify that the target user skills directory `~/.gemini/antigravity/skills/` exists.
- If it does not exist, create it:
  ```bash
  mkdir -p ~/.gemini/antigravity/skills
  ```

### 2. Write Skill Files
Create the subdirectory for each skill and write its respective `SKILL.md` file using the exact contents specified below.

---

#### A. Git Commit Automator (`commit`)
- **Directory**: `~/.gemini/antigravity/skills/commit`
- **File Content** (`~/.gemini/antigravity/skills/commit/SKILL.md`):
```markdown
---
name: commit
description: Use this skill immediately when the user types the slash command '/commit' or '/commit [all|staged]' (defaulting to staged if not specified) in the chat, or explicitly asks the AI to commit their changes.
---

# Git Commit Automator

## Strict Git Constraints (MANDATORY)
- **Do not proactively run any mutating Git commands** (such as `git add`, `git commit`, `git reset`, `git checkout`, or `git push`) unless the user has explicitly and directly instructed you to run that specific command in their prompt.
- Always explain what changes you intend to stage or commit and let the user review and confirm before you execute any mutating command.

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
```

---

#### B. Skill Generator (`newskill`)
- **Directory**: `~/.gemini/antigravity/skills/newskill`
- **File Content** (`~/.gemini/antigravity/skills/newskill/SKILL.md`):
```markdown
---
name: newskill
description: >-
  Use this skill immediately when the user types the slash command '/newskill' or '/skillgen' (e.g., '/newskill my-skill plugin'), OR when they ask in natural language to 'create a new skill', 'generate a skill template', or 'create a new plugin'.
---

# Skill Generator (`/newskill`)

## Strict Git Constraints (MANDATORY)
- **Do not proactively run any mutating Git commands** (such as `git add`, `git commit`, `git reset`, `git checkout`, or `git push`) unless the user has explicitly and directly instructed you to run that specific command in their prompt.
- Always explain what changes you intend to stage or commit and let the user review and confirm before you execute any mutating command.

## Overview
This skill guides the agent to create a new custom standalone skill or plugin structure in the appropriate configuration directories of the workspace.

## Quick Start
You can trigger this skill by running:
- `/newskill <name> [standalone|plugin]` (e.g., `/newskill deploy plugin` or `/newskill format-code`)
- Saying "create a new skill named <name>"

## Workflow

### 1. Parse Arguments and Determine Target Paths
- Parse the command arguments:
  - `<name>`: The name of the skill (lowercase, separated by hyphens). If not provided, ask the user for it.
  - `[standalone|plugin]`: The type of skill. Default to `standalone` if not specified.
- Determine the target directories based on the type:
  - **Standalone**: target path is `~/.gemini/antigravity/skills/<name>/`
  - **Plugin**: target path is `~/.gemini/config/plugins/<name>/`

### 2. Interview and Refine Requirements
Before writing any code or markdown, have a quick 1-round interactive exchange with the user to clarify:
- The exact goal and trigger conditions of the skill.
- Whether it requires code/scripts (if yes, we will prepare a Python CLI script template under `scripts/`; if no, it will be an instruction-only markdown skill).
- Any specific inputs/outputs it should handle.

### 3. Create Directory and Files
Once details are aligned, create the structure:
- **For Standalone Skills**:
  1. Create directory `~/.gemini/antigravity/skills/<name>/`.
  2. Write `SKILL.md` with:
     - YAML frontmatter (matching the requested name and description/triggers).
     - Standard markdown sections (Overview, Dependencies, Quick Start, Workflow, Common Mistakes).
  3. If a helper script is needed, create a `scripts/` directory and write a baseline Python script template using `argparse`.

- **For Plugins**:
  1. Create directory `~/.gemini/config/plugins/<name>/`.
  2. Write `plugin.json` containing the name, version `1.0.0`, description, and author metadata.
  3. Create `skills/` and `skills/<name>/` directories.
  4. Write `SKILL.md` in `skills/<name>/SKILL.md` following standard format.
  5. If scripts are needed, write them under `skills/<name>/scripts/`.

### 4. Acknowledge Creation
- Report to the user the exact paths of the files created.
- Provide a short instruction on how they can test or trigger their new skill.

## Common Mistakes
- **Incorrect Directory Layout**: Creating the `plugin.json` inside the `skills/` folder instead of the plugin root.
- **Incorrect Yaml Metadata**: Not wrapping descriptions in double quotes or formatting yaml incorrectly.
- **Lack of Verification**: Not detailing standard failure scenarios and trigger scopes.
```

---

#### C. Agent Specification Generator (`agentspec`)
- **Directory**: `~/.gemini/antigravity/skills/agentspec`
- **File Content** (`~/.gemini/antigravity/skills/agentspec/SKILL.md`):
```markdown
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
```

---

#### D. Skill Publisher (`skillpub`)
- **Directory**: `~/.gemini/antigravity/skills/skillpub`
- **File Content** (`~/.gemini/antigravity/skills/skillpub/SKILL.md`):
```markdown
---
name: skillpub
description: >-
  Use this skill immediately when the user types the slash command '/skillpub', '/skillsync', or '/skillpush', OR when they ask in natural language to 'publish custom skills', 'copy skills to repository', 'sync skills to github', or 'back up my skills'.
---

# Skill Publisher (`/skillpub`)

## Strict Git Constraints (MANDATORY)
- **Do not proactively run any mutating Git commands** (such as `git add`, `git commit`, `git reset`, `git checkout`, or `git push`) unless the user has explicitly and directly instructed you to run that specific command in their prompt.
- Always explain what changes you intend to stage or commit and let the user review and confirm before you execute any mutating command.

## Overview
This skill copies all custom (user-defined) standalone skills and plugins from your local `~/.gemini/` configuration path back to the target version-controlled skills repository at `/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/.gemini/`, and automatically updates the repository's `README.md` documentation.

## Dependencies
- Standard filesystem tools (`cp`, `mkdir`).
- Target repository directory: `/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/` (already initialized as a Git repo).

## Quick Start
You can trigger this skill by typing:
- `/skillpub`
- `/skillsync`
- `/skillpush`
- Saying "publish my custom skills" or "sync my skills"

## Workflow

### 1. Ensure Target Directory
Verify the target directory `/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/.gemini/` exists. If not, create its components:
```bash
mkdir -p /Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/.gemini/antigravity/skills
mkdir -p /Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/.gemini/config/plugins
```

### 2. Identify and Publish Standalone Skills
- Standalone skills are placed directly under `~/.gemini/antigravity/skills/`.
- Since this directory only holds user-defined skills, copy *all* folders within it recursively to the target path:
  ```bash
  # Example copy command:
  cp -R ~/.gemini/antigravity/skills/* /Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/.gemini/antigravity/skills/
  ```
  *(Filter out `.DS_Store` or other OS cache files if present)*

### 3. Identify and Publish Custom Plugins
- Plugins are placed under `~/.gemini/config/plugins/`.
- Standard system plugins are:
  - `android-cli-plugin`
  - `chrome-devtools-plugin`
  - `firebase`
  - `google-antigravity-sdk`
  - `modern-web-guidance-plugin`
  - `science`
- List all directories under `~/.gemini/config/plugins/` and filter out the system plugins.
- For each remaining directory (which represent custom plugins like `look-at-what-ai-can-do`), copy it recursively to the target path:
  ```bash
  cp -R ~/.gemini/config/plugins/<custom-plugin-name> /Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/.gemini/config/plugins/
  ```

### 4. Automatically Update README.md
- Read the repository `README.md` at `/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/README.md`.
- Locate the `## Gemini / Antigravity Custom Skills` section.
- Scan and parse all custom standalone skills and custom plugins found in the local setup.
- Regenerate the directory structure block and the detailed itemized list of custom skills (including their trigger commands, paths, and descriptions).
- Re-write the `README.md` with the updated Gemini section, ensuring that other non-Gemini sections (e.g. for Claude, Codex, or other systems) are left completely untouched.

### 5. Acknowledge and Summary
- Present a formatted list of all successfully published standalone skills and custom plugins.
- Report that `README.md` was dynamically updated and list the skills documented.
- Remind the user that they can run `git status` inside `/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/` to review, stage, and commit the changes.

## Common Mistakes
- **Copying System Plugins**: Accidentally copying `firebase` or `science` plugins to the custom repository. Ensure the filter list is strictly applied.
- **Breaking Relative Paths**: Copying files into the wrong target directory levels. Maintain the mirrored `~/.gemini` directory structure.
- **Overwriting Non-Gemini Sections**: Wiping out the general introduction or other platform documentation in `README.md` during update. Always target only the Gemini section.
```

---

#### E. Custom Skills Lister (`customskills`)
- **Directory**: `~/.gemini/antigravity/skills/customskills`
- **File Content** (`~/.gemini/antigravity/skills/customskills/SKILL.md`):
```markdown
---
name: customskills
description: >-
  Use this skill immediately when the user types the slash command '/customskills' or '/skillslist', OR when they ask in natural language to 'list custom skills', 'show custom skills', 'what custom skills do I have?', or 'list my skills'.
---

# Custom Skills Lister (`/customskills`)

## Overview
This skill scans the active directories to identify, parse, and list all user-defined custom standalone skills and custom plugins, separating them from the standard system plugins and skills.

## Quick Start
You can trigger this skill by typing:
- `/customskills`
- `/skillslist`
- Saying "list custom skills" or "show my custom skills"

## Workflow

### 1. Scan Standalone Skills
- List all subdirectories inside the standalone user skills path: `~/.gemini/antigravity/skills/`.
- For each directory found (excluding system files like `.DS_Store`):
  - Read `SKILL.md`.
  - Extract the `name` and `description` from the YAML frontmatter.
  - Classify these as **Standalone Skills**.

### 2. Scan Custom Plugins
- List all subdirectories inside the plugins path: `~/.gemini/config/plugins/`.
- Filter out standard system plugins:
  - `android-cli-plugin`
  - `chrome-devtools-plugin`
  - `firebase`
  - `google-antigravity-sdk`
  - `modern-web-guidance-plugin`
  - `science`
- For each remaining custom plugin subdirectory:
  - If a `skills/` directory exists inside it, list all subdirectories inside that `skills/` folder.
  - Read each `SKILL.md` file found under `skills/<skill_name>/SKILL.md`.
  - Extract its `name` and `description` from the YAML frontmatter.
  - Classify these as **Plugin Skills** under the parent plugin's name.

### 3. Display the List
- Print a formatted list of all detected custom skills to the chat.
- Group them by category:
  - **Standalone Custom Skills**: List trigger command, file path, and description.
  - **Custom Plugins and Skills**: List the plugin name and its nested skills (with their trigger command, file path, and description).

## Common Mistakes
- **Listing System Skills**: Showing standard system skills (like `firebase-firestore` or `a11y-debugging`) in the custom list. Always verify the exclusion list.
- **Malformed YAML**: If a custom skill has invalid frontmatter, the parser might fail. Implement fallback parsing (regex or basic string splitting) to extract name and description if YAML parsing fails.
```

---

#### F. Developer Skills Bootstrapper (`bootstrap`)
- **Directory**: `~/.gemini/antigravity/skills/bootstrap`
- **File Content** (`~/.gemini/antigravity/skills/bootstrap/SKILL.md`):
  *(This file is written with the exact content of this bootstrap skill, enabling full recursion/bootstrap capability)*

### 3. Complete and Acknowledge
- Once all files are written, verify that the 6 directories exist.
- Inform the user that the entire custom developer skills suite is now fully bootstrapped and ready to be used.

## Common Mistakes
- **Recursion loop issues**: Writing the bootstrap file with syntax errors. Make sure it writes a clean copy of itself.
- **Incorrect target paths**: Using relative paths that don't map correctly to `~/.gemini/`.
