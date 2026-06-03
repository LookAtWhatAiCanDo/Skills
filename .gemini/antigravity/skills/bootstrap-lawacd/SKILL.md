---
name: bootstrap-lawacd
description: >-
  Use this skill immediately when the user types the slash command '/bootstrap-lawacd' or '/install-lawacd', OR when they ask to 'install look-at-what-ai-can-do', 'bootstrap lawacd', or 'setup the AI tracker plugin'.
---

# AI Wins and Fails Tracker Bootstrapper (`/bootstrap-lawacd`)

## Overview
This skill automates the complete recreation and setup of the custom `look-at-what-ai-can-do` plugin (metadata, sub-skills, and Python logging script) inside the local configuration path: `~/.gemini/config/plugins/look-at-what-ai-can-do/`.

## Quick Start
You can trigger this skill by typing:
- `/bootstrap-lawacd`
- `/install-lawacd`
- Saying "initialize the look-at-what-ai-can-do plugin"

## Workflow

### 1. Ensure Target Directory Structure
Create the necessary plugin directories under `~/.gemini/config/plugins/`:
```bash
mkdir -p ~/.gemini/config/plugins/look-at-what-ai-can-do/skills/look-at-what-ai-can-do/scripts
```

### 2. Write plugin.json
Create `~/.gemini/config/plugins/look-at-what-ai-can-do/plugin.json` containing:
```json
{
  "name": "look-at-what-ai-can-do",
  "version": "1.0.0",
  "description": "Custom logging plugins for AI Wins and Fails",
  "author": {
    "name": "User"
  }
}
```

### 3. Write SKILL.md
Create `~/.gemini/config/plugins/look-at-what-ai-can-do/skills/look-at-what-ai-can-do/SKILL.md` containing:
```markdown
---
name: look-at-what-ai-can-do
description: Use this skill immediately when the user explicitly says "lawacd", "la whacked", "epic win", "epic fail", "way to go Einstein", or asks to remember something as an example of AI in a positive or negative context. Do NOT trigger on standard mentions of the full company name "Look At What AI Can Do" unless explicitly paired with these reactions or logging instructions.
---

# Goal
Capture real-world examples of AI successes (wins) and failures (fails) from the current session context and save them as markdown entries in the locally cloned Ideation repository for future content planning.

# Instructions
1. **Identify the Target Context**: Isolate the message or code block immediately preceding the user's trigger phrase that represents the specific win or fail.
2. **Classify the Event**: 
   - Label as `WIN` if the user is blown away or gives praise.
   - Label as `FAIL` if the user uses sarcasm ("Einstein", "killing me smalls", "sad trombone", "fail").
3. **Extract Parameters**:
   - `Topic`: A concise 3-5 word title of the subject (e.g., "Kotlin Multiplatform State Bug").
   - `Context`: The exact text, prompt, or code block being referenced.
   - `User Comment`: The specific phrase or feedback the user just typed.
4. **Execute**: Run the backend script `scripts/logger.py` passing these pieces of information as arguments.
5. **Acknowledge**: Give a brief, witty confirmation that the event has been safely captured in the Ideation repo.
```

### 4. Write logger.py
Create `~/.gemini/config/plugins/look-at-what-ai-can-do/skills/look-at-what-ai-can-do/scripts/logger.py` containing:
```python
#!/usr/bin/env python3
import sys
import os
from datetime import datetime

def log_event():
    # Ensure all required arguments are captured
    if len(sys.argv) < 5:
        print("Error: Missing logging parameters.")
        sys.exit(1)
        
    status_type = sys.argv[1]   # WIN or FAIL
    topic = sys.argv[2]         # e.g., "Compose Multiplatform UI"
    context = sys.argv[3]       # The raw snippet or text block
    comment = sys.argv[4]       # Your reaction/comment

    # Target the requested local repository directory
    repo_dir = "/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Ideation"
    log_path = os.path.join(repo_dir, "ai_wins_and_fails.md")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Safely isolate the backticks so they don't break the string rendering
    ticks = "```"

    # Construct the markdown entry cleanly
    markdown_entry = f"""
## [{status_type}] - {topic}
*Captured on: {timestamp}*

> **Reaction:** "{comment}"

### Context / Code Reference:
{ticks}
{context.strip()}
{ticks}

---
"""

    try:
        # Create directory path if it doesn't exist
        os.makedirs(repo_dir, exist_ok=True)
        
        # Append the new entry to the repository file
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(markdown_entry)
        print("Logged successfully to Ideation repo.")
    except Exception as e:
        print(f"Error writing to Ideation repo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    log_event()
```
Make the script executable: `chmod +x logger.py`

### 5. Verify & Acknowledge
- Confirm the folders and files have been successfully created.
- Instruct the user that they can now test the plugin by typing trigger words like `lawacd` or `epic fail` after an AI interaction.
