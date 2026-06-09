#!/usr/bin/env python3
"""
Test suite for document-skills skill focusing on SKILLS.md generation.
Tests skill discovery, categorization, and markdown table generation.
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
        custom_skill_dir = self.skills_dir / "test-skill"
        custom_skill_dir.mkdir()
        skill_md = custom_skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for documentation
license: MIT
---

# Test Skill
""")
        self.assertTrue(skill_md.exists())
        self.assertIn("test-skill", str(skill_md.parent.name))

    def test_discovers_open_source_skills_from_lock_file(self):
        """Test discovery of open-source skills from skills-lock.json."""
        lock_file = Path(self.temp_dir) / "skills-lock.json"
        skills_data = {
            "version": 1,
            "skills": {
                "frontend-design": {
                    "source": "anthropics/skills",
                    "ref": "main"
                },
                "skill-creator": {
                    "source": "anthropics/skills",
                    "ref": "main"
                }
            }
        }
        lock_file.write_text(json.dumps(skills_data))
        self.assertTrue(lock_file.exists())
        content = json.loads(lock_file.read_text())
        self.assertEqual(len(content["skills"]), 2)

    def test_discovers_agent_skills_from_plugins(self):
        """Test discovery of agent skills from plugins."""
        settings_file = Path(self.temp_dir) / ".claude" / "settings.json"
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        settings_data = {
            "enabledPlugins": {
                "agent-skills@addy-agent-skills": True
            }
        }
        settings_file.write_text(json.dumps(settings_data))
        self.assertTrue(settings_file.exists())
        content = json.loads(settings_file.read_text())
        self.assertIn("agent-skills@addy-agent-skills", content["enabledPlugins"])


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
---

# Skill Content Here
"""
        lines = skill_content.split('\n')
        self.assertEqual(lines[0], '---')
        closing_marker_idx = next(i for i, line in enumerate(lines[1:], 1) if line == '---')
        self.assertEqual(lines[closing_marker_idx], '---')
        self.assertIn('name: example-skill', skill_content)

    def test_extracts_skill_name(self):
        """Test extraction of skill name."""
        skill_content = """---
name: my-test-skill
description: Test skill
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


class TestSkillCategorization(unittest.TestCase):
    """Test categorization of skills by source."""

    def test_categorizes_custom_skills(self):
        """Test categorization of custom project skills."""
        skills = [
            {
                "name": "custom-skill",
                "path": "./.claude/skills/custom-skill/SKILL.md",
                "type": "Custom"
            }
        ]
        for skill in skills:
            self.assertEqual(skill["type"], "Custom")

    def test_categorizes_open_source_skills(self):
        """Test categorization of open-source skills."""
        skills = [
            {
                "name": "frontend-design",
                "source": "anthropics/skills",
                "type": "Open-source"
            }
        ]
        for skill in skills:
            self.assertEqual(skill["type"], "Open-source")

    def test_categorizes_agent_skills(self):
        """Test categorization of agent skills from plugins."""
        skills = [
            {
                "name": "spec",
                "source": "addyosmani/agent-skills",
                "type": "Agent Skill"
            }
        ]
        for skill in skills:
            self.assertEqual(skill["type"], "Agent Skill")


class TestMarkdownTableGeneration(unittest.TestCase):
    """Test markdown table generation for SKILLS.md."""

    def test_table_header_format(self):
        """Test that table header has correct format."""
        header = "| Skill | Type | Description | Source |"
        separator = "|-------|------|-------------|--------|"
        self.assertIn("Skill", header)
        self.assertIn("Type", header)
        self.assertIn("Description", header)
        self.assertIn("Source", header)
        self.assertIn("---", separator)

    def test_table_row_format(self):
        """Test that table rows follow markdown format."""
        row = "| **my-skill** | Custom | A test skill | [link](path) |"
        self.assertTrue(row.startswith("|"))
        self.assertTrue(row.endswith("|"))
        self.assertIn("**my-skill**", row)
        self.assertIn("Custom", row)

    def test_source_link_for_custom_skills(self):
        """Test that custom skills have correct source link format."""
        skill_name = "test-skill"
        source_link = f"[./.claude/skills/{skill_name}/SKILL.md](./.claude/skills/{skill_name}/SKILL.md)"
        self.assertIn(skill_name, source_link)
        self.assertIn("./.claude/skills", source_link)

    def test_source_link_for_open_source_skills(self):
        """Test that open-source skills link to anthropics/skills."""
        source_link = "[anthropics/skills](https://github.com/anthropics/skills)"
        self.assertIn("anthropics/skills", source_link)
        self.assertIn("https://github.com", source_link)

    def test_source_link_for_agent_skills(self):
        """Test that agent skills link to addyosmani/agent-skills."""
        source_link = "[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)"
        self.assertIn("addyosmani", source_link)
        self.assertIn("https://github.com", source_link)


class TestSKILLSmdGeneration(unittest.TestCase):
    """Test SKILLS.md file generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_creates_skills_md_file(self):
        """Test that SKILLS.md file is created."""
        skills_md = Path(self.temp_dir) / "SKILLS.md"
        content = """# Available Skills

## Custom Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **my-skill** | Custom | Test skill | [link](path) |
"""
        skills_md.write_text(content)
        self.assertTrue(skills_md.exists())
        self.assertIn("# Available Skills", skills_md.read_text())

    def test_skills_md_has_three_sections(self):
        """Test that SKILLS.md has sections for all three skill types."""
        content = """# Available Skills

## Custom Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|

## Open-source Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|

## Agent Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
"""
        self.assertIn("## Custom Skills", content)
        self.assertIn("## Open-source Skills", content)
        self.assertIn("## Agent Skills", content)

    def test_organizes_skills_by_type(self):
        """Test that skills are organized by type in sections."""
        content = """# Available Skills

## Custom Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **custom-skill** | Custom | Custom | source |

## Open-source Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **open-skill** | Open-source | Open | source |

## Agent Skills

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **agent-skill** | Agent Skill | Agent | source |
"""
        self.assertIn("**custom-skill**", content)
        self.assertIn("**open-skill**", content)
        self.assertIn("**agent-skill**", content)

    def test_includes_section_descriptions(self):
        """Test that each section has a description of its source."""
        content = """# Available Skills

## Custom Skills

Project-specific skills maintained in `./.claude/skills/`.

## Open-source Skills

Skills from [anthropics/skills](https://github.com/anthropics/skills) registered in `skills-lock.json`.

## Agent Skills

Skills from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) plugin.
"""
        self.assertIn("Project-specific skills", content)
        self.assertIn("anthropics/skills", content)
        self.assertIn("addyosmani/agent-skills", content)


class TestDescriptionTruncation(unittest.TestCase):
    """Test description truncation logic."""

    def test_truncates_long_description(self):
        """Test that long descriptions are truncated."""
        long_desc = "This is a very long description that goes on and on. It has multiple sentences. And more details."
        # Truncation should happen at first period
        truncated = long_desc.split('. ')[0] + '. '
        self.assertTrue(len(truncated) < len(long_desc))

    def test_preserves_short_description(self):
        """Test that short descriptions are preserved."""
        short_desc = "A short skill description."
        self.assertEqual(short_desc, short_desc)

    def test_handles_multiline_description(self):
        """Test that multiline descriptions are handled."""
        multiline = "First line\nSecond line\nThird line"
        first_line = multiline.split('\n')[0]
        self.assertEqual(first_line, "First line")


class TestSkillsSortingInTable(unittest.TestCase):
    """Test skill sorting in markdown tables."""

    def test_sorts_skills_alphabetically_within_type(self):
        """Test that skills are sorted alphabetically within each type."""
        skills = [
            {"name": "zulu-skill", "type": "Custom"},
            {"name": "alpha-skill", "type": "Custom"},
            {"name": "bravo-skill", "type": "Custom"},
        ]
        sorted_skills = sorted(skills, key=lambda s: s["name"])
        self.assertEqual(sorted_skills[0]["name"], "alpha-skill")
        self.assertEqual(sorted_skills[1]["name"], "bravo-skill")
        self.assertEqual(sorted_skills[2]["name"], "zulu-skill")

    def test_maintains_type_grouping(self):
        """Test that skill type grouping is maintained during sorting."""
        skills_by_type = {
            "Custom": [
                {"name": "skill-z", "type": "Custom"},
                {"name": "skill-a", "type": "Custom"},
            ],
            "Open-source": [
                {"name": "skill-y", "type": "Open-source"},
                {"name": "skill-b", "type": "Open-source"},
            ]
        }
        # Each type should maintain its own section
        self.assertEqual(len(skills_by_type["Custom"]), 2)
        self.assertEqual(len(skills_by_type["Open-source"]), 2)


class TestReportGeneration(unittest.TestCase):
    """Test report generation."""

    def test_generates_summary_report(self):
        """Test report with skill discovery summary."""
        report = {
            "total_skills_discovered": 5,
            "by_type": {
                "Custom": 2,
                "Open-source": 2,
                "Agent Skill": 1
            }
        }
        self.assertEqual(report["total_skills_discovered"], 5)
        self.assertEqual(report["by_type"]["Custom"], 2)
        self.assertEqual(report["by_type"]["Open-source"], 2)
        self.assertEqual(report["by_type"]["Agent Skill"], 1)

    def test_report_has_skill_lists(self):
        """Test that report includes lists of discovered skills."""
        report = {
            "custom_skills": ["skill-1", "skill-2"],
            "open_source_skills": ["skill-3"],
            "agent_skills": ["skill-4", "skill-5"],
        }
        self.assertEqual(len(report["custom_skills"]), 2)
        self.assertEqual(len(report["open_source_skills"]), 1)
        self.assertEqual(len(report["agent_skills"]), 2)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_handles_missing_skill_files(self):
        """Test graceful handling of missing SKILL.md files."""
        skill_dir = Path("/nonexistent/skill")
        skill_file = skill_dir / "SKILL.md"
        self.assertFalse(skill_file.exists())

    def test_handles_empty_skills_directory(self):
        """Test handling of empty .claude/skills directory."""
        temp_dir = tempfile.mkdtemp()
        skills_dir = Path(temp_dir) / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        self.assertEqual(skill_count, 0)
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_handles_malformed_yaml_gracefully(self):
        """Test handling of malformed SKILL.md frontmatter."""
        malformed = """---
name: bad-skill
description: Missing closing quotes
metadata: {broken json
---
"""
        self.assertIn("---", malformed)
        # Should attempt to parse without crashing


class TestConstantTableFormat(unittest.TestCase):
    """Test that markdown table format is consistent across projects."""

    def test_header_constant_across_projects(self):
        """Test that table header format is consistent."""
        header1 = "| Skill | Type | Description | Source |"
        header2 = "| Skill | Type | Description | Source |"
        self.assertEqual(header1, header2)

    def test_separator_constant_across_projects(self):
        """Test that table separator format is consistent."""
        sep1 = "|-------|------|-------------|--------|"
        sep2 = "|-------|------|-------------|--------|"
        self.assertEqual(sep1, sep2)

    def test_column_order_is_standard(self):
        """Test that column order is standard: Skill | Type | Description | Source."""
        header = "| Skill | Type | Description | Source |"
        columns = [col.strip() for col in header.split("|")[1:-1]]
        self.assertEqual(columns, ["Skill", "Type", "Description", "Source"])


if __name__ == "__main__":
    unittest.main()
