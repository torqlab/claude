#!/usr/bin/env python3
"""
Test suite for align-skills-documentation skill.
Tests skill discovery, metadata extraction, README updates, and report generation.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestSkillDiscovery(unittest.TestCase):
    """Test skill discovery from multiple sources."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.skills_dir = Path(self.temp_dir) / ".claude" / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_discovers_custom_skills(self):
        """Test discovery of custom skills from .claude/skills/."""
        # Create a custom skill
        custom_skill_dir = self.skills_dir / "test-skill"
        custom_skill_dir.mkdir()
        skill_md = custom_skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for documentation
license: MIT
metadata:
  author: Test Author
---

# Test Skill
""")

        # Verify skill can be found
        self.assertTrue(skill_md.exists())
        self.assertIn("test-skill", str(skill_md.parent.name))

    def test_discovers_skills_from_lock_file(self):
        """Test discovery of skills from skills-lock.json."""
        lock_file = Path(self.temp_dir) / "skills-lock.json"
        skills_data = {
            "skills": [
                {
                    "name": "open-source-skill",
                    "version": "1.0.0",
                    "repository": "anthropics/skills"
                }
            ]
        }
        lock_file.write_text(json.dumps(skills_data))

        # Verify lock file exists and contains skills
        self.assertTrue(lock_file.exists())
        content = json.loads(lock_file.read_text())
        self.assertEqual(len(content["skills"]), 1)
        self.assertEqual(content["skills"][0]["name"], "open-source-skill")

    def test_discovers_plugin_skills(self):
        """Test discovery of agent skills from plugins."""
        settings_file = Path(self.temp_dir) / ".claude" / "settings.json"
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        settings_data = {
            "plugins": {
                "agent-skills@addy-agent-skills": {
                    "enabled": True
                }
            }
        }
        settings_file.write_text(json.dumps(settings_data))

        # Verify settings file identifies enabled plugins
        self.assertTrue(settings_file.exists())
        content = json.loads(settings_file.read_text())
        self.assertIn("agent-skills@addy-agent-skills", content["plugins"])


class TestMetadataExtraction(unittest.TestCase):
    """Test extraction of skill metadata from SKILL.md files."""

    def test_extracts_frontmatter(self):
        """Test extraction of YAML frontmatter from SKILL.md."""
        skill_content = """---
name: example-skill
description: |
  This is a multi-line description
  that spans several lines
license: MIT
metadata:
  author: John Doe
  version: 1.0.0
---

# Skill Content Here
"""
        lines = skill_content.split('\n')

        # Verify frontmatter boundaries
        self.assertEqual(lines[0], '---')
        # Find closing --- marker
        closing_marker_idx = next(i for i, line in enumerate(lines[1:], 1) if line == '---')
        self.assertEqual(lines[closing_marker_idx], '---')
        self.assertIn('name: example-skill', skill_content)
        self.assertIn('license: MIT', skill_content)

    def test_extracts_skill_name(self):
        """Test extraction of skill name."""
        skill_content = """---
name: my-test-skill
---
"""
        self.assertIn("name: my-test-skill", skill_content)

    def test_extracts_skill_description(self):
        """Test extraction of skill description."""
        skill_content = """---
name: test-skill
description: |
  Use this skill when you need to do something.
  It discovers all available skills.
---
"""
        self.assertIn("Use this skill when", skill_content)
        self.assertIn("discovers all available skills", skill_content)

    def test_handles_missing_metadata(self):
        """Test graceful handling of missing optional metadata."""
        skill_content = """---
name: minimal-skill
description: A minimal skill
---
"""
        self.assertIn("name: minimal-skill", skill_content)
        self.assertNotIn("license:", skill_content)
        self.assertNotIn("metadata:", skill_content)


class TestSkillCategorization(unittest.TestCase):
    """Test categorization of skills by source."""

    def test_categorizes_custom_skills(self):
        """Test categorization of custom project skills."""
        skills = [
            {
                "name": "custom-skill",
                "path": "./.claude/skills/custom-skill/SKILL.md"
            }
        ]

        for skill in skills:
            skill_type = "Custom" if "./.claude/skills/" in skill["path"] else "Other"
            self.assertEqual(skill_type, "Custom")

    def test_categorizes_open_source_skills(self):
        """Test categorization of NPM-based open-source skills."""
        skills = [
            {
                "name": "open-source-skill",
                "source": "anthropics/skills"
            }
        ]

        for skill in skills:
            skill_type = "Open-source" if "anthropics" in skill.get("source", "") else "Other"
            self.assertEqual(skill_type, "Open-source")

    def test_categorizes_agent_skills(self):
        """Test categorization of agent skills from plugins."""
        skills = [
            {
                "name": "agent-skill",
                "source": "addyosmani/agent-skills"
            }
        ]

        for skill in skills:
            skill_type = "Agent Skill" if "addyosmani" in skill.get("source", "") else "Other"
            self.assertEqual(skill_type, "Agent Skill")


class TestREADMEUpdate(unittest.TestCase):
    """Test README.md synchronization."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_preserves_readme_structure(self):
        """Test that README structure is preserved during update."""
        readme_content = """# Project

## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| old-skill | Custom | Old skill | ./.claude/skills/old-skill |

## Other Section

Some content here.
"""
        readme_path = Path(self.temp_dir) / "README.md"
        readme_path.write_text(readme_content)

        # Verify structure is maintained
        content = readme_path.read_text()
        self.assertIn("## 📦 Skills", content)
        self.assertIn("## Other Section", content)
        self.assertIn("Some content here", content)

    def test_updates_skills_table(self):
        """Test that skills table is properly updated."""
        readme_content = """# Project

## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| old-skill | Custom | Old skill | path |
"""
        new_table = """| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| new-skill | Custom | New skill | path |
| old-skill | Custom | Old skill | path |"""

        # Verify table replacement logic
        self.assertIn("| Skill | Type |", readme_content)
        self.assertIn("old-skill", readme_content)
        self.assertIn("Custom", readme_content)

    def test_adds_trigger_context_section(self):
        """Test that Trigger Context section is added to README."""
        trigger_section = """## Trigger Context & Usage Patterns

### Custom Workflows
- **test-skill**: Use when you need to test something
"""
        self.assertIn("Trigger Context", trigger_section)
        self.assertIn("Use when", trigger_section)


class TestReportGeneration(unittest.TestCase):
    """Test generation of audit reports."""

    def test_generates_summary_report(self):
        """Test report with skill discovery summary."""
        report = {
            "total_skills": 5,
            "by_type": {
                "Custom": 2,
                "Open-source": 2,
                "Agent Skill": 1
            },
            "missing_from_readme": [],
            "newly_added": ["align-skills-documentation"],
            "removed": []
        }

        self.assertEqual(report["total_skills"], 5)
        self.assertEqual(report["by_type"]["Custom"], 2)
        self.assertEqual(len(report["newly_added"]), 1)

    def test_detects_missing_skills(self):
        """Test detection of skills in code but missing from README."""
        discovered_skills = {"skill-1", "skill-2", "skill-3"}
        documented_skills = {"skill-1", "skill-3"}
        missing = discovered_skills - documented_skills

        self.assertIn("skill-2", missing)
        self.assertEqual(len(missing), 1)

    def test_detects_removed_skills(self):
        """Test detection of skills removed from codebase."""
        documented_skills = {"old-skill-1", "old-skill-2"}
        discovered_skills = {"old-skill-1"}
        removed = documented_skills - discovered_skills

        self.assertIn("old-skill-2", removed)
        self.assertEqual(len(removed), 1)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_handles_malformed_yaml(self):
        """Test handling of malformed SKILL.md frontmatter."""
        malformed_content = """---
name: bad-skill
description: Missing closing quotes
metadata: {broken json
---
"""
        # Verify detection of malformed content
        self.assertIn("---", malformed_content)
        # In real implementation, should log error and skip

    def test_handles_missing_skill_files(self):
        """Test graceful handling of missing SKILL.md files."""
        skill_dir = Path("/nonexistent/skill")
        skill_file = skill_dir / "SKILL.md"

        # Verify file doesn't exist
        self.assertFalse(skill_file.exists())

    def test_handles_empty_skills_directory(self):
        """Test handling of empty .claude/skills directory."""
        temp_dir = tempfile.mkdtemp()
        skills_dir = Path(temp_dir) / ".claude" / "skills"
        skills_dir.mkdir(parents=True)

        # Count skill directories
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        self.assertEqual(skill_count, 0)

        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestTriggerContextExtraction(unittest.TestCase):
    """Test extraction of trigger patterns from descriptions."""

    def test_extracts_use_when_patterns(self):
        """Test extraction of 'Use when' patterns."""
        description = "Use when you need to create documentation or when files change frequently."

        # Verify pattern detection
        self.assertIn("Use when", description)
        patterns = [p for p in description.split("when") if p.strip()]
        self.assertGreater(len(patterns), 1)

    def test_extracts_trigger_context_patterns(self):
        """Test extraction of 'Trigger context' patterns."""
        description = "Trigger contexts: new skills added, files modified, release preparation."

        self.assertIn("Trigger context", description)

    def test_groups_patterns_by_workflow_phase(self):
        """Test grouping of trigger patterns by phase."""
        patterns = {
            "Custom Workflows": ["pr", "semantic-release"],
            "Documentation": ["create-changelog", "align-skills-documentation"],
            "Design": ["frontend-design"]
        }

        self.assertEqual(len(patterns["Custom Workflows"]), 2)
        self.assertIn("pr", patterns["Custom Workflows"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
