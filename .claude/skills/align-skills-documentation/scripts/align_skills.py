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
            # Find skills table rows ONLY in the 📦 Skills section (not directory structures)
            # Match: | **skill-name** | Type | Purpose | Source |
            skills_section = re.search(
                r'### 📦 Skills\s*\n+.*?\n+\| Skill \| Type \| Purpose \| Source \|.*?(?=\n## |\n### )',
                readme_content,
                re.DOTALL | re.IGNORECASE
            )
            if skills_section:
                # Only extract from the skills table section
                table_content = skills_section.group(0)
                matches = re.findall(r'\|\s*\*\*([a-z0-9\-]+)\*\*\s*\|', table_content, re.IGNORECASE)
                documented.update(matches)

            # Extract from trigger context ONLY (- **skill-name**: ...)
            # But limit to the Trigger Context section
            trigger_section = re.search(
                r'### Trigger Context & Usage Patterns.*?(?=\n## |\n### |\Z)',
                readme_content,
                re.DOTALL | re.IGNORECASE
            )
            if trigger_section:
                matches = re.findall(r'-\s+\*\*([a-z0-9\-]+)\*\*:', trigger_section.group(0), re.IGNORECASE)
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

    def _truncate_description(self, text: str, max_length: int = 120) -> str:
        """Truncate description to first sentence or max length."""
        if not text:
            return ""
        # Find first period followed by space or end of string
        match = re.search(r'\.(?:\s|$)', text)
        if match:
            truncated = text[:match.end()].strip()
        else:
            truncated = text[:max_length].strip()
        # Remove trailing period and add it back if truncated
        if len(truncated) > max_length:
            truncated = truncated[:max_length].rsplit(' ', 1)[0] + "..."
        return truncated

    def _generate_skills_table_rows(self) -> List[str]:
        """Generate markdown table rows for all discovered skills, grouped by type."""
        rows = []

        # Sort skills by type: Custom → Open-source → Agent Skills
        type_order = {"Custom": 0, "Open-source": 1, "Agent Skill": 2}
        sorted_skills = sorted(
            self.discovered_skills.items(),
            key=lambda x: (type_order.get(x[1]["type"], 3), x[0])
        )

        for skill_name, skill_info in sorted_skills:
            skill_type = skill_info["type"]
            description = self._truncate_description(skill_info.get("description", ""))

            # Generate source link based on type
            if skill_type == "Custom":
                source = f"[./.claude/skills/{skill_name}/SKILL.md](./.claude/skills/{skill_name}/SKILL.md)"
            elif skill_type == "Open-source":
                source = "[anthropics/skills](https://github.com/anthropics/skills)"
            else:  # Agent Skill
                source = "[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main)"

            # Format row
            row = f"| **{skill_name}** | {skill_type} | {description} | {source} |"
            rows.append(row)

        return rows

    def update_skills_table_in_readme(self) -> List[str]:
        """Update the skills table in README.md with all discovered skills."""
        if not self.readme_path.exists():
            return []

        content = self.readme_path.read_text()

        # Find the skills section and table
        # Pattern: ### 📦 Skills ... | Skill | Type | Purpose | Source |
        skills_section_pattern = r'(### 📦 Skills\s*\n+.*?\n+\| Skill \| Type \| Purpose \| Source \|\s*\n\|.*?\|.*?\|.*?\|.*?\|\s*\n)(.*?)(\n\n### |\n## )'

        match = re.search(skills_section_pattern, content, re.DOTALL | re.IGNORECASE)
        if not match:
            return []

        # Generate new table rows
        new_rows = self._generate_skills_table_rows()
        table_rows_content = "\n".join(new_rows) + "\n"

        # Replace the table content
        new_content = content[:match.start(2)] + table_rows_content + content[match.start(3):]

        if new_content != content:
            self.readme_path.write_text(new_content)
            return [f"Updated README.md skills table with {len(new_rows)} skills"]

        return []

    def generate_trigger_context_section(self) -> str:
        """
        Generate Trigger Context & Usage Patterns section from skill descriptions.
        Extracts trigger patterns and groups by category.
        """
        # Categorize skills by purpose based on descriptions and names
        categories = {
            "Workflow Planning & Specification": [],
            "Implementation & Build": [],
            "Testing & Debugging": [],
            "Code Review & Quality": [],
            "Frontend & UI": [],
            "Custom Project Skills": [],
        }

        for skill_name, skill_info in self.discovered_skills.items():
            description = skill_info.get("description", "").lower()
            name_lower = skill_name.lower()

            # Categorize based on keywords in description and name
            if any(kw in description or kw in name_lower for kw in ["spec", "plan", "requirement", "interview", "idea"]):
                categories["Workflow Planning & Specification"].append((skill_name, skill_info))
            elif any(kw in description or kw in name_lower for kw in ["build", "implement", "semantic-release", "commit"]):
                categories["Implementation & Build"].append((skill_name, skill_info))
            elif any(kw in description or kw in name_lower for kw in ["test", "debug", "error", "test-driven"]):
                categories["Testing & Debugging"].append((skill_name, skill_info))
            elif any(kw in description or kw in name_lower for kw in ["review", "quality", "security", "hardening", "performance"]):
                categories["Code Review & Quality"].append((skill_name, skill_info))
            elif any(kw in description or kw in name_lower for kw in ["frontend", "ui", "design", "browser"]):
                categories["Frontend & UI"].append((skill_name, skill_info))
            elif skill_info["type"] == "Custom":
                categories["Custom Project Skills"].append((skill_name, skill_info))
            else:
                # Default to workflow
                categories["Workflow Planning & Specification"].append((skill_name, skill_info))

        # Build markdown section
        section_lines = ["### Trigger Context & Usage Patterns", ""]

        for category_name, skills in categories.items():
            if skills:
                section_lines.append(f"#### {category_name}")
                for skill_name, skill_info in sorted(skills, key=lambda x: x[0]):
                    description = skill_info.get("description", "")
                    # Extract trigger hint (first sentence or short phrase)
                    trigger_hint = self._truncate_description(description, max_length=80)
                    if trigger_hint:
                        section_lines.append(f"- **{skill_name}**: {trigger_hint}")
                    else:
                        section_lines.append(f"- **{skill_name}**: Use this skill to work with {skill_name.replace('-', ' ')}")
                section_lines.append("")

        return "\n".join(section_lines)

    def update_trigger_context_in_readme(self) -> List[str]:
        """
        Insert or update the Trigger Context & Usage Patterns section in README.md.
        Inserts after the skills table if it doesn't exist.
        """
        if not self.readme_path.exists():
            return []

        content = self.readme_path.read_text()
        new_section = self.generate_trigger_context_section()

        # Check if section already exists
        existing_pattern = r'### Trigger Context & Usage Patterns.*?(?=\n### |\n## |\Z)'
        existing_match = re.search(existing_pattern, content, re.DOTALL | re.IGNORECASE)

        if existing_match:
            # Replace existing section
            new_content = content[:existing_match.start()] + new_section + content[existing_match.end():]
        else:
            # Find insertion point: after skills table ends, before next ### or ## section
            insertion_pattern = r'(### 📦 Skills\s*\n+.*?\n\| Skill \| Type \| Purpose \| Source \|\s*\n(?:\|.*?\n)*)'
            insertion_match = re.search(insertion_pattern, content, re.DOTALL | re.IGNORECASE)

            if insertion_match:
                # Insert after the table
                insert_pos = insertion_match.end()
                new_content = content[:insert_pos] + "\n" + new_section + "\n" + content[insert_pos:]
            else:
                return []

        if new_content != content:
            self.readme_path.write_text(new_content)
            return ["Generated Trigger Context & Usage Patterns section in README.md"]

        return []

    def generate_decision_trees_section(self) -> str:
        """Generate decision tree section for AGENTS.md."""
        section = """## 🎯 Decision Trees

Guide for agents to select the right workflow based on your situation.

### "I need to implement a feature"
- Do you have clear requirements?
  - NO → Use `/interview-me` or `/idea-refine` to clarify, then continue
  - YES → Continue to next question
- Have you written a specification?
  - NO → Use `/spec` to write detailed requirements, then continue
  - YES → Continue to next question
- Have you planned the work?
  - NO → Use `/plan` to break into ordered tasks, then continue
  - YES → Continue to next question
- Ready to build?
  - Use `/build` to implement incrementally
  - As you code, use `/test` for test-driven validation
  - When ready, use `/review` for quality gate
  - Finally, use `/ship` for production launch

### "Something is broken (bug or test failure)"
- Do you understand the root cause?
  - NO → Use `/debugging-and-error-recovery` for systematic analysis
  - YES → Continue to next question
- Is there a failing test?
  - NO → Use `/test` to create a failing test first (TDD approach)
  - YES → Continue to next question
- Ready to fix?
  - Use `/build` to implement the fix
  - Use `/test` to verify the test now passes
  - Use `/review` for quality gate
  - Use `/ship` if deploying

### "Performance is an issue"
- Have you profiled the application?
  - NO → Use `/performance-optimization` to profile and identify bottlenecks
  - YES → Continue to next question
- Ready to optimize?
  - Use `/build` to implement optimizations
  - Use `/test` to verify improvements
  - Use `/review` for quality gate

### "Security concern or compliance requirement"
- Need to harden code?
  - Use `/security-and-hardening` for vulnerability analysis
  - Use `/build` to implement hardening measures
  - Use `/test` to verify security improvements
  - Use `/review` and `/ship` for deployment

### "Refactoring or design work"
- Need API/module design guidance?
  - Use `/api-and-interface-design` for stable interface design
- Need documentation of architectural decisions?
  - Use `/documentation-and-adrs` to record decisions
- Need to review before merging?
  - Use `/code-review-and-quality` for detailed multi-axis review
"""
        return section

    def generate_agent_combinations_section(self) -> str:
        """Generate agent combinations matrix for AGENTS.md."""
        section = """## 🔗 Agent Combinations & Context Flow

Common agent workflow sequences and the context that flows between them.

| Sequence | Prerequisites | Purpose | Output Context |
|----------|---|---------|--------|
| `/interview-me` → `/spec` | Unclear requirements | Clarify and document requirements | Detailed specification |
| `/spec` → `/plan` → `/build` | Clear specification | Feature development workflow | Planned tasks → Implementation |
| `/plan` → `/build` → `/test` → `/review` | Task list | Complete build cycle | Code changes → Tests → Review feedback |
| `/test` → `/build` → `/review` → `/ship` | Failing test | Bug fix and deployment | Test fix → Reviewed code → Production ready |
| `/debugging-and-error-recovery` → `/test` → `/build` | Error symptoms | Systematic debugging | Root cause → Failing test → Fix |
| `/performance-optimization` → `/build` → `/test` | Performance baseline | Performance improvement | Optimization strategy → Implemented → Verified |
| `/security-and-hardening` → `/build` → `/test` → `/review` | Security audit | Security hardening | Hardening strategy → Implementation → Verification |
| `/api-and-interface-design` → `/build` → `/test` | API requirements | Stable interface design | API design → Implementation → Tests |
| `/code-review-and-quality` → `/ship` | Code ready for review | Final quality gate before ship | Review feedback → Ship checklist |
| `/doubt-driven-development` → `/build` | Non-trivial decision | Adversarial review of design | Questioned assumptions → Confirmed approach |
| `/documentation-and-adrs` → `/build` | Architectural decision | Record decision and implement | ADR → Implementation |

**Context flows left-to-right**: Output from one agent becomes the input context for the next agent in the sequence.
"""
        return section

    def generate_custom_skills_integration_section(self) -> str:
        """Generate custom skills integration guide for AGENTS.md."""
        section = """## 🛠️ Custom Skills Integration Guide

Where custom project-specific skills fit into the agent workflow, and how they integrate with agent skills.

| Skill | Purpose | Integration Point | Works With Agents | Sequence |
|-------|---------|-------------------|------------------|----------|
| **semantic-release** | Create feature branches with semantic versioning | During `/plan` → `/build` | `/plan`, `/build` | `/plan` → `/semantic-release` (create branch) → `/build` |
| **git-branch** | Create semantic-release naming convention branches | At start of `/build` | `/plan`, `/build` | `/plan` → `/git-branch` (create) → `/build` |
| **pr** | Create GitHub pull requests aligned with semantic-release | After `/build` when ready for review | `/build`, `/review`, `/ship` | `/build` → `/review` → `/pr` (create) → `/ship` |
| **github-mcp-setup** | Configure GitHub MCP server for automated workflows | Before any `/pr` usage | `/pr` | Setup first, then use `/pr` |
| **align-skills-documentation** | Synchronize documentation with available skills | Before releases or during maintenance | Any workflow | Use after adding new skills |

**Integration strategy**:
- **Branch creation**: Use `/semantic-release` or `/git-branch` early in `/build` phase
- **Code review integration**: `/review` provides feedback context for `/pr` creation
- **Release workflow**: Complete `/build` → `/review` → `/pr` → `/ship` sequence
- **Documentation**: Keep `/align-skills-documentation` up to date after skill additions
"""
        return section

    def generate_agent_context_requirements_section(self) -> str:
        """Generate agent context requirements for AGENTS.md."""
        section = """## 📋 Agent Context Requirements

Prerequisites, inputs, and outputs for each major agent workflow phase.

| Agent | Phase | Prerequisites | Input Context | Output | Success Criteria |
|-------|-------|---|---|--------|------------------|
| `/interview-me` | Requirements | Problem description | Initial idea or requirement | Clarified requirements | Clear understanding of actual needs |
| `/idea-refine` | Requirements | Vague concept | Rough idea or feature request | Actionable requirements | Requirements are specific and measurable |
| `/spec` | Specification | Clear requirements | Requirements document | Detailed specification with acceptance criteria | Spec includes acceptance criteria and edge cases |
| `/plan` | Planning | Specification complete | Detailed spec | Ordered tasks with dependencies | Tasks are ordered, dependencies clear, ready to build |
| `/build` | Implementation | Task list ready | Task description and related spec | Tested, verified, committed code | Code changes committed to feature branch |
| `/test` | Testing | Code or failing test | Code changes or test failure | Passing tests or verified behavior | All tests passing or behavior verified |
| `/review` | Review | Code ready for feedback | Code changes to review | Review feedback or approval | All review feedback addressed |
| `/ship` | Launch | Code reviewed and approved | Approved code and release context | Production deployment checklist | Deployment checklist completed |
| `/debugging-and-error-recovery` | Debugging | Error symptoms or test failure | Error message, logs, or failing test | Root cause identified | Root cause documented and understood |
| `/performance-optimization` | Optimization | Performance baseline | Baseline metrics and code | Optimization strategy and/or implementation | Performance improved per requirements |
| `/security-and-hardening` | Security | Security audit or vulnerability | Code to audit or vulnerability details | Hardening strategy or implementation | Security improvements verified |
| `/frontend-ui-engineering` | Frontend | Design requirements | UI requirements or design specs | Implemented UI components | UI passes acceptance criteria |
| `/api-and-interface-design` | Architecture | API requirements | API requirements or module spec | Stable interface design | API design reviewed and documented |

**Context inheritance**: Later phases build on outputs from earlier phases. Each output becomes input context for the next agent in the workflow.
"""
        return section

    def update_agents_md_sections(self) -> List[str]:
        """
        Update or insert all 4 new sections in AGENTS.md.
        Returns list of sections updated.
        """
        if not self.agents_md_path.exists():
            return []

        updates = []

        # Generate new sections
        decision_trees = self.generate_decision_trees_section()
        combinations = self.generate_agent_combinations_section()
        custom_skills = self.generate_custom_skills_integration_section()
        context_reqs = self.generate_agent_context_requirements_section()

        # Update each section
        if self._update_markdown_section(self.agents_md_path, "🎯 Decision Trees", decision_trees):
            updates.append("Updated Decision Trees section")
        if self._update_markdown_section(self.agents_md_path, "🔗 Agent Combinations & Context Flow", combinations):
            updates.append("Updated Agent Combinations section")
        if self._update_markdown_section(self.agents_md_path, "🛠️ Custom Skills Integration Guide", custom_skills):
            updates.append("Updated Custom Skills Integration section")
        if self._update_markdown_section(self.agents_md_path, "📋 Agent Context Requirements", context_reqs):
            updates.append("Updated Agent Context Requirements section")

        return updates

    def _update_markdown_section(self, file_path: Path, section_header: str, new_content: str) -> bool:
        """
        Update or insert a markdown section.
        Returns True if updated, False otherwise.
        """
        content = file_path.read_text()
        original_content = content

        # Normalize header search (handle emoji and variations)
        # Extract the meaningful part of the header
        header_key = section_header.replace("## ", "").replace("### ", "")

        # Look for section with either ## or ### format
        pattern = rf'(#{"{2,3}"}\s+.*{re.escape(header_key)}.*?\n)(.*?)(?=\n#{"{2,3}"}\s+|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            # Replace existing section
            new_content_with_header = new_content if new_content.startswith("#") else f"## {section_header}\n\n{new_content}"
            content = content[:match.start()] + new_content_with_header + content[match.end():]
        else:
            # Insert new section before "Getting Help" or at end
            insertion_point_pattern = r'\n## Getting Help'
            insertion_match = re.search(insertion_point_pattern, content, re.IGNORECASE)

            if insertion_match:
                insert_pos = insertion_match.start()
                new_section = f"{new_content}\n"
                content = content[:insert_pos] + "\n" + new_section + content[insert_pos:]
            else:
                # Insert before last "---" or at end
                if content.rstrip().endswith("---"):
                    insert_pos = content.rfind("\n---")
                    content = content[:insert_pos] + "\n\n" + new_content + "\n" + content[insert_pos:]
                else:
                    content = content.rstrip() + "\n\n" + new_content + "\n"

        if content != original_content:
            file_path.write_text(content)
            return True

        return False

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

        print("\n📝 Updating README.md skills table...")
        readme_updates = self.update_skills_table_in_readme()
        if readme_updates:
            for update in readme_updates:
                print(f"   ✓ {update}")
        else:
            print("   ✓ Skills table already up to date")

        print("\n📝 Updating Trigger Context section...")
        context_updates = self.update_trigger_context_in_readme()
        if context_updates:
            for update in context_updates:
                print(f"   ✓ {update}")
        else:
            print("   ✓ Trigger context section already up to date")

        print("\n📖 Updating AGENTS.md sections...")
        agents_updates = self.update_agents_md_sections()
        if agents_updates:
            for update in agents_updates:
                print(f"   ✓ {update}")
        else:
            print("   ✓ AGENTS.md sections already up to date")

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
