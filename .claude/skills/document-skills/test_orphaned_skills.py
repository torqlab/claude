#!/usr/bin/env python3
"""
Test suite for orphaned skill detection and removal in document-skills skill.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
import os

# Add scripts directory to path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from align_skills import SkillAligner


class TestOrphanedSkillDetection(unittest.TestCase):
    """Test detection of non-existing skills in documentation."""

    def setUp(self):
        """Create temporary project structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.claude_dir = self.temp_path / ".claude"
        self.skills_dir = self.claude_dir / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_custom_skill(self, skill_name: str, skill_dir=None):
        """Helper to create a custom skill file."""
        if skill_dir is None:
            skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(f"""---
name: {skill_name}
description: Test skill {skill_name}
---

# {skill_name} Skill
""")
        return skill_md

    def test_detects_orphaned_skill_in_readme_table(self):
        """Test detection of skill in README but not in filesystem."""
        # Create README with orphaned skill reference
        readme = self.temp_path / "README.md"
        readme.write_text("""# Project

## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| **create-changelog** | Custom | Generate changelog | ./.claude/skills/create-changelog |
| **pr-open** | Custom | Create PR | ./.claude/skills/pr-open |
""")

        # Create only pr-open skill on filesystem
        self._create_custom_skill("pr-open")

        # Run aligner
        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        # Verify detection
        self.assertIn("create-changelog", orphaned)
        self.assertNotIn("pr-open", orphaned)
        self.assertEqual(len(orphaned), 1)

    def test_detects_multiple_orphaned_skills(self):
        """Test detection of multiple orphaned skills."""
        readme = self.temp_path / "README.md"
        readme.write_text("""## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| **old-tool** | Custom | Old tool | path |
| **deprecated-helper** | Custom | Deprecated | path |
| **removed-workflow** | Custom | Removed | path |
| **pr-open** | Custom | Real skill | path |
""")

        # Create only one real skill
        self._create_custom_skill("pr-open")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        self.assertEqual(len(orphaned), 3)
        self.assertIn("old-tool", orphaned)
        self.assertIn("deprecated-helper", orphaned)
        self.assertIn("removed-workflow", orphaned)

    def test_detects_orphaned_skill_in_agents_md(self):
        """Test detection of orphaned skill in AGENTS.md."""
        agents_md = self.temp_path / "AGENTS.md"
        agents_md.write_text("""## 🛠️ Custom Skills Integration Guide

| Skill | Integration Point | Works With Agents | Sequence |
|-------|-------------------|------------------|----------|
| **create-changelog** | After /build | /build, /ship | /build → /create-changelog → /ship |
| **pr-open** | After review | /review | /review → /pr-open |
""")

        # Create only pr-open skill
        self._create_custom_skill("pr-open")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        self.assertIn("create-changelog", orphaned)
        self.assertNotIn("pr-open", orphaned)


class TestOrphanedSkillRemoval(unittest.TestCase):
    """Test removal of orphaned skills from documentation."""

    def setUp(self):
        """Create temporary project structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.claude_dir = self.temp_path / ".claude"
        self.skills_dir = self.claude_dir / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_custom_skill(self, skill_name: str):
        """Helper to create a custom skill file."""
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(f"""---
name: {skill_name}
description: Test skill {skill_name}
---

# {skill_name} Skill
""")

    def test_removes_orphaned_skill_from_readme_table(self):
        """Test removal of orphaned skill from README skills table."""
        readme = self.temp_path / "README.md"
        readme.write_text("""# Project

## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| **create-changelog** | Custom | Generate changelog | ./.claude/skills/create-changelog |
| **pr-open** | Custom | Create PR | ./.claude/skills/pr-open |

## Other Section

Content here
""")

        self._create_custom_skill("pr-open")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        # Remove orphaned skills
        cleaned = aligner.remove_orphaned_skills_from_readme(orphaned)

        # Verify removal
        updated_readme = readme.read_text()
        self.assertNotIn("create-changelog", updated_readme)
        self.assertIn("pr-open", updated_readme)
        self.assertIn("## Other Section", updated_readme)
        self.assertTrue(len(cleaned) > 0)

    def test_removes_orphaned_skill_from_directory_listing(self):
        """Test removal of orphaned skill from directory structure in README."""
        readme = self.temp_path / "README.md"
        readme.write_text("""## Directory Structure

├── .claude/
│   ├── skills/
│   │   ├── create-changelog/
│   │   ├── pr-open/
│   │   └── github-mcp-setup/
""")

        self._create_custom_skill("pr-open")
        self._create_custom_skill("github-mcp-setup")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        cleaned = aligner.remove_orphaned_skills_from_readme(orphaned)

        updated_readme = readme.read_text()
        self.assertNotIn("create-changelog/", updated_readme)
        self.assertIn("pr-open/", updated_readme)
        self.assertIn("github-mcp-setup/", updated_readme)

    def test_removes_orphaned_skill_from_trigger_context(self):
        """Test removal of orphaned skill from trigger context section."""
        readme = self.temp_path / "README.md"
        readme.write_text("""## Trigger Context & Usage Patterns

### Custom Workflows
- **create-changelog**: Use when generating changelog
- **pr-open**: Use when creating pull requests
""")

        self._create_custom_skill("pr-open")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        cleaned = aligner.remove_orphaned_skills_from_readme(orphaned)

        updated_readme = readme.read_text()
        self.assertNotIn("create-changelog", updated_readme)
        self.assertIn("pr-open", updated_readme)

    def test_removes_orphaned_skill_from_agents_md(self):
        """Test removal of orphaned skill from AGENTS.md custom skills section."""
        agents_md = self.temp_path / "AGENTS.md"
        agents_md.write_text("""## 🛠️ Custom Skills Integration Guide

| Skill | Integration Point | Works With Agents | Sequence |
|-------|-------------------|------------------|----------|
| **create-changelog** | After /build | /build, /ship | /build → /create-changelog → /ship |
| **pr-open** | After review | /review | /review → /pr-open |
""")

        self._create_custom_skill("pr-open")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        cleaned = aligner.remove_orphaned_skills_from_agents_md(orphaned)

        updated_agents = agents_md.read_text()
        self.assertNotIn("create-changelog", updated_agents)
        self.assertIn("pr-open", updated_agents)

    def test_comprehensive_cleanup_multiple_files(self):
        """Test comprehensive cleanup across README and AGENTS.md."""
        readme = self.temp_path / "README.md"
        readme.write_text("""## 📦 Skills

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| **old-tool** | Custom | Old | path |
| **pr-open** | Custom | Real | path |
""")

        agents_md = self.temp_path / "AGENTS.md"
        agents_md.write_text("""## 🛠️ Custom Skills Integration

| Skill | Integration Point |
|-------|-------------------|
| **old-tool** | Some point |
| **pr-open** | After review |
""")

        self._create_custom_skill("pr-open")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        orphaned = aligner.find_orphaned_skills()

        readme_cleaned = aligner.remove_orphaned_skills_from_readme(orphaned)
        agents_cleaned = aligner.remove_orphaned_skills_from_agents_md(orphaned)

        # Verify both files updated
        self.assertTrue(len(readme_cleaned) > 0)
        self.assertTrue(len(agents_cleaned) > 0)

        updated_readme = readme.read_text()
        updated_agents = agents_md.read_text()

        # Verify orphaned skill removed from both
        self.assertNotIn("old-tool", updated_readme)
        self.assertNotIn("old-tool", updated_agents)

        # Verify real skill preserved in both
        self.assertIn("pr-open", updated_readme)
        self.assertIn("pr-open", updated_agents)


class TestSkillDiscoveryWithExistenceVerification(unittest.TestCase):
    """Test that discovered skills are verified to exist."""

    def setUp(self):
        """Create temporary project structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.claude_dir = self.temp_path / ".claude"
        self.skills_dir = self.claude_dir / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_only_discovers_skills_with_existing_skill_md(self):
        """Test that skill discovery verifies SKILL.md exists."""
        # Create skill directory but NO SKILL.md file
        orphan_dir = self.skills_dir / "orphan-skill"
        orphan_dir.mkdir()

        # Create valid skill with SKILL.md
        valid_dir = self.skills_dir / "valid-skill"
        valid_dir.mkdir()
        (valid_dir / "SKILL.md").write_text("---\nname: valid-skill\n---")

        aligner = SkillAligner(self.temp_path)
        discovered = aligner.discover_skills()

        # Verify only valid skill is discovered
        self.assertIn("valid-skill", discovered)
        self.assertNotIn("orphan-skill", discovered)

    def test_reports_malformed_skill_md(self):
        """Test handling of malformed SKILL.md files."""
        skill_dir = self.skills_dir / "bad-skill"
        skill_dir.mkdir()
        # Write malformed YAML
        (skill_dir / "SKILL.md").write_text("---\nbad: yaml: {broken")

        aligner = SkillAligner(self.temp_path)
        # Should not raise, just skip the skill
        discovered = aligner.discover_skills()
        self.assertNotIn("bad-skill", discovered)


class TestReportGeneration(unittest.TestCase):
    """Test report generation for cleanup operations."""

    def setUp(self):
        """Create temporary project structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.claude_dir = self.temp_path / ".claude"
        self.skills_dir = self.claude_dir / "skills"
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_report_includes_orphaned_count(self):
        """Test that report includes count of orphaned skills."""
        readme = self.temp_path / "README.md"
        readme.write_text("""| Skill | Type |
|-------|------|
| **old1** | Custom |
| **old2** | Custom |
""")

        (self.skills_dir / "real-skill").mkdir()
        (self.skills_dir / "real-skill" / "SKILL.md").write_text("---\nname: real-skill\n---")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        report = aligner.generate_report()

        self.assertEqual(report["orphaned_count"], 2)
        self.assertIn("old1", report["orphaned_skills"])
        self.assertIn("old2", report["orphaned_skills"])

    def test_report_indicates_clean_documentation(self):
        """Test that report indicates when documentation is clean."""
        readme = self.temp_path / "README.md"
        readme.write_text("""| Skill | Type |
|-------|------|
| **real-skill** | Custom |
""")

        (self.skills_dir / "real-skill").mkdir()
        (self.skills_dir / "real-skill" / "SKILL.md").write_text("---\nname: real-skill\n---")

        aligner = SkillAligner(self.temp_path)
        aligner.discover_skills()
        aligner.extract_documented_skills()
        report = aligner.generate_report()

        self.assertEqual(report["orphaned_count"], 0)
        self.assertTrue(report["documentation_clean"])


if __name__ == "__main__":
    unittest.main()
