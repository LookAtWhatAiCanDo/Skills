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
