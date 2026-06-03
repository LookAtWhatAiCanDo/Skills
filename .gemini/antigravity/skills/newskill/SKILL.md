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
