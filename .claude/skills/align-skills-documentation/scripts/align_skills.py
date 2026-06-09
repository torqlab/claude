#!/usr/bin/env python3
"""
Skill discovery and documentation alignment script.
Detects all available skills and removes non-existing skills from documentation.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import yaml


class SkillAligner:
    """Aligns skills documentation with actual available skills."""

    def __init__(self, project_root: Path = Path.cwd()):
        """Initialize with project root."""
        self.project_root = project_root
        self.claude_dir = project_root / ".claude"
        self.readme_path = project_root / "README.md"
        self.agents_md_path = project_root / "AGENTS.md"
        self.skills_lock_path = project_root / "skills-lock.json"
        self.settings_path = self.claude_dir / "settings.json"

        self.discovered_skills: Dict[str, Dict] = {}
        self.documented_skills: Set[str] = set()
        self.removed_skills: List[Tuple[str, List[str]]] = []  # (skill_name, locations_removed_from)
        self.report: Dict = {}

    def discover_skills(self) -> Dict[str, Dict]:
        """
        Discover all available skills from multiple sources.
        Returns dict of {skill_name: {name, type, path, description, source}}

        Discovery order matters:
        1. First, identify open-source skills from skills-lock.json (these take priority)
        2. Then discover custom skills, excluding those already in skills-lock.json
        3. Finally, discover agent skills from enabled plugins
        """
        discovered = {}
        open_source_skill_names = set()

        # 1. Discover NPM-based open-source skills FIRST (priority)
        if self.skills_lock_path.exists():
            try:
                lock_data = json.loads(self.skills_lock_path.read_text())
                skills_obj = lock_data.get("skills", {})
                # Handle both array format and object format
                if isinstance(skills_obj, list):
                    skills_to_process = skills_obj
                else:
                    skills_to_process = skills_obj.values() if isinstance(skills_obj, dict) else []

                for skill in skills_to_process:
                    if isinstance(skill, dict):
                        skill_name = skill.get("name") or skill.get("skillPath", "").split("/")[-2]
                    else:
                        skill_name = skill

                    if skill_name:
                        open_source_skill_names.add(skill_name)
                        discovered[skill_name] = {
                            "type": "Open-source",
                            "name": skill_name,
                            "description": "",
                            "source": "anthropics/skills",
                        }
            except Exception as e:
                print(f"Warning: Failed to parse skills-lock.json: {e}")

        # 2. Discover custom skills from .claude/skills/ (exclude open-source)
        custom_skills_dir = self.claude_dir / "skills"
        if custom_skills_dir.exists():
            for skill_dir in custom_skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    # CRITICAL: Verify file exists before documenting
                    if skill_md.exists():
                        try:
                            metadata = self._extract_skill_metadata(skill_md)
                            skill_name = metadata.get("name", skill_dir.name)

                            # Skip if already registered as open-source
                            if skill_name not in open_source_skill_names:
                                discovered[skill_name] = {
                                    "type": "Custom",
                                    "path": str(skill_md),
                                    "name": skill_name,
                                    "description": metadata.get("description", ""),
                                    "source": f"./.claude/skills/{skill_dir.name}/SKILL.md",
                                }
                        except Exception as e:
                            print(f"Warning: Failed to parse {skill_md}: {e}")

        # 3. Discover agent skills from plugins
        if self.settings_path.exists():
            try:
                settings_data = json.loads(self.settings_path.read_text())
                enabled_plugins = settings_data.get("enabledPlugins", {})
                if enabled_plugins.get("agent-skills@addy-agent-skills", False):
                    # Add known agent skills
                    agent_skills = [
                        "spec", "plan", "build", "test", "review", "ship",
                        "interview-me", "idea-refine", "code-simplify",
                        "frontend-ui-engineering", "api-and-interface-design",
                        "performance-optimization", "debugging-and-error-recovery",
                        "ci-cd-and-automation", "deprecation-and-migration",
                        "git-workflow-and-versioning", "code-review-and-quality",
                        "browser-testing-with-devtools", "documentation-and-adrs",
                        "security-and-hardening", "incremental-implementation",
                        "source-driven-development", "spec-driven-development",
                        "test-driven-development", "doubt-driven-development",
                        "shipping-and-launch", "context-engineering",
                        "using-agent-skills", "planning-and-task-breakdown"
                    ]
                    for skill_name in agent_skills:
                        discovered[skill_name] = {
                            "type": "Agent Skill",
                            "name": skill_name,
                            "description": "",
                            "source": "addyosmani/agent-skills",
                        }
            except Exception as e:
                print(f"Warning: Failed to parse settings.json: {e}")

        self.discovered_skills = discovered
        return discovered

    def _extract_skill_metadata(self, skill_file: Path) -> Dict:
        """Extract metadata from SKILL.md frontmatter."""
        content = skill_file.read_text()

        # Parse YAML frontmatter
        if content.startswith("---"):
            try:
                lines = content.split("\n")
                end_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
                yaml_content = "\n".join(lines[1:end_idx])
                metadata = yaml.safe_load(yaml_content) or {}
                return metadata
            except Exception as e:
                raise ValueError(f"Failed to parse YAML frontmatter: {e}")

        return {"name": skill_file.parent.name, "description": ""}

    def extract_documented_skills(self) -> Set[str]:
        """
        Extract all skills mentioned in README.md and AGENTS.md.
        Returns set of skill names found in documentation.
        """
        documented = set()

        # Extract from README.md skills table
        if self.readme_path.exists():
            readme_content = self.readme_path.read_text()
            # Find skills table rows (format: | **skill-name** | ...)
            matches = re.findall(r'\|\s*\*\*([a-z0-9\-]+)\*\*\s*\|', readme_content, re.IGNORECASE)
            documented.update(matches)

            # Extract from directory structure (├── skill-name/)
            matches = re.findall(r'├──\s+([a-z0-9\-]+)/', readme_content, re.IGNORECASE)
            documented.update(matches)

            # Extract from trigger context (- **skill-name**: ...)
            matches = re.findall(r'-\s+\*\*([a-z0-9\-]+)\*\*:', readme_content, re.IGNORECASE)
            documented.update(matches)

        # Extract from AGENTS.md custom skills table
        if self.agents_md_path.exists():
            agents_content = self.agents_md_path.read_text()
            # Find custom skills integration guide entries
            matches = re.findall(r'\|\s*\*\*([a-z0-9\-]+)\*\*\s*\|', agents_content, re.IGNORECASE)
            documented.update(matches)

        self.documented_skills = documented
        return documented

    def find_orphaned_skills(self) -> Set[str]:
        """
        Find skills documented but not discovered (orphaned/deleted skills).
        Returns set of orphaned skill names.
        """
        discovered_names = set(self.discovered_skills.keys())
        orphaned = self.documented_skills - discovered_names
        return orphaned

    def remove_orphaned_skills_from_readme(self, orphaned: Set[str]) -> List[str]:
        """
        Remove all references to orphaned skills from README.md.
        Returns list of locations cleaned.
        """
        if not self.readme_path.exists():
            return []

        content = self.readme_path.read_text()
        original_content = content
        locations_cleaned = []

        for skill_name in orphaned:
            # Pattern for table row: | **skill-name** | ... |
            # Match entire row starting with skill name
            pattern = rf'\|\s*\*\*{re.escape(skill_name)}\*\*\s*\|[^\n]*\n'
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, '', content, flags=re.IGNORECASE)
                locations_cleaned.append(f"README.md skills table: {skill_name}")

            # Remove from directory structure listing
            # Pattern: ├── skill-name/ or │   ├── skill-name/
            pattern = rf'^\s*[│\s]*├──\s+{re.escape(skill_name)}/\n'
            if re.search(pattern, content, re.MULTILINE):
                content = re.sub(pattern, '', content, flags=re.MULTILINE)
                locations_cleaned.append(f"README.md directory structure: {skill_name}")

            # Remove from trigger context section
            # Pattern: - **skill-name**: Use when...
            pattern = rf'^\s*-\s+\*\*{re.escape(skill_name)}\*\*:.*\n'
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE)
                locations_cleaned.append(f"README.md trigger context: {skill_name}")

        if content != original_content:
            self.readme_path.write_text(content)

        return locations_cleaned

    def remove_orphaned_skills_from_agents_md(self, orphaned: Set[str]) -> List[str]:
        """
        Remove all references to orphaned skills from AGENTS.md.
        Returns list of locations cleaned.
        """
        if not self.agents_md_path.exists():
            return []

        content = self.agents_md_path.read_text()
        original_content = content
        locations_cleaned = []

        for skill_name in orphaned:
            # Pattern for custom skills table row
            pattern = rf'\|\s*\*\*{re.escape(skill_name)}\*\*\s*\|[^\n]*\n'
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, '', content, flags=re.IGNORECASE)
                locations_cleaned.append(f"AGENTS.md custom skills table: {skill_name}")

            # Remove from custom skills integration guide
            pattern = rf'\|\s*/{re.escape(skill_name)}\s*\|[^\n]*\n'
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, '', content, flags=re.IGNORECASE)
                locations_cleaned.append(f"AGENTS.md integration guide: {skill_name}")

            # Remove any narrative references
            pattern = rf'/({re.escape(skill_name)}|{re.escape(skill_name.replace("-", "_"))})'
            matches = len(re.findall(pattern, content, re.IGNORECASE))
            if matches > 0:
                # Only remove if in clear removable sections (not in examples)
                # This is conservative to avoid breaking documentation
                pass

        if content != original_content:
            self.agents_md_path.write_text(content)

        return locations_cleaned

    def generate_report(self) -> Dict:
        """Generate comprehensive alignment report."""
        orphaned = self.find_orphaned_skills()

        report = {
            "timestamp": str(Path(".").resolve().stat().st_mtime),
            "discovered_skills_count": len(self.discovered_skills),
            "documented_skills_count": len(self.documented_skills),
            "discovered_by_type": {
                "Custom": len([s for s in self.discovered_skills.values() if s["type"] == "Custom"]),
                "Open-source": len([s for s in self.discovered_skills.values() if s["type"] == "Open-source"]),
                "Agent Skill": len([s for s in self.discovered_skills.values() if s["type"] == "Agent Skill"]),
            },
            "orphaned_skills": sorted(list(orphaned)),
            "orphaned_count": len(orphaned),
            "cleanup_summary": self.removed_skills,
            "documentation_clean": len(orphaned) == 0,
        }

        return report

    def run(self):
        """Execute full alignment workflow."""
        print("🔍 Discovering available skills...")
        self.discover_skills()
        print(f"   Found {len(self.discovered_skills)} available skills")

        print("📚 Extracting documented skills...")
        self.extract_documented_skills()
        print(f"   Found {len(self.documented_skills)} documented skills")

        orphaned = self.find_orphaned_skills()
        if orphaned:
            print(f"\n🧹 Removing {len(orphaned)} orphaned skills from documentation...")
            print(f"   Orphaned skills: {', '.join(sorted(orphaned))}")

            # Remove from README.md
            readme_cleaned = self.remove_orphaned_skills_from_readme(orphaned)
            if readme_cleaned:
                print(f"   ✓ README.md cleaned: {len(readme_cleaned)} locations")
                for location in readme_cleaned:
                    print(f"     - {location}")

            # Remove from AGENTS.md
            agents_cleaned = self.remove_orphaned_skills_from_agents_md(orphaned)
            if agents_cleaned:
                print(f"   ✓ AGENTS.md cleaned: {len(agents_cleaned)} locations")
                for location in agents_cleaned:
                    print(f"     - {location}")

            # Track removals
            for skill in orphaned:
                all_locations = readme_cleaned + agents_cleaned
                skill_locations = [loc for loc in all_locations if skill in loc]
                self.removed_skills.append((skill, skill_locations))

            print(f"\n✅ Cleanup complete!")
        else:
            print("✅ No orphaned skills found - documentation is clean!")

        # Generate report
        self.report = self.generate_report()

        # Print summary
        print("\n📋 Summary Report")
        print(f"   Discovered: {self.report['discovered_skills_count']} skills")
        print(f"   - Custom: {self.report['discovered_by_type']['Custom']}")
        print(f"   - Open-source: {self.report['discovered_by_type']['Open-source']}")
        print(f"   - Agent Skills: {self.report['discovered_by_type']['Agent Skill']}")
        print(f"   Documented: {self.report['documented_skills_count']} skills")
        if orphaned:
            print(f"   Removed: {self.report['orphaned_count']} orphaned skills")
            print(f"   Status: ⚠️  Documentation updated")
        else:
            print(f"   Status: ✅ Documentation in sync")

        return self.report


if __name__ == "__main__":
    aligner = SkillAligner(Path.cwd())
    report = aligner.run()
    print(json.dumps(report, indent=2))
