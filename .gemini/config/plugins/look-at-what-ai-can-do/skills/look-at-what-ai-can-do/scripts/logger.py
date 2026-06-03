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
