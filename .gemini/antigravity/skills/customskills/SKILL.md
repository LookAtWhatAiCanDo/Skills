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
