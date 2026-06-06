# AI Developer Skills

This repository contains custom configuration, plugins, scripts, and developer skills for various AI assistants (e.g., Gemini/Antigravity, Claude, Codex, etc.).

---

## Gemini / Antigravity Custom Skills

This section houses custom plugins and standalone skills configured for the Google Antigravity/Gemini workspace environment.

### Directory Structure

Custom configuration is tracked under the `.gemini` folder, matching the exact directory layout expected in the user's home directory (`~/.gemini/`):

```
.gemini/
├── config/
│   └── plugins/
│       └── look-at-what-ai-can-do/           # Multi-component plugin
│           ├── plugin.json                   # Plugin metadata
│           └── skills/
│               └── look-at-what-ai-can-do/
│                   ├── SKILL.md              # Trigger rules & logic
│                   └── scripts/
│                       └── logger.py         # Python script
└── antigravity/
    └── skills/
        ├── agentspec/                        # Agent Specification Generator
        │   └── SKILL.md
        ├── bootstrap/                        # Developer Skills Bootstrapper
        │   └── SKILL.md
        ├── bootstrap-lawacd/                 # AI Wins/Fails Tracker Bootstrapper
        │   └── SKILL.md
        ├── commit/           # Git Commit Automator
        │   └── SKILL.md
        ├── customskills/                     # Custom Skills Lister
        │   └── SKILL.md
        ├── newskill/                         # Skill Generator
        │   └── SKILL.md
        └── skillpub/                         # Skill Publisher
        │   └── SKILL.md
        │   └── scripts/
        │       └── publish.py
```

---

### 1. Agent Specification Generator (`/agentspec`)

Use this skill immediately when the user types the slash command '/agentspec' or '/agents', OR when they ask in natural language to 'document agents', 'generate agent spec', 'create AGENTS.md', 'list agent architecture', or 'setup codebase agents'.

* **Path**: `.gemini/antigravity/skills/agentspec/SKILL.md`
* **Trigger Command**: `/agentspec`
* **Natural Language Triggers**: `/agents`, `Saying "document the agents for this project" or "create an AGENTS.md"`

---

### 2. Developer Skills Bootstrapper (`/bootstrap`)

Use this skill immediately when the user types the slash command '/bootstrap' or '/bootstrap install', OR when they ask in natural language to 'install custom skills suite', 'bootstrap my developer skills', or 'initialize custom skills'.

* **Path**: `.gemini/antigravity/skills/bootstrap/SKILL.md`
* **Trigger Command**: `/bootstrap`
* **Natural Language Triggers**: `/bootstrap install`, `Saying "initialize my custom developer skills"`

---

### 3. AI Wins and Fails Tracker Bootstrapper (`/bootstrap-lawacd`)

Use this skill immediately when the user types the slash command '/bootstrap-lawacd' or '/install-lawacd', OR when they ask to 'install look-at-what-ai-can-do', 'bootstrap lawacd', or 'setup the AI tracker plugin'.

* **Path**: `.gemini/antigravity/skills/bootstrap-lawacd/SKILL.md`
* **Trigger Command**: `/bootstrap-lawacd`
* **Natural Language Triggers**: `/install-lawacd`, `Saying "initialize the look-at-what-ai-can-do plugin"`

---

### 4. Git Commit Automator (`/commit`)

MANDATORY. You MUST unconditionally load and read this skill file (via view_file) immediately when the user runs '/commit' or '/commit [all|staged]' (defaulting to staged if not specified), or explicitly asks the AI to commit. You must generate both a commit message and a detailed description.

* **Path**: `.gemini/antigravity/skills/commit/SKILL.md`
* **Trigger Command**: `/commit (defaults to committing staged changes)`
* **Natural Language Triggers**: `/commit staged (commits currently staged changes)`, `/commit all (stages all unstaged changes, then commits them)`

---

### 5. Custom Skills Lister (`/customskills`)

Use this skill immediately when the user types the slash command '/customskills' or '/skillslist', OR when they ask in natural language to 'list custom skills', 'show custom skills', 'what custom skills do I have?', or 'list my skills'.

* **Path**: `.gemini/antigravity/skills/customskills/SKILL.md`
* **Trigger Command**: `/customskills`
* **Natural Language Triggers**: `/skillslist`, `Saying "list custom skills" or "show my custom skills"`

---

### 6. Skill Generator (`/newskill`)

Use this skill immediately when the user types the slash command '/newskill' or '/skillgen' (e.g., '/newskill my-skill plugin'), OR when they ask in natural language to 'create a new skill', 'generate a skill template', or 'create a new plugin'.

* **Path**: `.gemini/antigravity/skills/newskill/SKILL.md`
* **Trigger Command**: `/newskill <name> [standalone|plugin] (e.g., /newskill deploy plugin or /newskill format-code)`
* **Natural Language Triggers**: `Saying "create a new skill named <name>"`

---

### 7. Skill Publisher (`/skillpub`)

Use this skill immediately when the user types the slash command '/skillpub', '/skillsync', or '/skillpush', OR when they ask in natural language to 'publish custom skills', 'copy skills to repository', 'sync skills to github', or 'back up my skills'.

* **Path**: `.gemini/antigravity/skills/skillpub/SKILL.md`
* **Trigger Command**: `/skillpub`
* **Natural Language Triggers**: `/skillsync`, `/skillpush`, `Saying "publish my custom skills" or "sync my skills"`

---

### 8. AI Wins and Fails Tracker (look-at-what-ai-can-do)

Use this skill immediately when the user explicitly says "lawacd", "la whacked", "epic win", "epic fail", "way to go Einstein", or asks to remember something as an example of AI in a positive or negative context. Do NOT trigger on standard mentions of the full company name "Look At What AI Can Do" unless explicitly paired with these reactions or logging instructions.

* **Path**: `.gemini/config/plugins/look-at-what-ai-can-do/skills/look-at-what-ai-can-do/SKILL.md`

---

### Installation & Syncing

To load these skills into your Antigravity environment, ensure they are copied or symlinked to your user data directory:

```bash
# Sync files to the local active Gemini configuration path
cp -R .gemini/config/plugins/* ~/.gemini/config/plugins/
cp -R .gemini/antigravity/skills/* ~/.gemini/antigravity/skills/
```
