#!/usr/bin/env python3
"""
Skill discovery and SKILLS.md generation script.
Discovers all available skills from multiple sources and generates a consolidated SKILLS.md file.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set
import yaml


class SkillAligner:
    """Generates SKILLS.md documentation with discovered skills."""

    # Standard markdown table format (constant across projects)
    MD_TABLE_HEADER = "| Skill | Type | Description | Source |"
    MD_TABLE_SEPARATOR = "|-------|------|-------------|--------|"

    def __init__(self, project_root: Path = Path.cwd()):
        """Initialize with project root."""
        self.project_root = project_root
        self.claude_dir = project_root / ".claude"
        self.skills_md_path = project_root / "SKILLS.md"
        self.skills_lock_path = project_root / "skills-lock.json"
        self.settings_path = self.claude_dir / "settings.json"

        self.custom_skills: Dict[str, Dict] = {}
        self.open_source_skills: Dict[str, Dict] = {}
        self.agent_skills: Dict[str, Dict] = {}
        self.report: Dict = {}

    def discover_skills(self) -> Dict[str, List[Dict]]:
        """
        Discover all available skills from multiple sources.
        Returns dict organized by type: {type -> [skills]}

        Discovery order (with deduplication):
        1. Open-source skills from skills-lock.json (priority)
        2. Custom skills from .claude/skills/ (excluding open-source)
        3. Agent skills from enabled plugins
        """
        # 1. Discover open-source skills from skills-lock.json FIRST (priority)
        if self.skills_lock_path.exists():
            try:
                lock_data = json.loads(self.skills_lock_path.read_text())
                skills_obj = lock_data.get("skills", {})

                # Handle both dict and list formats
                if isinstance(skills_obj, dict):
                    for skill_name, skill_info in skills_obj.items():
                        self.open_source_skills[skill_name] = {
                            "name": skill_name,
                            "description": "",
                            "source": "anthropics/skills",
                            "type": "Open-source",
                        }
                elif isinstance(skills_obj, list):
                    for skill in skills_obj:
                        if isinstance(skill, dict):
                            skill_name = skill.get("name") or skill.get("skillPath", "").split("/")[-2]
                            if skill_name:
                                self.open_source_skills[skill_name] = {
                                    "name": skill_name,
                                    "description": "",
                                    "source": "anthropics/skills",
                                    "type": "Open-source",
                                }
            except Exception as e:
                print(f"Warning: Failed to parse skills-lock.json: {e}")

        # 2. Discover custom skills from .claude/skills/ (exclude open-source)
        custom_skills_dir = self.claude_dir / "skills"
        if custom_skills_dir.exists():
            for skill_dir in custom_skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        try:
                            metadata = self._extract_skill_metadata(skill_md)
                            skill_name = metadata.get("name", skill_dir.name)
                            # CRITICAL: Only add as custom if NOT already in open-source
                            if skill_name not in self.open_source_skills:
                                self.custom_skills[skill_name] = {
                                    "name": skill_name,
                                    "description": metadata.get("description", ""),
                                    "source": f"./.claude/skills/{skill_dir.name}/SKILL.md",
                                    "type": "Custom",
                                }
                        except Exception as e:
                            print(f"Warning: Failed to parse {skill_md}: {e}")

        # 3. Discover agent skills from plugins
        if self.settings_path.exists():
            try:
                settings_data = json.loads(self.settings_path.read_text())
                enabled_plugins = settings_data.get("enabledPlugins", {})
                if enabled_plugins.get("agent-skills@addy-agent-skills", False):
                    # Known agent skills from addyosmani/agent-skills
                    agent_skills_list = [
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
                    for skill_name in agent_skills_list:
                        self.agent_skills[skill_name] = {
                            "name": skill_name,
                            "description": "",
                            "source": "addyosmani/agent-skills",
                            "type": "Agent Skill",
                        }
            except Exception as e:
                print(f"Warning: Failed to parse settings.json: {e}")

        return {
            "Custom": list(self.custom_skills.values()),
            "Open-source": list(self.open_source_skills.values()),
            "Agent Skill": list(self.agent_skills.values()),
        }

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

    def _truncate_description(self, text: str, max_length: int = 100) -> str:
        """Truncate description to first sentence or max length."""
        if not text:
            return ""
        # Find first period or newline
        match = re.search(r'\.(?:\s|$)|\n', text)
        if match:
            truncated = text[:match.end()].strip()
        else:
            truncated = text[:max_length].strip()
        # Remove trailing period and add ellipsis if truncated
        if len(truncated) > max_length:
            truncated = truncated[:max_length].rsplit(' ', 1)[0] + "..."
        return truncated

    def _generate_table_row(self, skill: Dict) -> str:
        """Generate a markdown table row for a skill."""
        skill_name = skill["name"]
        skill_type = skill["type"]
        description = self._truncate_description(skill["description"])

        # Generate source link based on type
        if skill_type == "Custom":
            source = f"[{skill['source']}]({skill['source']})"
        elif skill_type == "Open-source":
            source = "[anthropics/skills](https://github.com/anthropics/skills)"
        else:  # Agent Skill
            source = "[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)"

        return f"| **{skill_name}** | {skill_type} | {description} | {source} |"

    def generate_skills_md(self, skills_by_type: Dict[str, List[Dict]]) -> str:
        """Generate the complete SKILLS.md content."""
        lines = [
            "# Available Skills",
            "",
            "This document lists all available skills organized by type.",
            "",
            "## Custom Skills",
            "",
            "Project-specific skills maintained in `./.claude/skills/`.",
            "",
            self.MD_TABLE_HEADER,
            self.MD_TABLE_SEPARATOR,
        ]

        # Add custom skills
        for skill in sorted(skills_by_type.get("Custom", []), key=lambda s: s["name"]):
            lines.append(self._generate_table_row(skill))

        if not skills_by_type.get("Custom"):
            lines.append("| *(No custom skills)* | — | — | — |")

        lines.extend([
            "",
            "## Open-source Skills",
            "",
            "Skills from [anthropics/skills](https://github.com/anthropics/skills) registered in `skills-lock.json`.",
            "",
            self.MD_TABLE_HEADER,
            self.MD_TABLE_SEPARATOR,
        ])

        # Add open-source skills
        for skill in sorted(skills_by_type.get("Open-source", []), key=lambda s: s["name"]):
            lines.append(self._generate_table_row(skill))

        if not skills_by_type.get("Open-source"):
            lines.append("| *(No open-source skills)* | — | — | — |")

        lines.extend([
            "",
            "## Agent Skills",
            "",
            "Skills from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) plugin.",
            "",
            self.MD_TABLE_HEADER,
            self.MD_TABLE_SEPARATOR,
        ])

        # Add agent skills
        for skill in sorted(skills_by_type.get("Agent Skill", []), key=lambda s: s["name"]):
            lines.append(self._generate_table_row(skill))

        if not skills_by_type.get("Agent Skill"):
            lines.append("| *(No agent skills)* | — | — | — |")

        # Add decision tree section
        lines.extend([
            "",
            "## 🎯 Decision Trees",
            "",
            "Guide for selecting the right skill based on your situation.",
            "",
            "### \"I need to implement a feature\"",
            "- Do you have clear requirements?",
            "  - NO → Use `/interview-me` or `/idea-refine` to clarify, then continue",
            "  - YES → Continue to next question",
            "- Have you written a specification?",
            "  - NO → Use `/spec` to write detailed requirements, then continue",
            "  - YES → Continue to next question",
            "- Have you planned the work?",
            "  - NO → Use `/plan` to break into ordered tasks, then continue",
            "  - YES → Continue to next question",
            "- Ready to build?",
            "  - Use `/build` to implement incrementally",
            "  - As you code, use `/test` for test-driven validation",
            "  - When ready, use `/review` for quality gate",
            "  - Finally, use `/ship` for production launch",
            "",
            "### \"Something is broken (bug or test failure)\"",
            "- Do you understand the root cause?",
            "  - NO → Use `/debugging-and-error-recovery` for systematic analysis",
            "  - YES → Continue to next question",
            "- Is there a failing test?",
            "  - NO → Use `/test` to create a failing test first (TDD approach)",
            "  - YES → Continue to next question",
            "- Ready to fix?",
            "  - Use `/build` to implement the fix",
            "  - Use `/test` to verify the test now passes",
            "  - Use `/review` for quality gate",
            "  - Use `/ship` if deploying",
            "",
            "### \"Performance is an issue\"",
            "- Have you profiled the application?",
            "  - NO → Use `/performance-optimization` to profile and identify bottlenecks",
            "  - YES → Continue to next question",
            "- Ready to optimize?",
            "  - Use `/build` to implement optimizations",
            "  - Use `/test` to verify improvements",
            "  - Use `/review` for quality gate",
            "",
            "### \"Security concern or compliance requirement\"",
            "- Need to harden code?",
            "  - Use `/security-and-hardening` for vulnerability analysis",
            "  - Use `/build` to implement hardening measures",
            "  - Use `/test` to verify security improvements",
            "  - Use `/review` and `/ship` for deployment",
            "",
            "### \"Refactoring or design work\"",
            "- Need API/module design guidance?",
            "  - Use `/api-and-interface-design` for stable interface design",
            "- Need documentation of architectural decisions?",
            "  - Use `/documentation-and-adrs` to record decisions",
            "- Need to review before merging?",
            "  - Use `/code-review-and-quality` for detailed multi-axis review",
        ])

        return "\n".join(lines)

    def write_skills_md(self, content: str) -> bool:
        """Write SKILLS.md to disk. Returns True if file was written/updated."""
        original_content = None
        if self.skills_md_path.exists():
            original_content = self.skills_md_path.read_text()

        self.skills_md_path.write_text(content)

        if original_content is None:
            return True
        return original_content != content

    def generate_report(self) -> Dict:
        """Generate comprehensive discovery report."""
        total_skills = len(self.custom_skills) + len(self.open_source_skills) + len(self.agent_skills)

        report = {
            "timestamp": str(self.project_root.stat().st_mtime),
            "total_skills_discovered": total_skills,
            "by_type": {
                "Custom": len(self.custom_skills),
                "Open-source": len(self.open_source_skills),
                "Agent Skill": len(self.agent_skills),
            },
            "custom_skills": sorted(list(self.custom_skills.keys())),
            "open_source_skills": sorted(list(self.open_source_skills.keys())),
            "agent_skills": sorted(list(self.agent_skills.keys())),
            "skills_md_generated": True,
        }

        return report

    def run(self) -> Dict:
        """Execute full skill discovery and SKILLS.md generation workflow."""
        print("🔍 Discovering available skills...")
        skills_by_type = self.discover_skills()

        total = sum(len(skills) for skills in skills_by_type.values())
        print(f"   Found {total} available skills")
        print(f"   - Custom: {len(self.custom_skills)}")
        print(f"   - Open-source: {len(self.open_source_skills)}")
        print(f"   - Agent Skills: {len(self.agent_skills)}")

        print("\n📝 Generating SKILLS.md...")
        content = self.generate_skills_md(skills_by_type)

        print("\n💾 Writing SKILLS.md...")
        was_written = self.write_skills_md(content)
        if was_written:
            print(f"   ✓ SKILLS.md generated at {self.skills_md_path}")
        else:
            print(f"   ✓ SKILLS.md already up to date")

        # Generate report
        self.report = self.generate_report()

        # Print summary
        print("\n📋 Discovery Summary")
        print(f"   Total skills: {self.report['total_skills_discovered']}")
        print(f"   - Custom: {self.report['by_type']['Custom']}")
        print(f"   - Open-source: {self.report['by_type']['Open-source']}")
        print(f"   - Agent Skills: {self.report['by_type']['Agent Skill']}")
        print(f"   Status: ✅ SKILLS.md synchronized")

        return self.report


if __name__ == "__main__":
    aligner = SkillAligner(Path.cwd())
    report = aligner.run()
    print("\n" + json.dumps(report, indent=2))
