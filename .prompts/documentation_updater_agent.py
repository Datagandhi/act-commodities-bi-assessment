"""
Documentation Updater Agent - Incremental README Updates

This agent detects changes in your repository and updates documentation
incrementally rather than regenerating from scratch.

Usage:
    python documentation_updater_agent.py --watch --auto-update
    python documentation_updater_agent.py --diff --target README.md
    python documentation_updater_agent.py --update-section "SQL Development" --reason "Added Query 8"

Author: ACT Commodities BI Assessment
Version: 1.0
Date: November 2025
"""

import argparse
import os
import yaml
import json
import difflib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import hashlib


class DocumentationUpdater:
    """
    Agent for incrementally updating documentation based on repository changes.
    
    Supports:
    - Change detection (file additions, removals, modifications)
    - Differential updates (only update affected sections)
    - Change tracking (what changed, when, why)
    - Rollback capability
    """
    
    def __init__(self, repo_root: str = "."):
        """
        Initialize the Documentation Updater.
        
        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = Path(repo_root)
        self.cache_dir = self.repo_root / ".prompts" / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.cache_dir / "doc_state.json"
        
    def detect_changes(self) -> Dict[str, List[str]]:
        """
        Detect changes in repository since last documentation update.
        
        Returns:
            Dictionary with 'added', 'modified', 'removed' file lists
        """
        current_state = self._get_repo_state()
        previous_state = self._load_state()
        
        changes = {
            "added": [],
            "modified": [],
            "removed": []
        }
        
        # Find added and modified files
        for filepath, filehash in current_state.items():
            if filepath not in previous_state:
                changes["added"].append(filepath)
            elif previous_state[filepath] != filehash:
                changes["modified"].append(filepath)
        
        # Find removed files
        for filepath in previous_state:
            if filepath not in current_state:
                changes["removed"].append(filepath)
        
        return changes
    
    def _get_repo_state(self) -> Dict[str, str]:
        """
        Get current state of repository (file paths and hashes).
        
        Returns:
            Dictionary mapping file paths to MD5 hashes
        """
        state = {}
        
        # Patterns to track
        patterns = [
            "*.sql",
            "*.md",
            "*.pbix",
            "*.pbip",
            "*.yaml",
            "*.json",
            "*.py"
        ]
        
        # Exclude patterns
        exclude_patterns = [
            ".cache",
            ".git",
            "__pycache__",
            "*.pyc"
        ]
        
        for pattern in patterns:
            for filepath in self.repo_root.rglob(pattern):
                # Skip excluded paths
                if any(excl in str(filepath) for excl in exclude_patterns):
                    continue
                
                try:
                    relative_path = filepath.relative_to(self.repo_root)
                    with open(filepath, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    state[str(relative_path)] = file_hash
                except Exception as e:
                    print(f"Warning: Could not hash {filepath}: {e}")
        
        return state
    
    def _load_state(self) -> Dict[str, str]:
        """Load previous repository state from cache."""
        if not self.state_file.exists():
            return {}
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                return data.get('file_hashes', {})
        except Exception as e:
            print(f"Warning: Could not load state: {e}")
            return {}
    
    def _save_state(self, state: Dict[str, str]):
        """Save current repository state to cache."""
        data = {
            'file_hashes': state,
            'last_update': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_update_prompt(self, changes: Dict[str, List[str]], 
                               target_doc: str = "README.md") -> str:
        """
        Generate a prompt for updating documentation based on changes.
        
        Args:
            changes: Dictionary of added/modified/removed files
            target_doc: Documentation file to update
            
        Returns:
            Prompt string for Gen AI to update documentation
        """
        prompt = f"""
You are a technical documentation specialist maintaining project documentation.

**Task**: Update the existing {target_doc} to reflect recent repository changes.

**CRITICAL**: Only update the sections affected by changes. Do NOT regenerate the entire document.

---

## Repository Changes Detected

**Files Added ({len(changes['added'])}):**
{self._format_file_list(changes['added'])}

**Files Modified ({len(changes['modified'])}):**
{self._format_file_list(changes['modified'])}

**Files Removed ({len(changes['removed'])}):**
{self._format_file_list(changes['removed'])}

---

## Current Documentation

```markdown
{self._read_file(target_doc)}
```

---

## Update Instructions

1. **Analyze Changes**: Determine which sections of {target_doc} are affected
   - New files → Update "File Organization" section
   - Modified SQL → Update "SQL Development" section
   - Modified Power BI → Update "Power BI Report" section
   - Modified model.md → Update "Dimensional Modeling Exercise" section

2. **Generate Differential Update**: Provide ONLY the sections that need updating
   - Format: Section heading + updated content
   - Preserve existing formatting style
   - Maintain markdown structure

3. **Provide Change Summary**: Explain what changed and why the update is needed

---

## Output Format

```json
{{
  "sections_to_update": [
    {{
      "section_name": "File Organization",
      "reason": "New files added: example.sql",
      "updated_content": "...full section content with changes..."
    }},
    {{
      "section_name": "SQL Development",
      "reason": "Query 8 added to sql_assignment.sql",
      "updated_content": "...full section content with changes..."
    }}
  ],
  "changelog_entry": "Added Query 8 for calculating trader commission rates",
  "timestamp": "{datetime.now().isoformat()}"
}}
```

---

**Remember**: 
- Update ONLY affected sections
- Preserve existing tone and formatting
- No emoji or AI-style language
- Keep inline code formatting with backticks
- Maintain H2/H3 hierarchy
"""
        
        return prompt
    
    def _format_file_list(self, files: List[str]) -> str:
        """Format file list for prompt."""
        if not files:
            return "  (none)"
        return "\n".join([f"  - {f}" for f in files])
    
    def _read_file(self, filepath: str) -> str:
        """Read file content safely."""
        try:
            full_path = self.repo_root / filepath
            if not full_path.exists():
                return "(File not found)"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"(Error reading file: {e})"
    
    def apply_updates(self, updates: Dict[str, Any], target_doc: str = "README.md"):
        """
        Apply section updates to documentation file.
        
        Args:
            updates: Dictionary containing sections_to_update
            target_doc: Documentation file to update
        """
        doc_path = self.repo_root / target_doc
        
        if not doc_path.exists():
            print(f"Error: {target_doc} not found")
            return
        
        # Read current documentation
        with open(doc_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Create backup with sanitized filename
        backup_filename = target_doc.replace('\\', '_').replace('/', '_')
        backup_path = self.cache_dir / f"{backup_filename}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(current_content)
        
        print(f"✅ Backup created: {backup_path}")
        
        # Apply each section update
        updated_content = current_content
        
        for section_update in updates.get('sections_to_update', []):
            section_name = section_update['section_name']
            new_content = section_update['updated_content']
            reason = section_update['reason']
            
            print(f"🔄 Updating section: {section_name}")
            print(f"   Reason: {reason}")
            
            # Replace section content
            updated_content = self._replace_section(updated_content, section_name, new_content)
        
        # Write updated documentation
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ {target_doc} updated successfully")
        
        # Save changelog
        self._save_changelog(updates)
        
        # Update state
        current_state = self._get_repo_state()
        self._save_state(current_state)
    
    def _replace_section(self, content: str, section_name: str, new_section_content: str) -> str:
        """
        Replace a section in markdown document.
        
        Args:
            content: Full document content
            section_name: Name of section to replace (H2 heading)
            new_section_content: New content for the section
            
        Returns:
            Updated document content
        """
        lines = content.split('\n')
        result_lines = []
        in_target_section = False
        section_level = None
        skip_until_next_section = False
        
        for line in lines:
            # Check if this is the target section
            if line.startswith('## ') and section_name in line:
                in_target_section = True
                section_level = 2
                skip_until_next_section = True
                # Add the new section content
                result_lines.append(new_section_content)
                continue
            
            # Check if we've reached the next section of same or higher level
            if skip_until_next_section:
                if line.startswith('## '):  # Same level section
                    skip_until_next_section = False
                    in_target_section = False
                elif line.startswith('# '):  # Higher level section
                    skip_until_next_section = False
                    in_target_section = False
                else:
                    continue  # Skip lines in old section
            
            result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _save_changelog(self, updates: Dict[str, Any]):
        """Save changelog entry."""
        changelog_file = self.cache_dir / "CHANGELOG.md"
        
        entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Changes**: {updates.get('changelog_entry', 'Documentation updated')}

**Sections Updated**:
"""
        
        for section_update in updates.get('sections_to_update', []):
            entry += f"- {section_update['section_name']}: {section_update['reason']}\n"
        
        entry += "\n---\n"
        
        # Append to changelog
        if changelog_file.exists():
            with open(changelog_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            entry = entry + existing
        
        with open(changelog_file, 'w', encoding='utf-8') as f:
            f.write(entry)
        
        print(f"✅ Changelog updated: {changelog_file}")
    
    def show_diff(self, target_doc: str = "README.md"):
        """Show what would be updated without making changes."""
        changes = self.detect_changes()
        
        print("=" * 60)
        print("REPOSITORY CHANGES DETECTED")
        print("=" * 60)
        
        print(f"\n📁 Added ({len(changes['added'])}):")
        for f in changes['added']:
            print(f"  + {f}")
        
        print(f"\n✏️  Modified ({len(changes['modified'])}):")
        for f in changes['modified']:
            print(f"  ~ {f}")
        
        print(f"\n🗑️  Removed ({len(changes['removed'])}):")
        for f in changes['removed']:
            print(f"  - {f}")
        
        print("\n" + "=" * 60)
        print(f"DOCUMENTATION UPDATE NEEDED: {target_doc}")
        print("=" * 60)
        
        # Generate update prompt
        prompt = self.generate_update_prompt(changes, target_doc)
        
        print("\n📝 Generated Update Prompt:")
        print(prompt[:500] + "...\n")
        
        print("\nℹ️  To apply updates:")
        print(f"  1. Copy the full prompt (saved to .prompts/.cache/update_prompt.txt)")
        print(f"  2. Send to Gen AI (GPT-4, Claude, etc.)")
        print(f"  3. Save response as .prompts/.cache/updates.json")
        print(f"  4. Run: python documentation_updater_agent.py --apply")
        
        # Save prompt to file
        prompt_file = self.cache_dir / "update_prompt.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"\n✅ Full prompt saved: {prompt_file}")


def main():
    """Command-line interface for Documentation Updater."""
    parser = argparse.ArgumentParser(
        description="Incrementally update documentation based on repository changes"
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Show what would be updated without making changes"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply updates from .prompts/.cache/updates.json"
    )
    parser.add_argument(
        "--target",
        default="README.md",
        help="Target documentation file to update (default: README.md)"
    )
    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="Reset tracking state (next run will treat all files as new)"
    )
    
    args = parser.parse_args()
    
    # Initialize updater
    updater = DocumentationUpdater()
    
    if args.reset_state:
        print("🔄 Resetting documentation tracking state...")
        if updater.state_file.exists():
            updater.state_file.unlink()
        # Create new baseline by saving current state
        current_state = updater._get_repo_state()
        updater._save_state(current_state)
        print("✅ State reset complete")
        return
    
    if args.diff:
        updater.show_diff(args.target)
    
    elif args.apply:
        print(f"📝 Applying updates to {args.target}...")
        
        updates_file = updater.cache_dir / "updates.json"
        if not updates_file.exists():
            print(f"❌ Error: {updates_file} not found")
            print("   Generate updates first with --diff, then create updates.json")
            return
        
        with open(updates_file, 'r') as f:
            updates = json.load(f)
        
        updater.apply_updates(updates, args.target)
    
    else:
        print("Usage:")
        print("  --diff          Show changes and generate update prompt")
        print("  --apply         Apply updates from updates.json")
        print("  --target FILE   Specify documentation file (default: README.md)")
        print("  --reset-state   Reset change tracking")


if __name__ == "__main__":
    main()
