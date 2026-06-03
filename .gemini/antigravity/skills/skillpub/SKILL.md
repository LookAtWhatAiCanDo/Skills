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
This skill automates the process of backing up your custom user-defined standalone skills and plugins from your local `~/.gemini/` configurations into your version-controlled repository, and updating the repository's `README.md` documentation automatically.

It does this by executing a single Python helper script, resolving all file copies, system exclusions, `.DS_Store` filtering, and documentation generation under a single execution.

## Quick Start
You can trigger this skill by typing:
- `/skillpub`
- `/skillsync`
- `/skillpush`
- Saying "publish my custom skills" or "sync my skills"

## Workflow

### 1. Execute the Publisher Script
Run the unified Python publisher script from your local standalone skills directory:
```bash
python3 ~/.gemini/antigravity/skills/skillpub/scripts/publish.py
```

### 2. Acknowledge and Summarize
- Confirm to the user that the synchronization script completed successfully.
- Present a summary of the copied standalone skills and custom plugins.
- Inform the user that `README.md` has been dynamically parsed and updated in the repository.
- Remind the user they can run `git status` or the `/commit` command inside the repository `/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills/` to review, stage, and commit the newly synced changes.

## Common Mistakes
- **Running manual copy commands**: Trying to copy directories manually using `cp` or `mkdir`. Always use the unified `publish.py` script to avoid multiple user prompts and ensure OS files (like `.DS_Store`) and system plugins are filtered correctly.
