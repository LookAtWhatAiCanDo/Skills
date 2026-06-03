#!/usr/bin/env python3
import os
import shutil
import re

# List of system plugins to exclude
SYSTEM_PLUGINS = {
    "android-cli-plugin",
    "chrome-devtools-plugin",
    "firebase",
    "google-antigravity-sdk",
    "modern-web-guidance-plugin",
    "science"
}

def copy_tree_without_ds_store(src, dst):
    """Recursively copies files from src to dst, ignoring .DS_Store."""
    if not os.path.exists(src):
        return
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        if item == ".DS_Store":
            continue
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_tree_without_ds_store(s, d)
        else:
            shutil.copy2(s, d)

def parse_frontmatter(file_path):
    """Parses standard frontmatter from a SKILL.md file."""
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if not content.startswith("---"):
        return None
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
        
    yaml_text = parts[1]
    lines = yaml_text.strip().split("\n")
    
    data = {}
    current_key = None
    current_val = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # New key definition (e.g., name: or description:)
        if ":" in line and not line.startswith(" "):
            if current_key:
                data[current_key] = " ".join(current_val).strip()
            key, val = line.split(":", 1)
            current_key = key.strip()
            val = val.strip()
            if val in (">-", ">", "|", "|-"):
                current_val = []
            else:
                current_val = [val]
        elif current_key and line.startswith(" "):
            current_val.append(line.strip())
            
    if current_key:
        data[current_key] = " ".join(current_val).strip()
        
    # Clean quotes from description if present
    if "description" in data:
        desc = data["description"]
        if (desc.startswith('"') and desc.endswith('"')) or (desc.startswith("'") and desc.endswith("'")):
            data["description"] = desc[1:-1].strip()
            
    return data

def main():
    home = os.path.expanduser("~")
    src_skills_dir = os.path.join(home, ".gemini", "antigravity", "skills")
    src_plugins_dir = os.path.join(home, ".gemini", "config", "plugins")
    
    repo_root = "/Users/pv/Dev/GitHub/LookAtWhatAiCanDo/Skills"
    dest_skills_dir = os.path.join(repo_root, ".gemini", "antigravity", "skills")
    dest_plugins_dir = os.path.join(repo_root, ".gemini", "config", "plugins")
    
    print("Syncing custom standalone skills...")
    if os.path.exists(src_skills_dir):
        for skill_name in sorted(os.listdir(src_skills_dir)):
            if skill_name == ".DS_Store":
                continue
            src_path = os.path.join(src_skills_dir, skill_name)
            if os.path.isdir(src_path):
                print(f" - Copying {skill_name}")
                copy_tree_without_ds_store(src_path, os.path.join(dest_skills_dir, skill_name))
    
    print("Syncing custom plugins...")
    custom_plugins = []
    if os.path.exists(src_plugins_dir):
        for plugin_name in sorted(os.listdir(src_plugins_dir)):
            if plugin_name == ".DS_Store" or plugin_name in SYSTEM_PLUGINS:
                continue
            src_path = os.path.join(src_plugins_dir, plugin_name)
            if os.path.isdir(src_path):
                print(f" - Copying {plugin_name}")
                copy_tree_without_ds_store(src_path, os.path.join(dest_plugins_dir, plugin_name))
                custom_plugins.append(plugin_name)
                
    # Gather information about custom standalone skills
    standalone_skills = []
    if os.path.exists(dest_skills_dir):
        for skill_name in sorted(os.listdir(dest_skills_dir)):
            if skill_name == ".DS_Store":
                continue
            skill_path = os.path.join(dest_skills_dir, skill_name, "SKILL.md")
            metadata = parse_frontmatter(skill_path)
            if metadata:
                standalone_skills.append({
                    "name": metadata.get("name", skill_name),
                    "description": metadata.get("description", ""),
                    "path": f".gemini/antigravity/skills/{skill_name}/SKILL.md",
                    "dir": skill_name
                })
                
    # Gather information about custom plugin skills
    plugin_skills = []
    for plugin_name in custom_plugins:
        plugin_skills_path = os.path.join(dest_plugins_dir, plugin_name, "skills")
        if os.path.exists(plugin_skills_path):
            for skill_name in sorted(os.listdir(plugin_skills_path)):
                if skill_name == ".DS_Store":
                    continue
                skill_path = os.path.join(plugin_skills_path, skill_name, "SKILL.md")
                metadata = parse_frontmatter(skill_path)
                if metadata:
                    plugin_skills.append({
                        "plugin": plugin_name,
                        "name": metadata.get("name", skill_name),
                        "description": metadata.get("description", ""),
                        "path": f".gemini/config/plugins/{plugin_name}/skills/{skill_name}/SKILL.md",
                        "dir": skill_name
                    })

    # Generate the README section
    print("Generating README documentation update...")
    
    # 1. Directory Structure Representation
    dir_structure = [
        "```",
        ".gemini/",
        "├── config/",
        "│   └── plugins/"
    ]
    
    for idx, plugin in enumerate(custom_plugins):
        prefix = "└── " if idx == len(custom_plugins) - 1 else "├── "
        dir_structure.append(f"│       {prefix}{plugin}/           # Multi-component plugin")
        dir_structure.append(f"│           ├── plugin.json                   # Plugin metadata")
        dir_structure.append(f"│           └── skills/")
        dir_structure.append(f"│               └── {plugin}/")
        dir_structure.append(f"│                   ├── SKILL.md              # Trigger rules & logic")
        
        # Check for scripts
        scripts_path = os.path.join(dest_plugins_dir, plugin, "skills", plugin, "scripts")
        if os.path.exists(scripts_path):
            dir_structure.append(f"│                   └── scripts/")
            for script_file in sorted(os.listdir(scripts_path)):
                if script_file != ".DS_Store":
                    dir_structure.append(f"│                       └── {script_file}         # Python script")
                    
    dir_structure.append("└── antigravity/")
    dir_structure.append("    └── skills/")
    
    for idx, skill in enumerate(standalone_skills):
        prefix = "└── " if idx == len(standalone_skills) - 1 else "├── "
        comment = ""
        if skill["dir"] == "commit":
            comment = "           # Git Commit Automator"
        elif skill["dir"] == "newskill":
            comment = "                         # Skill Generator"
        elif skill["dir"] == "agentspec":
            comment = "                        # Agent Specification Generator"
        elif skill["dir"] == "skillpub":
            comment = "                         # Skill Publisher"
        elif skill["dir"] == "customskills":
            comment = "                     # Custom Skills Lister"
        elif skill["dir"] == "bootstrap-lawacd":
            comment = "                 # AI Wins/Fails Tracker Bootstrapper"
        elif skill["dir"] == "bootstrap":
            comment = "                        # Developer Skills Bootstrapper"
            
        dir_structure.append(f"        {prefix}{skill['dir']}/{comment}")
        dir_structure.append(f"        │   └── SKILL.md")
        
        # Check for scripts
        scripts_path = os.path.join(dest_skills_dir, skill["dir"], "scripts")
        if os.path.exists(scripts_path):
            dir_structure.append(f"        │   └── scripts/")
            for script_file in sorted(os.listdir(scripts_path)):
                if script_file != ".DS_Store":
                    dir_structure.append(f"        │       └── {script_file}")
                    
    # Clean up trailing vertical bars from the directory structure lists if needed
    for i in range(len(dir_structure)):
        # If line contains '|' and the next lines don't use it, we can fix it, but standard layout is fine.
        pass
        
    dir_structure.append("```")
    dir_structure_str = "\n".join(dir_structure)
    
    # 2. Detailed Itemized Custom Skills List
    itemized_list = []
    counter = 1
    
    # Helper to parse triggers/command usage out of the description or quick start inside SKILL.md
    def extract_quick_start_triggers(skill_full_path):
        if not os.path.exists(skill_full_path):
            return "N/A", "N/A"
        with open(skill_full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        triggers = []
        is_qs = False
        for line in lines:
            if "## Quick Start" in line or "## Usage" in line:
                is_qs = True
                continue
            if is_qs and line.startswith("## "):
                break
            if is_qs and (line.strip().startswith("-") or line.strip().startswith("*")):
                # Extract code quotes or standard texts
                clean_line = line.strip().lstrip("-* ").replace("`", "")
                if (clean_line.startswith('"') and clean_line.endswith('"')) or (clean_line.startswith("'") and clean_line.endswith("'")):
                    clean_line = clean_line[1:-1].strip()
                triggers.append(clean_line)
                
        # Parse usage section briefly
        usage_str = ""
        is_usage = False
        for line in lines:
            if "## Usage" in line:
                is_usage = True
                continue
            if is_usage and line.startswith("## "):
                break
            if is_usage:
                usage_str += line
                
        return triggers, usage_str.strip()

    # Process Standalone Skills
    for skill in standalone_skills:
        skill_full_path = os.path.join(dest_skills_dir, skill["dir"], "SKILL.md")
        triggers, usage = extract_quick_start_triggers(skill_full_path)
        
        # Determine Title
        title_map = {
            "commit": "Git Commit Automator (`/commit`)",
            "newskill": "Skill Generator (`/newskill`)",
            "agentspec": "Agent Specification Generator (`/agentspec`)",
            "skillpub": "Skill Publisher (`/skillpub`)",
            "customskills": "Custom Skills Lister (`/customskills`)",
            "bootstrap-lawacd": "AI Wins and Fails Tracker Bootstrapper (`/bootstrap-lawacd`)",
            "bootstrap": "Developer Skills Bootstrapper (`/bootstrap`)"
        }
        title = title_map.get(skill["dir"], f"{skill['name'].title()} Skill")
        
        triggers_formatted = ""
        if triggers:
            # First trigger acts as Command Trigger
            primary_trigger = triggers[0]
            other_triggers = ", ".join(f'`{t}`' for t in triggers[1:])
            triggers_formatted = f"\n* **Trigger Command**: `{primary_trigger}`\n"
            if other_triggers:
                triggers_formatted += f"* **Natural Language Triggers**: {other_triggers}\n"
                
        item = f"""### {counter}. {title}

{skill['description']}

* **Path**: `{skill['path']}`{triggers_formatted}
"""
        if usage:
            item += f"\n#### Usage\n{usage}\n"
            
        itemized_list.append(item.strip())
        counter += 1

    # Process Plugin Skills
    for skill in plugin_skills:
        skill_full_path = os.path.join(dest_plugins_dir, skill["plugin"], "skills", skill["dir"], "SKILL.md")
        triggers, usage = extract_quick_start_triggers(skill_full_path)
        
        title = "AI Wins and Fails Tracker" if skill["plugin"] == "look-at-what-ai-can-do" else f"{skill['name'].title()} Plugin"
        
        triggers_formatted = ""
        if triggers:
            triggers_formatted = f"\n* **Trigger Phrases**: " + ", ".join(f"`{t}`" for t in triggers) + "\n"
            
        item = f"""### {counter}. {title} ({skill['plugin']})

{skill['description']}

* **Path**: `{skill['path']}`{triggers_formatted}
"""
        if usage:
            item += f"\n#### Usage\n{usage}\n"
            
        itemized_list.append(item.strip())
        counter += 1

    itemized_list_str = "\n\n---\n\n".join(itemized_list)
    
    # Assemble the full custom skills block
    new_gemini_section = f"""## Gemini / Antigravity Custom Skills

This section houses custom plugins and standalone skills configured for the Google Antigravity/Gemini workspace environment.

### Directory Structure

Custom configuration is tracked under the `.gemini` folder, matching the exact directory layout expected in the user's home directory (`~/.gemini/`):

{dir_structure_str}

---

{itemized_list_str}

---"""

    readme_path = os.path.join(repo_root, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            
        # Match from "## Gemini / Antigravity Custom Skills" to "### Installation & Syncing"
        pattern = re.compile(
            r"## Gemini / Antigravity Custom Skills.*?### Installation & Syncing",
            re.DOTALL
        )
        
        if pattern.search(readme_content):
            # Replace target block
            updated_content = pattern.sub(new_gemini_section + "\n\n### Installation & Syncing", readme_content)
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Successfully updated README.md.")
        else:
            print("Warning: Could not locate Gemini custom skills section boundaries in README.md.")
    else:
        print("Error: README.md not found in repository.")
        
    print("\nSync and documentation compilation complete!")

if __name__ == "__main__":
    main()
