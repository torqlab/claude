#!/usr/bin/env python3
"""
Skill discovery and SKILLS.md generation script.
Discovers all available skills from multiple sources and generates a consolidated SKILLS.md file.
"""

import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Set, Optional
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
        2. Custom skills from .kiro/skills/ and .claude/skills/ (excluding open-source)
        3. Agent skills from ACTUALLY ENABLED plugins only
        """
        # 1. Load open-source skills from skills-lock.json FIRST (establishes baseline)
        open_source_names: Set[str] = set()
        if self.skills_lock_path.exists():
            try:
                lock_data = json.loads(self.skills_lock_path.read_text())
                skills_obj = lock_data.get("skills", {})

                # Handle dict format (typical)
                if isinstance(skills_obj, dict):
                    for skill_name, skill_info in skills_obj.items():
                        open_source_names.add(skill_name)
                        # Extract source repository info for GitHub link
                        source_repo = skill_info.get("source", "anthropics/skills")
                        
                        print(f"  Fetching description for {skill_name}...")
                        description = self._fetch_skill_description_from_github(
                            source_repo, skill_name
                        )
                        
                        # Fallback: if no description from GitHub, try local copy
                        if not description:
                            description = self._fetch_description_from_local(skill_name)
                        
                        self.open_source_skills[skill_name] = {
                            "name": skill_name,
                            "description": description,
                            "source": source_repo,
                            "source_type": skill_info.get("sourceType", "github"),
                            "type": "Open-source",
                        }
                # Handle list format (if applicable)
                elif isinstance(skills_obj, list):
                    for skill in skills_obj:
                        if isinstance(skill, dict):
                            skill_name = skill.get("name") or skill.get("skillPath", "").split("/")[-2]
                            if skill_name:
                                open_source_names.add(skill_name)
                                source_repo = skill.get("source", "anthropics/skills")
                                
                                print(f"  Fetching description for {skill_name}...")
                                description = self._fetch_skill_description_from_github(
                                    source_repo, skill_name
                                )
                                
                                # Fallback: if no description from GitHub, try local copy
                                if not description:
                                    description = self._fetch_description_from_local(skill_name)
                                
                                self.open_source_skills[skill_name] = {
                                    "name": skill_name,
                                    "description": description,
                                    "source": source_repo,
                                    "source_type": skill.get("sourceType", "github"),
                                    "type": "Open-source",
                                }
            except Exception as e:
                print(f"Warning: Failed to parse skills-lock.json: {e}")

        # 2. Discover custom skills from BOTH .kiro/skills/ and .claude/skills/
        # Only skills NOT in skills-lock.json are considered custom
        for skills_base_dir in [self.project_root / ".kiro" / "skills", self.claude_dir / "skills"]:
            if skills_base_dir.exists():
                for skill_dir in skills_base_dir.iterdir():
                    if skill_dir.is_dir():
                        skill_md = skill_dir / "SKILL.md"
                        if skill_md.exists():
                            try:
                                metadata = self._extract_skill_metadata(skill_md)
                                skill_name = metadata.get("name", skill_dir.name)
                                # CRITICAL: Only add as custom if NOT in open-source skills-lock.json
                                if skill_name not in open_source_names:
                                    # Determine relative path from project root
                                    try:
                                        rel_path = skill_md.relative_to(self.project_root)
                                    except ValueError:
                                        rel_path = skill_md
                                    
                                    self.custom_skills[skill_name] = {
                                        "name": skill_name,
                                        "description": metadata.get("description", ""),
                                        "source": f"./{rel_path}",
                                        "type": "Custom",
                                    }
                            except Exception as e:
                                print(f"Warning: Failed to parse {skill_md}: {e}")

        # 3. Discover agent skills from ACTUALLY ENABLED plugins ONLY
        # Do NOT hardcode skills — only include if plugin is explicitly enabled
        if self.settings_path.exists():
            try:
                settings_data = json.loads(self.settings_path.read_text())
                enabled_plugins = settings_data.get("enabledPlugins", {})
                
                # Check if agent-skills plugin is enabled
                if enabled_plugins.get("agent-skills@addy-agent-skills", False):
                    # Plugin is enabled — fetch agent skills list from metadata or hardcoded known list
                    # For now, we use the known list, but it will only be included if the plugin is enabled
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

    def _fetch_skill_description_from_github(
        self, source_repo: str, skill_name: str
    ) -> str:
        """
        Fetch skill description from GitHub repository.
        Constructs URL like: https://raw.githubusercontent.com/source_repo/main/skills/skill_name/SKILL.md
        """
        try:
            # Try common branch names
            for branch in ["main", "master"]:
                # Construct URL to fetch SKILL.md
                github_raw_url = (
                    f"https://raw.githubusercontent.com/{source_repo}/{branch}/"
                    f"skills/{skill_name}/SKILL.md"
                )
                
                try:
                    with urllib.request.urlopen(github_raw_url, timeout=5) as response:
                        content = response.read().decode("utf-8")
                        # Extract description from YAML frontmatter
                        metadata = self._extract_metadata_from_content(content)
                        if metadata.get("description"):
                            return metadata["description"]
                except urllib.error.HTTPError:
                    # Try next branch
                    continue
                except Exception:
                    # Timeout or network error, try next branch
                    continue
        except Exception as e:
            print(f"Warning: Could not fetch description for {skill_name}: {e}")
        
        return ""

    def _extract_metadata_from_content(self, content: str) -> Dict:
        """Extract metadata from SKILL.md content string."""
        if content.startswith("---"):
            try:
                lines = content.split("\n")
                end_idx = next(
                    (i for i in range(1, len(lines)) if lines[i].strip() == "---"),
                    None,
                )
                if end_idx:
                    yaml_content = "\n".join(lines[1:end_idx])
                    metadata = yaml.safe_load(yaml_content) or {}
                    return metadata
            except Exception:
                pass
        return {}

    def _fetch_description_from_local(self, skill_name: str) -> str:
        """
        Fallback: Fetch skill description from local .kiro/skills/ or .claude/skills/ copy.
        """
        for skills_base_dir in [self.project_root / ".kiro" / "skills", self.claude_dir / "skills"]:
            skill_path = skills_base_dir / skill_name / "SKILL.md"
            if skill_path.exists():
                try:
                    metadata = self._extract_skill_metadata(skill_path)
                    if metadata.get("description"):
                        return metadata["description"]
                except Exception:
                    pass
        return ""

    def _generate_decision_trees(
        self, skills_by_type: Dict[str, List[Dict]]
    ) -> List[str]:
        """
        Generate decision trees dynamically based on discovered skills.
        Only include skills that actually exist in the project.
        """
        lines = [
            "",
            "## 🎯 Decision Trees",
            "",
            "Guide for selecting the right skill based on your situation.",
            "This section is generated based on skills available in your project.",
            "",
        ]

        # Get all discovered skill names (flatten all types)
        all_skills = {}
        for skill_list in skills_by_type.values():
            for skill in skill_list:
                all_skills[skill["name"]] = skill

        # Helper to check if skill exists
        def skill_exists(name: str) -> bool:
            return name in all_skills

        # Build decision trees only mentioning existing skills
        trees = []

        # Decision Tree 1: Implementation workflow
        impl_tree = [
            "",
            "### \"I need to implement or build something\"",
            "- Do you have clear requirements?",
            "  - NO → Clarify requirements first, then continue",
            "  - YES → Continue to next question",
        ]

        # Add spec skills if they exist
        spec_skills = [s for s in all_skills.keys() if "spec" in s.lower()]
        if spec_skills:
            impl_tree.extend([
                "- Have you written a specification or design?",
                "  - NO → " + " or ".join(f"`/{s}`" for s in sorted(spec_skills)) + " to write requirements",
                "  - YES → Continue to next question",
            ])

        # Add planning skills if they exist
        plan_skills = [s for s in all_skills.keys() if "plan" in s.lower()]
        if plan_skills:
            impl_tree.extend([
                "- Have you planned the work?",
                "  - NO → " + " or ".join(f"`/{s}`" for s in sorted(plan_skills)) + " to break into tasks",
                "  - YES → Ready to build",
            ])

        # Add build/test/review skills if they exist
        build_skills = [s for s in all_skills.keys() if "build" in s.lower()]
        review_skills = [s for s in all_skills.keys() if "review" in s.lower() or "code-review" in s.lower()]
        test_skills = [s for s in all_skills.keys() if "test" in s.lower() and "debugging" not in s.lower()]

        if build_skills or test_skills or review_skills:
            impl_tree.append("- Ready to build:")
            if build_skills:
                impl_tree.append("  - Use " + " or ".join(f"`/{s}`" for s in sorted(build_skills)))
            if test_skills:
                impl_tree.append("  - Use " + " or ".join(f"`/{s}`" for s in sorted(test_skills)) + " for validation")
            if review_skills:
                impl_tree.append("  - Use " + " or ".join(f"`/{s}`" for s in sorted(review_skills)) + " for quality gate")

        trees.extend(impl_tree)

        # Decision Tree 2: Debugging workflow
        debug_tree = [
            "",
            "### \"Something is broken (bug or test failure)\"",
        ]

        debug_skills = [s for s in all_skills.keys() if "debug" in s.lower() or "error" in s.lower()]
        if debug_skills:
            debug_tree.extend([
                "- Do you understand the root cause?",
                "  - NO → Use " + " or ".join(f"`/{s}`" for s in sorted(debug_skills)) + " for analysis",
                "  - YES → Continue to next question",
            ])

        if test_skills:
            debug_tree.extend([
                "- Have you written a failing test?",
                "  - NO → Use " + " or ".join(f"`/{s}`" for s in sorted(test_skills)) + " to create one",
                "  - YES → Ready to fix",
            ])

        if build_skills:
            debug_tree.append("- Fix the issue:")
            debug_tree.append("  - Use " + " or ".join(f"`/{s}`" for s in sorted(build_skills)))
            if test_skills:
                debug_tree.append("  - Use " + " or ".join(f"`/{s}`" for s in sorted(test_skills)) + " to verify fix")
            if review_skills:
                debug_tree.append("  - Use " + " or ".join(f"`/{s}`" for s in sorted(review_skills)))

        trees.extend(debug_tree)

        # Decision Tree 3: Code Quality / Refactoring
        quality_tree = [
            "",
            "### \"Code quality or refactoring\"",
        ]

        quality_skills = [s for s in all_skills.keys() if "review" in s.lower() or "quality" in s.lower() or "refactor" in s.lower()]
        if quality_skills:
            quality_tree.append("- Use " + " or ".join(f"`/{s}`" for s in sorted(quality_skills)) + " to improve code")

        design_skills = [s for s in all_skills.keys() if "design" in s.lower() or "architecture" in s.lower() or "api" in s.lower()]
        if design_skills:
            quality_tree.append("- Use " + " or ".join(f"`/{s}`" for s in sorted(design_skills)) + " for design guidance")

        doc_skills = [s for s in all_skills.keys() if "doc" in s.lower() or "adr" in s.lower()]
        if doc_skills:
            quality_tree.append("- Use " + " or ".join(f"`/{s}`" for s in sorted(doc_skills)) + " for documentation")

        trees.extend(quality_tree)

        # Decision Tree 4: Performance
        perf_tree = [
            "",
            "### \"Performance optimization\"",
        ]

        perf_skills = [s for s in all_skills.keys() if "performance" in s.lower() or "optimization" in s.lower()]
        if perf_skills:
            perf_tree.append("- Use " + " or ".join(f"`/{s}`" for s in sorted(perf_skills)) + " to identify and fix bottlenecks")

        trees.extend(perf_tree)

        # Decision Tree 5: Security
        sec_tree = [
            "",
            "### \"Security or compliance\"",
        ]

        sec_skills = [s for s in all_skills.keys() if "security" in s.lower() or "hardening" in s.lower()]
        if sec_skills:
            sec_tree.append("- Use " + " or ".join(f"`/{s}`" for s in sorted(sec_skills)) + " for security analysis")

        trees.extend(sec_tree)

        # Note about available skills
        lines.extend(trees)
        lines.extend([
            "",
            "## 📋 Skill Summary",
            "",
            f"Total skills available: {sum(len(v) for v in skills_by_type.values())}",
            f"- Custom: {len(skills_by_type.get('Custom', []))}",
            f"- Open-source: {len(skills_by_type.get('Open-source', []))}",
            f"- Agent Skills: {len(skills_by_type.get('Agent Skill', []))}",
        ])

        return lines

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
            # For custom skills, link to the local SKILL.md file
            source = f"[{skill['source']}]({skill['source']})"
        elif skill_type == "Open-source":
            # For open-source skills, generate GitHub link from source repository
            source_repo = skill.get("source", "anthropics/skills")
            github_url = f"https://github.com/{source_repo}"
            # Extract repo name for link text
            repo_name = source_repo.split("/")[-1]
            source = f"[{source_repo}]({github_url})"
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
            "Project-specific skills maintained in `./.kiro/skills/` and `./.claude/skills/`.",
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
            "Skills from external repositories registered in `skills-lock.json`.",
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
            "Skills from enabled plugins in `.claude/settings.json`.",
            "",
            self.MD_TABLE_HEADER,
            self.MD_TABLE_SEPARATOR,
        ])

        # Add agent skills
        for skill in sorted(skills_by_type.get("Agent Skill", []), key=lambda s: s["name"]):
            lines.append(self._generate_table_row(skill))

        if not skills_by_type.get("Agent Skill"):
            lines.append("| *(No agent skills)* | — | — | — |")

        # Generate dynamic decision trees based on discovered skills
        lines.extend(self._generate_decision_trees(skills_by_type))

        return "\n".join(lines)

    def write_skills_md(self, content: str) -> bool:
        """
        Write SKILLS.md to disk.
        ALWAYS overwrites existing file to ensure no stale data.
        Returns True if file was written/updated.
        """
        # ALWAYS delete existing file first to ensure clean generation
        if self.skills_md_path.exists():
            try:
                self.skills_md_path.unlink()
                print(f"   Removed stale SKILLS.md")
            except Exception as e:
                print(f"Warning: Could not remove existing SKILLS.md: {e}")

        # Write fresh content
        self.skills_md_path.write_text(content)
        return True

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
