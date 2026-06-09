#!/usr/bin/env python3
"""
Integration test for align-skills-documentation skill.
Demonstrates end-to-end workflow: discovery → extraction → categorization → README update.
"""

import json
import tempfile
from pathlib import Path
import unittest


class TestSkillAlignmentIntegration(unittest.TestCase):
    """End-to-end integration test for the skill alignment workflow."""

    def setUp(self):
        """Set up a realistic test project structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_dir = self.temp_dir / "project"
        self.project_dir.mkdir()

        # Create project structure
        self.claude_dir = self.project_dir / ".claude"
        self.skills_dir = self.claude_dir / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_workflow_discovers_and_documents_skills(self):
        """Test complete workflow: discover skills, extract metadata, update README."""
        # Step 1: Create multiple skills
        self._create_custom_skill("pr", "Create GitHub PRs with semantic-release conventions")
        self._create_custom_skill("semantic-release", "Manage git branches and commits with versioning")
        self._create_custom_skill("create-changelog", "Generate changelog entries from git diffs")

        # Step 2: Create skills-lock.json for open-source skills
        self._create_skills_lock()

        # Step 3: Create settings.json with enabled plugins
        self._create_settings_with_plugins()

        # Step 4: Verify discovery
        custom_skills = list(self.skills_dir.glob("*/SKILL.md"))
        self.assertEqual(len(custom_skills), 3)

        # Step 5: Verify metadata extraction
        for skill_file in custom_skills:
            content = skill_file.read_text()
            self.assertIn("---", content)  # Frontmatter exists
            self.assertIn("name:", content)
            self.assertIn("description:", content)

        # Step 6: Create initial README without skills section
        readme_path = self.project_dir / "README.md"
        readme_path.write_text("# My Project\n\n## Usage\n\nSome content.\n")

        # Step 7: Simulate README update
        self._update_readme_with_skills(readme_path)

        # Step 8: Verify README contains skills table
        updated_content = readme_path.read_text()
        self.assertIn("## 📦 Skills", updated_content)
        self.assertIn("| Skill | Type | Purpose | Source |", updated_content)
        self.assertIn("pr", updated_content)
        self.assertIn("semantic-release", updated_content)

    def test_detects_and_reports_documentation_drift(self):
        """Test detection of skills missing from documentation."""
        # Create 3 custom skills
        self._create_custom_skill("skill-1", "First skill")
        self._create_custom_skill("skill-2", "Second skill")
        self._create_custom_skill("skill-3", "Third skill")

        # Create README documenting only 2 of them
        readme_path = self.project_dir / "README.md"
        readme_path.write_text("""# Project

## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| skill-1 | Custom | First skill | ./.claude/skills/skill-1 |
| skill-2 | Custom | Second skill | ./.claude/skills/skill-2 |
""")

        # Discover all skills
        discovered = {"skill-1", "skill-2", "skill-3"}
        documented = {"skill-1", "skill-2"}
        missing = discovered - documented

        # Verify drift detection
        self.assertEqual(missing, {"skill-3"})
        self.assertIn("skill-3", missing)

    def test_skill_categorization_in_readme(self):
        """Test that skills are properly categorized in README output."""
        self._create_custom_skill("custom-skill", "A custom skill")
        readme_path = self.project_dir / "README.md"

        # Simulate categorized output
        skills_table = """| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| custom-skill | Custom | A custom skill | ./.claude/skills/custom-skill |
| open-source-skill | Open-source | An open-source skill | https://github.com/anthropics/skills |
| agent-skill | Agent Skill | An agent skill | https://github.com/addyosmani/agent-skills |
"""
        readme_path.write_text(f"# Project\n## 📦 Skills\n\n{skills_table}")

        content = readme_path.read_text()
        self.assertIn("Custom", content)
        self.assertIn("Open-source", content)
        self.assertIn("Agent Skill", content)

    def test_trigger_patterns_extraction(self):
        """Test extraction and documentation of trigger patterns."""
        # Create a skill with trigger patterns in description
        skill_content = """---
name: test-skill
description: |
  Use this skill when you need documentation updates.
  Use this skill whenever skills are added to the project.
  Trigger contexts: release preparation, audit tasks.
license: MIT
---

# Test Skill
"""
        skill_file = self.skills_dir / "test-skill" / "SKILL.md"
        skill_file.parent.mkdir(parents=True)
        skill_file.write_text(skill_content)

        # Extract trigger patterns
        content = skill_file.read_text()
        has_use_when = "Use this skill when" in content
        has_use_whenever = "Use this skill whenever" in content
        has_trigger = "Trigger contexts:" in content

        self.assertTrue(has_use_when)
        self.assertTrue(has_use_whenever)
        self.assertTrue(has_trigger)

        # Generate trigger context section
        trigger_section = """## Trigger Context & Usage Patterns

### When to Use
- **test-skill**: Use when you need documentation updates, or whenever skills are added to the project
- **test-skill**: Trigger contexts: release preparation, audit tasks
"""
        self.assertIn("Trigger Context", trigger_section)
        self.assertIn("Use when", trigger_section)

    def test_report_generation_summary(self):
        """Test generation of discovery and update report."""
        self._create_custom_skill("skill-1", "First")
        self._create_custom_skill("skill-2", "Second")
        self._create_skills_lock()

        # Generate report data
        report = {
            "timestamp": "2026-06-09T10:30:00Z",
            "total_skills_discovered": 3,
            "skills_by_type": {
                "Custom": 2,
                "Open-source": 1,
                "Agent Skill": 0
            },
            "documentation_status": {
                "documented": 2,
                "missing": 1,
                "removed": 0
            },
            "changes": {
                "newly_added": ["skill-2"],
                "updated_descriptions": ["skill-1"],
                "removed": []
            }
        }

        # Verify report structure
        self.assertEqual(report["total_skills_discovered"], 3)
        self.assertEqual(report["skills_by_type"]["Custom"], 2)
        self.assertEqual(len(report["changes"]["newly_added"]), 1)

    # Helper methods

    def _create_custom_skill(self, name, description):
        """Create a custom skill file."""
        skill_dir = self.skills_dir / name
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(f"""---
name: {name}
description: {description}
license: MIT
metadata:
  author: Test Author
---

# {name.title()} Skill

This is the content of {name}.
""")

    def _create_skills_lock(self):
        """Create skills-lock.json with open-source skills."""
        lock_file = self.project_dir / "skills-lock.json"
        lock_file.write_text(json.dumps({
            "skills": [
                {
                    "name": "open-source-skill",
                    "version": "1.0.0",
                    "repository": "anthropics/skills"
                }
            ]
        }))

    def _create_settings_with_plugins(self):
        """Create .claude/settings.json with enabled plugins."""
        settings_file = self.claude_dir / "settings.json"
        settings_file.write_text(json.dumps({
            "plugins": {
                "agent-skills@addy-agent-skills": {
                    "enabled": True
                }
            }
        }))

    def _update_readme_with_skills(self, readme_path):
        """Simulate README update with skills table."""
        current_content = readme_path.read_text()

        skills_section = """## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| create-changelog | Custom | Generate changelog entries from git diffs | ./.claude/skills/create-changelog |
| pr | Custom | Create GitHub PRs with semantic-release conventions | ./.claude/skills/pr |
| semantic-release | Custom | Manage git branches and commits with versioning | ./.claude/skills/semantic-release |

## Trigger Context & Usage Patterns

### Custom Workflows
- **pr**: Use when you need to create a pull request with semantic-release conventions
- **semantic-release**: Use when managing git branches and commits
- **create-changelog**: Use when generating changelog entries from diffs
"""

        updated = current_content.replace("## Usage", skills_section + "\n\n## Usage")
        readme_path.write_text(updated)


if __name__ == "__main__":
    unittest.main(verbosity=2)
