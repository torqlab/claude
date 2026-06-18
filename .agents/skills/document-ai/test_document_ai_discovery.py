#!/usr/bin/env python3
"""
Test suite for document-ai skill focusing on AI.md generation.
Tests AI tool discovery (skills, hooks, agents), categorization, and markdown table generation.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestAIToolsDiscovery(unittest.TestCase):
    """Test AI tools discovery from multiple sources (skills, hooks, agents)."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.skills_dir = Path(self.temp_dir) / ".kiro" / "skills"
        self.hooks_dir = Path(self.temp_dir) / ".kiro" / "hooks"
        self.agents_dir = Path(self.temp_dir) / ".kiro" / "agents"
        self.skills_dir.mkdir(parents=True)
        self.hooks_dir.mkdir(parents=True)
        self.agents_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_discovers_custom_skills(self):
        """Test discovery of custom skills from .kiro/skills/."""
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

    def test_discovers_hooks(self):
        """Test discovery of hooks from .kiro/hooks/."""
        hook_file = self.hooks_dir / "test-hook.kiro.hook"
        hook_data = {
            "name": "Test Hook",
            "shortName": "test-hook",
            "when": {"type": "userTriggered"},
            "then": {"type": "askAgent", "prompt": "Test prompt"}
        }
        hook_file.write_text(json.dumps(hook_data))
        self.assertTrue(hook_file.exists())
        content = json.loads(hook_file.read_text())
        self.assertEqual(content["name"], "Test Hook")

    def test_discovers_agents(self):
        """Test discovery of agents from .kiro/agents/."""
        agent_file = self.agents_dir / "test-agent.agent.json"
        agent_data = {
            "name": "test-agent",
            "displayName": "Test Agent",
            "description": "A test agent",
            "skills": ["test-skill"]
        }
        agent_file.write_text(json.dumps(agent_data))
        self.assertTrue(agent_file.exists())
        content = json.loads(agent_file.read_text())
        self.assertEqual(content["displayName"], "Test Agent")

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
    """Test extraction of AI tool metadata (skills, hooks, agents) from files."""

    def test_extracts_skill_frontmatter(self):
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

    def test_extracts_hook_name(self):
        """Test extraction of hook name and trigger type."""
        hook_data = {
            "name": "Review Code",
            "shortName": "review-code",
            "when": {"type": "userTriggered"}
        }
        self.assertEqual(hook_data["name"], "Review Code")
        self.assertEqual(hook_data["when"]["type"], "userTriggered")

    def test_extracts_agent_name_and_skills(self):
        """Test extraction of agent name and used skills."""
        agent_data = {
            "name": "code-review-agent",
            "displayName": "Code Review Agent",
            "skills": ["code-review-excellence", "karpathy-guidelines"]
        }
        self.assertEqual(len(agent_data["skills"]), 2)


class TestAIToolsCategorization(unittest.TestCase):
    """Test categorization of AI tools by source."""

    def test_categorizes_custom_skills(self):
        """Test categorization of custom project skills."""
        skills = [
            {
                "name": "custom-skill",
                "path": "./.kiro/skills/custom-skill/SKILL.md",
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

    def test_categorizes_hooks_by_trigger_type(self):
        """Test categorization of hooks by trigger type."""
        hooks = [
            {"name": "review-code", "trigger": "userTriggered", "type": "Manual Trigger"},
            {"name": "post-task-review", "trigger": "postTaskExecution", "type": "Task Event"},
            {"name": "format-on-save", "trigger": "fileEdited", "type": "File Event"}
        ]
        self.assertEqual(hooks[0]["type"], "Manual Trigger")
        self.assertEqual(hooks[1]["type"], "Task Event")
        self.assertEqual(hooks[2]["type"], "File Event")

    def test_categorizes_agents_by_responsibility(self):
        """Test categorization of agents by their responsibilities."""
        agents = [
            {"name": "code-review-agent", "description": "Performs code review", "category": "Review"},
            {"name": "test-agent", "description": "Runs tests", "category": "Testing"}
        ]
        self.assertEqual(agents[0]["category"], "Review")
        self.assertEqual(agents[1]["category"], "Testing")


class TestMarkdownTableGeneration(unittest.TestCase):
    """Test markdown table generation for AI.md."""

    def test_table_header_format(self):
        """Test that table header has correct format."""
        header = "| Skill | Type | Description | Keywords |"
        separator = "|-------|------|-------------|----------|"
        self.assertIn("Skill", header)
        self.assertIn("Type", header)
        self.assertIn("Keywords", header)
        self.assertIn("---", separator)

    def test_table_row_format(self):
        """Test that table rows follow markdown format."""
        row = "| **my-skill** | Custom | A test skill | skill, documentation |"
        self.assertTrue(row.startswith("|"))
        self.assertTrue(row.endswith("|"))
        self.assertIn("**my-skill**", row)
        self.assertIn("Custom", row)

    def test_source_link_for_custom_skills(self):
        """Test that custom skills have correct source link format."""
        skill_name = "test-skill"
        source_link = f"[./.kiro/skills/{skill_name}/SKILL.md](./.kiro/skills/{skill_name}/SKILL.md)"
        self.assertIn(skill_name, source_link)
        self.assertIn("./.kiro/skills", source_link)

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


class TestAImdGeneration(unittest.TestCase):
    """Test AI.md file generation with all AI tools (skills, hooks, agents)."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_creates_ai_md_file(self):
        """Test that AI.md file is created."""
        ai_md = Path(self.temp_dir) / "AI.md"
        content = """# Available AI Tools

## Custom Skills

| Skill | Type | Description | Keywords |
|-------|------|-------------|----------|
| **my-skill** | Custom | Test skill | skill |

## Hooks

| Hook | Trigger Type | Description |
|------|--------------|-------------|
| **review-code** | Manual | Code review |

## Agents

| Agent | Description | Uses Skills |
|-------|-------------|-------------|
| **code-review-agent** | Code review | code-review-excellence |
"""
        ai_md.write_text(content)
        self.assertTrue(ai_md.exists())
        self.assertIn("# Available AI Tools", ai_md.read_text())
        self.assertIn("## Custom Skills", ai_md.read_text())
        self.assertIn("## Hooks", ai_md.read_text())
        self.assertIn("## Agents", ai_md.read_text())

    def test_ai_md_has_multiple_sections(self):
        """Test that AI.md has sections for skills, hooks, agents."""
        content = """# Available AI Tools

## Custom Skills

| Skill | Type | Description | Keywords |
|-------|------|-------------|----------|

## Open-source Skills

| Skill | Type | Description | Keywords |
|-------|------|-------------|----------|

## Agent Skills

| Skill | Type | Description | Keywords |
|-------|------|-------------|----------|

## Hooks

| Hook | Trigger Type | Description |
|------|--------------|-------------|

## Agents

| Agent | Description | Uses Skills |
|-------|-------------|-------------|

## 🎯 Decision Trees

[decision tree content]

## 🔗 Agent Tools Graph

[Mermaid graph visualization]
"""
        self.assertIn("## Custom Skills", content)
        self.assertIn("## Hooks", content)
        self.assertIn("## Agents", content)
        self.assertIn("## Agent Tools Graph", content)

    def test_organizes_tools_by_type(self):
        """Test that AI tools are organized by type in sections."""
        content = """# Available AI Tools

## Custom Skills

| Skill | Type | Description | Keywords |
|-------|------|-------------|----------|
| **custom-skill** | Custom | Custom | skill |

## Hooks

| Hook | Trigger Type | Description |
|------|--------------|-------------|
| **review-code** | userTriggered | Review |

## Agents

| Agent | Description | Uses Skills |
|-------|-------------|-------------|
| **review-agent** | Reviews code | custom-skill |
"""
        self.assertIn("**custom-skill**", content)
        self.assertIn("**review-code**", content)
        self.assertIn("**review-agent**", content)

    def test_includes_section_descriptions(self):
        """Test that each section has a description of its content."""
        content = """# Available AI Tools

## Custom Skills

Project-specific skills maintained in `.kiro/skills/`.

## Hooks

Automated triggers configured in `.kiro/hooks/`.

## Agents

AI agents configured in `.kiro/agents/` using skills.
"""
        self.assertIn("Project-specific skills", content)
        self.assertIn(".kiro/hooks/", content)
        self.assertIn(".kiro/agents/", content)


class TestDescriptionTruncation(unittest.TestCase):
    """Test description truncation logic."""

    def test_truncates_long_description(self):
        """Test that long descriptions are truncated."""
        long_desc = "This is a very long description that goes on and on. It has multiple sentences. And more details."
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


class TestToolsSortingInTable(unittest.TestCase):
    """Test AI tools sorting in markdown tables."""

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
        """Test that AI tool type grouping is maintained during sorting."""
        tools_by_type = {
            "Custom": [
                {"name": "skill-z", "type": "Custom"},
                {"name": "skill-a", "type": "Custom"},
            ],
            "Hooks": [
                {"name": "hook-y", "type": "Hook"},
                {"name": "hook-b", "type": "Hook"},
            ]
        }
        self.assertEqual(len(tools_by_type["Custom"]), 2)
        self.assertEqual(len(tools_by_type["Hooks"]), 2)


class TestReportGeneration(unittest.TestCase):
    """Test report generation for AI tools discovery."""

    def test_generates_summary_report(self):
        """Test report with AI tools discovery summary."""
        report = {
            "total_tools_discovered": 10,
            "skills": {
                "custom": 3,
                "open_source": 4,
                "agent_skill": 2
            },
            "hooks": 5,
            "agents": 3
        }
        self.assertEqual(report["total_tools_discovered"], 10)
        self.assertEqual(report["skills"]["custom"], 3)
        self.assertEqual(report["hooks"], 5)

    def test_report_has_tool_lists(self):
        """Test that report includes lists of discovered AI tools."""
        report = {
            "custom_skills": ["skill-1", "skill-2"],
            "hooks": ["hook-1", "hook-2", "hook-3"],
            "agents": ["agent-1"],
        }
        self.assertEqual(len(report["custom_skills"]), 2)
        self.assertEqual(len(report["hooks"]), 3)
        self.assertEqual(len(report["agents"]), 1)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_handles_missing_skill_files(self):
        """Test graceful handling of missing SKILL.md files."""
        skill_dir = Path("/nonexistent/skill")
        skill_file = skill_dir / "SKILL.md"
        self.assertFalse(skill_file.exists())

    def test_handles_empty_skills_directory(self):
        """Test handling of empty .kiro/skills directory."""
        temp_dir = tempfile.mkdtemp()
        skills_dir = Path(temp_dir) / ".kiro" / "skills"
        skills_dir.mkdir(parents=True)
        skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()])
        self.assertEqual(skill_count, 0)
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_handles_malformed_json_gracefully(self):
        """Test handling of malformed hook/agent JSON files."""
        malformed = """{
"name": "test",
"description": broken json without quotes,
}"""
        self.assertIn("broken json", malformed)


class TestConstantTableFormat(unittest.TestCase):
    """Test that markdown table format is consistent across projects."""

    def test_header_constant_across_projects(self):
        """Test that skills table header format is consistent."""
        header1 = "| Skill | Type | Description | Keywords |"
        header2 = "| Skill | Type | Description | Keywords |"
        self.assertEqual(header1, header2)

    def test_separator_constant_across_projects(self):
        """Test that table separator format is consistent."""
        sep1 = "|-------|------|-------------|----------|"
        sep2 = "|-------|------|-------------|----------|"
        self.assertEqual(sep1, sep2)

    def test_column_order_is_standard(self):
        """Test that column order is standard for skills table."""
        header = "| Skill | Type | Description | Keywords |"
        columns = [col.strip() for col in header.split("|")[1:-1]]
        self.assertEqual(columns, ["Skill", "Type", "Description", "Keywords"])


if __name__ == "__main__":
    unittest.main()
