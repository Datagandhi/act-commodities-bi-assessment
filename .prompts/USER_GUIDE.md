# Documentation Automation - User Guide

## First Time Setup

### Step 1: Generate Initial Documentation
```powershell
python .prompts/documentation_agent.py --template project_readme --output README.md --vars .prompts/example_variables_project_readme.yaml --validate
```

### Step 2: Create Baseline Cache
```powershell
python .prompts/documentation_updater_agent.py --reset-state
```

**⚠️ IMPORTANT:** After running `--reset-state`, the system snapshots the current state. Make code changes AFTER this step.

---

## Update Existing Documentation

### Step 1: Make Your Code Changes
Edit SQL queries, Power BI visuals, dimensional models, etc.

**Example:**
```powershell
# Add a new query to your SQL file
# Modify a Power BI visual
# Update dimensional model diagram
```

### Step 2: Detect Changes
```powershell
python .prompts/documentation_updater_agent.py --diff --target README.md
```

### Step 3: Generate Updates JSON
```powershell
# Read the generated prompt
cat .prompts/.cache/update_prompt.txt

# Use Copilot Chat to generate updates:
# @workspace Read .prompts/.cache/update_prompt.txt and generate updates.json with sections to update in README.md

# Save Copilot's JSON response to:
# .prompts/.cache/updates.json
```

### Step 4: Apply Updates
```powershell
python .prompts/documentation_updater_agent.py --apply --target README.md
```

---

## Available Templates

| Template | Output File |
|----------|-------------|
| `project_readme` | README.md |
| `dimensional_model` | model.md |
| `powerbi_report` | performance_overview_documentation.md |

---

## Example: Update README After Adding New SQL Query

```powershell
# 1. Edit completed_sql_queries.sql (add Query 8)

# 2. Detect changes
python .prompts/documentation_updater_agent.py --diff --target README.md

# 3. Review what changed
cat .prompts/.cache/update_prompt.txt

# 4. Generate updates.json via Copilot Chat:
#    @workspace Read .prompts/.cache/update_prompt.txt and create updates.json

# 5. Apply updates
python .prompts/documentation_updater_agent.py --apply --target README.md
```

---

## Quick Reference

**Generate fresh docs:**
```powershell
python .prompts/documentation_agent.py --template project_readme --output README.md --vars .prompts/example_variables_project_readme.yaml
```

**Reset tracking (treat all files as new):**
```powershell
python .prompts/documentation_updater_agent.py --reset-state
```

**Check what changed:**
```powershell
python .prompts/documentation_updater_agent.py --diff --target README.md
```

**Apply updates:**
```powershell
python .prompts/documentation_updater_agent.py --apply --target README.md
```
