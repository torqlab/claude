#!/usr/bin/env python3
"""
Exhaustive test suite for skill classification logic in document-ai skill.

The core rule:
- Open-source skills = skills whose names appear as keys in skills-lock.json
- Custom skills = skills in .kiro/skills/ or .claude/skills/ NOT in skills-lock.json
- Agent skills = skills from enabled plugins in .claude/settings.json

This test suite verifies that the classification is ALWAYS determined by
skills-lock.json presence, never by the existence of local directories.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to path for importing
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from align_skills import AIDocumentationGenerator


class TestOpenSourceClassification(unittest.TestCase):
    """
    Verify that skills-lock.json is the SOLE source of truth for
    open-source classification.
    """

    def setUp(self):
        """Create a temporary project structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.kiro_skills = self.temp_dir / ".kiro" / "skills"
        self.kiro_skills.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_local_skill(self, name: str, description: str = "Test"):
        """Helper: create a local skill directory with SKILL.md."""
        skill_dir = self.kiro_skills / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
        )

    def _create_skills_lock(self, skills_dict: dict):
        """Helper: create skills-lock.json with given skills."""
        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": skills_dict
        }))

    def test_skill_in_lock_file_is_open_source(self):
        """A skill in skills-lock.json MUST be classified as Open-source."""
        self._create_local_skill("karpathy-guidelines", "Coding guidelines")
        self._create_skills_lock({
            "karpathy-guidelines": {
                "source": "forrestchang/andrej-karpathy-skills",
                "sourceType": "github",
                "computedHash": "abc123"
            }
        })

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        # karpathy-guidelines must be in Open-source
        open_source_names = [s["name"] for s in result["Open-source"]]
        custom_names = [s["name"] for s in result["Custom"]]

        self.assertIn("karpathy-guidelines", open_source_names)
        self.assertNotIn("karpathy-guidelines", custom_names)

    def test_skill_with_local_copy_and_lock_entry_is_open_source(self):
        """
        Even if a skill has a local copy in .kiro/skills/, if its name
        is in skills-lock.json, it MUST be classified as Open-source.
        """
        # Create local copies (as if installed from GitHub)
        self._create_local_skill("code-review-excellence", "Code review")
        self._create_local_skill("skill-creator", "Create skills")
        self._create_local_skill("r3f-animation", "R3F animation")

        # All three are in skills-lock.json
        self._create_skills_lock({
            "code-review-excellence": {
                "source": "awesome-skills/code-review-skill",
                "sourceType": "github",
                "computedHash": "hash1"
            },
            "skill-creator": {
                "source": "anthropics/skills",
                "sourceType": "github",
                "computedHash": "hash2"
            },
            "r3f-animation": {
                "source": "EnzeD/r3f-skills",
                "sourceType": "github",
                "computedHash": "hash3"
            }
        })

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source_names = [s["name"] for s in result["Open-source"]]
        custom_names = [s["name"] for s in result["Custom"]]

        # All must be Open-source, NOT custom
        self.assertIn("code-review-excellence", open_source_names)
        self.assertIn("skill-creator", open_source_names)
        self.assertIn("r3f-animation", open_source_names)

        self.assertNotIn("code-review-excellence", custom_names)
        self.assertNotIn("skill-creator", custom_names)
        self.assertNotIn("r3f-animation", custom_names)

    def test_skill_not_in_lock_file_is_custom(self):
        """A skill in .kiro/skills/ but NOT in skills-lock.json is Custom."""
        self._create_local_skill("document-ai", "Documentation skill")
        self._create_local_skill("server-dev", "Dev server")

        # skills-lock.json exists but does NOT contain these skills
        self._create_skills_lock({
            "some-other-skill": {
                "source": "org/repo",
                "sourceType": "github",
                "computedHash": "xyz"
            }
        })

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        custom_names = [s["name"] for s in result["Custom"]]
        open_source_names = [s["name"] for s in result["Open-source"]]

        self.assertIn("document-ai", custom_names)
        self.assertIn("server-dev", custom_names)
        self.assertNotIn("document-ai", open_source_names)
        self.assertNotIn("server-dev", open_source_names)

    def test_mixed_skills_classified_correctly(self):
        """
        Realistic scenario: project has both open-source (installed) and
        custom (project-specific) skills in .kiro/skills/.
        """
        # Open-source skills (have local copies AND are in lock file)
        self._create_local_skill("karpathy-guidelines", "Coding guidelines")
        self._create_local_skill("code-review-excellence", "Code review")
        self._create_local_skill("r3f-fundamentals", "R3F basics")
        self._create_local_skill("threejs-animation", "Three.js animation")

        # Custom skills (local only, NOT in lock file)
        self._create_local_skill("document-ai", "AI documentation")
        self._create_local_skill("align-product-config-validator", "Validator alignment")
        self._create_local_skill("server-dev", "Development server")
        self._create_local_skill("r3f-pbr", "PBR textures - custom")

        # skills-lock.json only lists the open-source ones
        self._create_skills_lock({
            "karpathy-guidelines": {
                "source": "forrestchang/andrej-karpathy-skills",
                "sourceType": "github",
                "computedHash": "h1"
            },
            "code-review-excellence": {
                "source": "awesome-skills/code-review-skill",
                "sourceType": "github",
                "computedHash": "h2"
            },
            "r3f-fundamentals": {
                "source": "EnzeD/r3f-skills",
                "sourceType": "github",
                "computedHash": "h3"
            },
            "threejs-animation": {
                "source": "cloudai-x/threejs-skills",
                "sourceType": "github",
                "computedHash": "h4"
            }
        })

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source_names = sorted([s["name"] for s in result["Open-source"]])
        custom_names = sorted([s["name"] for s in result["Custom"]])

        # Open-source must be exactly the lock file entries
        self.assertEqual(open_source_names, sorted([
            "code-review-excellence",
            "karpathy-guidelines",
            "r3f-fundamentals",
            "threejs-animation"
        ]))

        # Custom must be exactly the non-lock-file entries
        self.assertEqual(custom_names, sorted([
            "align-product-config-validator",
            "document-ai",
            "r3f-pbr",
            "server-dev"
        ]))

    def test_no_skill_appears_in_multiple_categories(self):
        """No skill name should appear in more than one category."""
        self._create_local_skill("shared-skill", "Shared")
        self._create_local_skill("unique-custom", "Unique")

        self._create_skills_lock({
            "shared-skill": {
                "source": "org/repo",
                "sourceType": "github",
                "computedHash": "abc"
            }
        })

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        all_names = []
        for category_skills in result.values():
            all_names.extend([s["name"] for s in category_skills])

        # Check no duplicates
        self.assertEqual(len(all_names), len(set(all_names)),
                         f"Duplicate skill found: {all_names}")

    def test_lock_file_without_local_copy_still_open_source(self):
        """
        A skill in skills-lock.json that has no local directory
        is still classified as Open-source.
        """
        # No local skill directory created
        self._create_skills_lock({
            "remote-only-skill": {
                "source": "org/remote-repo",
                "sourceType": "github",
                "computedHash": "xyz"
            }
        })

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source_names = [s["name"] for s in result["Open-source"]]
        self.assertIn("remote-only-skill", open_source_names)

    def test_empty_lock_file_means_all_local_are_custom(self):
        """If skills-lock.json has no skills, all local skills are Custom."""
        self._create_local_skill("skill-a", "Skill A")
        self._create_local_skill("skill-b", "Skill B")

        self._create_skills_lock({})  # empty skills object

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        custom_names = [s["name"] for s in result["Custom"]]
        open_source_names = [s["name"] for s in result["Open-source"]]

        self.assertIn("skill-a", custom_names)
        self.assertIn("skill-b", custom_names)
        self.assertEqual(len(open_source_names), 0)

    def test_missing_lock_file_means_all_local_are_custom(self):
        """If skills-lock.json doesn't exist, all local skills are Custom."""
        self._create_local_skill("skill-x", "Skill X")
        self._create_local_skill("skill-y", "Skill Y")

        # No skills-lock.json created

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        custom_names = [s["name"] for s in result["Custom"]]
        open_source_names = [s["name"] for s in result["Open-source"]]

        self.assertIn("skill-x", custom_names)
        self.assertIn("skill-y", custom_names)
        self.assertEqual(len(open_source_names), 0)


class TestOpenSourceSourceAttribution(unittest.TestCase):
    """Verify that open-source skills get correct GitHub source links."""

    def setUp(self):
        """Create a temporary project structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.kiro_skills = self.temp_dir / ".kiro" / "skills"
        self.kiro_skills.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_local_skill(self, name: str, description: str = "Test"):
        """Helper: create a local skill directory with SKILL.md."""
        skill_dir = self.kiro_skills / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
        )

    def test_open_source_skill_has_github_source(self):
        """Open-source skills must have their GitHub source from lock file."""
        self._create_local_skill("karpathy-guidelines", "Guidelines")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": {
                "karpathy-guidelines": {
                    "source": "forrestchang/andrej-karpathy-skills",
                    "sourceType": "github",
                    "computedHash": "abc"
                }
            }
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source = result["Open-source"]
        skill = next(s for s in open_source if s["name"] == "karpathy-guidelines")

        self.assertEqual(skill["source"], "forrestchang/andrej-karpathy-skills")
        self.assertEqual(skill["type"], "Open-source")

    def test_custom_skill_has_local_path_source(self):
        """Custom skills must have their local file path as source."""
        self._create_local_skill("my-custom-skill", "My custom skill")

        # No lock file entry for this skill
        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        custom = result["Custom"]
        skill = next(s for s in custom if s["name"] == "my-custom-skill")

        self.assertIn(".kiro/skills/my-custom-skill/SKILL.md", skill["source"])
        self.assertEqual(skill["type"], "Custom")

    def test_multiple_open_source_repos_attributed_correctly(self):
        """Each open-source skill gets its specific repo, not a generic one."""
        self._create_local_skill("r3f-animation", "R3F animation")
        self._create_local_skill("threejs-lighting", "Three.js lighting")
        self._create_local_skill("skill-creator", "Skill creator")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": {
                "r3f-animation": {
                    "source": "EnzeD/r3f-skills",
                    "sourceType": "github",
                    "computedHash": "h1"
                },
                "threejs-lighting": {
                    "source": "cloudai-x/threejs-skills",
                    "sourceType": "github",
                    "computedHash": "h2"
                },
                "skill-creator": {
                    "source": "anthropics/skills",
                    "sourceType": "github",
                    "computedHash": "h3"
                }
            }
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source = {s["name"]: s for s in result["Open-source"]}

        self.assertEqual(open_source["r3f-animation"]["source"], "EnzeD/r3f-skills")
        self.assertEqual(open_source["threejs-lighting"]["source"], "cloudai-x/threejs-skills")
        self.assertEqual(open_source["skill-creator"]["source"], "anthropics/skills")


class TestRealWorldProjectClassification(unittest.TestCase):
    """
    Test with the actual project structure to catch the exact bug reported:
    karpathy-guidelines being classified as Custom when it should be Open-source.
    """

    def setUp(self):
        """Create a project structure mirroring the real project."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.kiro_skills = self.temp_dir / ".kiro" / "skills"
        self.kiro_skills.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_local_skill(self, name: str, description: str = "Test"):
        """Helper: create a local skill directory with SKILL.md."""
        skill_dir = self.kiro_skills / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
        )

    def test_real_project_karpathy_is_open_source(self):
        """
        BUG FIX VERIFICATION: karpathy-guidelines must be Open-source because
        it appears in skills-lock.json with source 'forrestchang/andrej-karpathy-skills'.
        """
        # Create all skills that exist locally in the real project
        all_local_skills = [
            "align-product-config-validator",
            "code-review-excellence",
            "document-ai",
            "karpathy-guidelines",
            "r3f-animation",
            "r3f-contact-shadows",
            "r3f-fundamentals",
            "r3f-geometry",
            "r3f-html",
            "r3f-interaction",
            "r3f-lighting",
            "r3f-loaders",
            "r3f-materials",
            "r3f-pbr",
            "r3f-physics",
            "r3f-postprocessing",
            "r3f-shaders",
            "r3f-textures",
            "server-dev",
            "server-test",
            "skill-creator",
            "threejs-animation",
            "threejs-fundamentals",
            "threejs-geometry",
            "threejs-interaction",
            "threejs-lighting",
            "threejs-loaders",
            "threejs-materials",
            "threejs-postprocessing",
            "threejs-shaders",
            "threejs-textures",
        ]
        for name in all_local_skills:
            self._create_local_skill(name, f"Description for {name}")

        # Create skills-lock.json matching the real project
        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": {
                "code-review-excellence": {
                    "source": "awesome-skills/code-review-skill",
                    "sourceType": "github",
                    "computedHash": "hash1"
                },
                "karpathy-guidelines": {
                    "source": "forrestchang/andrej-karpathy-skills",
                    "sourceType": "github",
                    "computedHash": "hash2"
                },
                "r3f-animation": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-fundamentals": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-geometry": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-interaction": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-lighting": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-loaders": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-materials": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-physics": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-postprocessing": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-shaders": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "r3f-textures": {"source": "EnzeD/r3f-skills", "sourceType": "github", "computedHash": "h"},
                "skill-creator": {
                    "source": "anthropics/skills",
                    "sourceType": "github",
                    "skillPath": "skills/skill-creator/SKILL.md",
                    "computedHash": "hash3"
                },
                "threejs-animation": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-fundamentals": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-geometry": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-interaction": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-lighting": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-loaders": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-materials": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-postprocessing": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-shaders": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
                "threejs-textures": {"source": "cloudai-x/threejs-skills", "sourceType": "github", "computedHash": "h"},
            }
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source_names = sorted([s["name"] for s in result["Open-source"]])
        custom_names = sorted([s["name"] for s in result["Custom"]])

        # CRITICAL: karpathy-guidelines must be Open-source
        self.assertIn("karpathy-guidelines", open_source_names,
                      "BUG: karpathy-guidelines should be Open-source (it's in skills-lock.json)")
        self.assertNotIn("karpathy-guidelines", custom_names,
                         "BUG: karpathy-guidelines should NOT be Custom")

        # CRITICAL: code-review-excellence must be Open-source
        self.assertIn("code-review-excellence", open_source_names,
                      "BUG: code-review-excellence should be Open-source")
        self.assertNotIn("code-review-excellence", custom_names)

        # CRITICAL: skill-creator must be Open-source
        self.assertIn("skill-creator", open_source_names,
                      "BUG: skill-creator should be Open-source")
        self.assertNotIn("skill-creator", custom_names)

        # Custom skills should be ONLY those not in lock file
        expected_custom = sorted([
            "align-product-config-validator",
            "document-ai",
            "r3f-contact-shadows",
            "r3f-html",
            "r3f-pbr",
            "server-dev",
            "server-test",
        ])
        self.assertEqual(custom_names, expected_custom,
                         f"Custom skills mismatch. Got: {custom_names}")

        # Open-source should match lock file keys exactly
        expected_open_source = sorted([
            "code-review-excellence",
            "karpathy-guidelines",
            "r3f-animation",
            "r3f-fundamentals",
            "r3f-geometry",
            "r3f-interaction",
            "r3f-lighting",
            "r3f-loaders",
            "r3f-materials",
            "r3f-physics",
            "r3f-postprocessing",
            "r3f-shaders",
            "r3f-textures",
            "skill-creator",
            "threejs-animation",
            "threejs-fundamentals",
            "threejs-geometry",
            "threejs-interaction",
            "threejs-lighting",
            "threejs-loaders",
            "threejs-materials",
            "threejs-postprocessing",
            "threejs-shaders",
            "threejs-textures",
        ])
        self.assertEqual(open_source_names, expected_open_source,
                         f"Open-source skills mismatch. Got: {open_source_names}")


class TestMarkdownOutputClassification(unittest.TestCase):
    """Verify the generated markdown tables have correct classification."""

    def setUp(self):
        """Create a temporary project structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.kiro_skills = self.temp_dir / ".kiro" / "skills"
        self.kiro_skills.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_local_skill(self, name: str, description: str = "Test"):
        """Helper: create a local skill directory with SKILL.md."""
        skill_dir = self.kiro_skills / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
        )

    def test_open_source_skill_in_open_source_section(self):
        """Open-source skills must appear in '## Open-source Skills' section."""
        self._create_local_skill("karpathy-guidelines", "Guidelines")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": {
                "karpathy-guidelines": {
                    "source": "forrestchang/andrej-karpathy-skills",
                    "sourceType": "github",
                    "computedHash": "abc"
                }
            }
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()
        md_content = gen.generate_skills_md(result)

        # Split by sections
        sections = md_content.split("## ")

        # Find the Open-source Skills section
        open_source_section = next(
            (s for s in sections if s.startswith("Open-source Skills")), None
        )
        self.assertIsNotNone(open_source_section,
                             "Missing '## Open-source Skills' section")
        self.assertIn("karpathy-guidelines", open_source_section)

        # Verify it's NOT in Custom Skills section
        custom_section = next(
            (s for s in sections if s.startswith("Custom Skills")), None
        )
        self.assertIsNotNone(custom_section)
        self.assertNotIn("karpathy-guidelines", custom_section)

    def test_custom_skill_in_custom_section(self):
        """Custom skills must appear in '## Custom Skills' section."""
        self._create_local_skill("my-project-skill", "Project specific")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()
        md_content = gen.generate_skills_md(result)

        sections = md_content.split("## ")

        custom_section = next(
            (s for s in sections if s.startswith("Custom Skills")), None
        )
        self.assertIsNotNone(custom_section)
        self.assertIn("my-project-skill", custom_section)

        open_source_section = next(
            (s for s in sections if s.startswith("Open-source Skills")), None
        )
        self.assertIsNotNone(open_source_section)
        self.assertNotIn("my-project-skill", open_source_section)

    def test_table_row_has_correct_type_label(self):
        """Table rows must show correct Type column value."""
        self._create_local_skill("open-skill", "Open")
        self._create_local_skill("custom-skill", "Custom")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": {
                "open-skill": {
                    "source": "org/repo",
                    "sourceType": "github",
                    "computedHash": "x"
                }
            }
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()
        md_content = gen.generate_skills_md(result)

        # Check that open-skill row has "Open-source" type
        self.assertIn("| **open-skill** | Open-source |", md_content)

        # Check that custom-skill row has "Custom" type
        self.assertIn("| **custom-skill** | Custom |", md_content)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling in classification."""

    def setUp(self):
        """Create a temporary project structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.kiro_skills = self.temp_dir / ".kiro" / "skills"
        self.kiro_skills.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_local_skill(self, name: str, description: str = "Test"):
        """Helper: create a local skill directory with SKILL.md."""
        skill_dir = self.kiro_skills / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
        )

    def test_malformed_lock_file_treats_all_as_custom(self):
        """Malformed skills-lock.json should gracefully degrade."""
        self._create_local_skill("some-skill", "Some skill")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text("{ invalid json }")

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        # Should not crash, skill falls to custom
        custom_names = [s["name"] for s in result["Custom"]]
        self.assertIn("some-skill", custom_names)

    def test_skill_dir_without_skill_md_is_ignored(self):
        """A skill directory without SKILL.md is not discovered."""
        empty_dir = self.kiro_skills / "empty-skill"
        empty_dir.mkdir()

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        all_names = []
        for category_skills in result.values():
            all_names.extend([s["name"] for s in category_skills])

        self.assertNotIn("empty-skill", all_names)

    def test_skill_with_malformed_frontmatter_is_skipped(self):
        """A skill with broken YAML frontmatter is skipped gracefully."""
        skill_dir = self.kiro_skills / "broken-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nbad: yaml: {broken\n---\n")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        # Should not raise
        result = gen.discover_skills()

        all_names = []
        for category_skills in result.values():
            all_names.extend([s["name"] for s in category_skills])

        self.assertNotIn("broken-skill", all_names)

    def test_lock_file_with_list_format(self):
        """Handle alternative list format in skills-lock.json."""
        self._create_local_skill("listed-skill", "Listed skill")

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": [
                {
                    "name": "listed-skill",
                    "source": "org/listed-repo",
                    "sourceType": "github"
                }
            ]
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source_names = [s["name"] for s in result["Open-source"]]
        custom_names = [s["name"] for s in result["Custom"]]

        self.assertIn("listed-skill", open_source_names)
        self.assertNotIn("listed-skill", custom_names)

    def test_claude_skills_dir_discovery(self):
        """Skills in .claude/skills/ follow same classification rules."""
        claude_skills = self.temp_dir / ".claude" / "skills"
        claude_skills.mkdir(parents=True)

        # Create a skill in .claude/skills/
        skill_dir = claude_skills / "claude-custom-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: claude-custom-skill\ndescription: Claude skill\n---\n"
        )

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        custom_names = [s["name"] for s in result["Custom"]]
        self.assertIn("claude-custom-skill", custom_names)

    def test_claude_skills_in_lock_file_are_open_source(self):
        """Skills in .claude/skills/ that are in lock file are Open-source."""
        claude_skills = self.temp_dir / ".claude" / "skills"
        claude_skills.mkdir(parents=True)

        skill_dir = claude_skills / "oss-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: oss-skill\ndescription: OSS\n---\n"
        )

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "skills": {
                "oss-skill": {
                    "source": "org/oss-repo",
                    "sourceType": "github",
                    "computedHash": "h"
                }
            }
        }))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        open_source_names = [s["name"] for s in result["Open-source"]]
        custom_names = [s["name"] for s in result["Custom"]]

        self.assertIn("oss-skill", open_source_names)
        self.assertNotIn("oss-skill", custom_names)


class TestAgentSkillClassification(unittest.TestCase):
    """Verify agent skills from plugins are classified correctly."""

    def setUp(self):
        """Create a temporary project structure."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.kiro_skills = self.temp_dir / ".kiro" / "skills"
        self.kiro_skills.mkdir(parents=True)
        self.claude_dir = self.temp_dir / ".claude"
        self.claude_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_enabled_plugin_skills_are_agent_skills(self):
        """Skills from enabled plugins are classified as Agent Skill."""
        settings_path = self.claude_dir / "settings.json"
        settings_path.write_text(json.dumps({
            "enabledPlugins": {
                "agent-skills@addy-agent-skills": True
            }
        }))

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        agent_names = [s["name"] for s in result["Agent Skill"]]
        self.assertTrue(len(agent_names) > 0,
                        "Agent skills should be discovered when plugin is enabled")

    def test_disabled_plugin_no_agent_skills(self):
        """Disabled plugins should NOT produce agent skills."""
        settings_path = self.claude_dir / "settings.json"
        settings_path.write_text(json.dumps({
            "enabledPlugins": {
                "agent-skills@addy-agent-skills": False
            }
        }))

        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        agent_names = [s["name"] for s in result["Agent Skill"]]
        self.assertEqual(len(agent_names), 0,
                         "Disabled plugin should not produce agent skills")

    def test_no_settings_file_no_agent_skills(self):
        """Missing settings.json means no agent skills."""
        lock_path = self.temp_dir / "skills-lock.json"
        lock_path.write_text(json.dumps({"version": 1, "skills": {}}))

        gen = AIDocumentationGenerator(self.temp_dir)
        result = gen.discover_skills()

        agent_names = [s["name"] for s in result["Agent Skill"]]
        self.assertEqual(len(agent_names), 0)


if __name__ == "__main__":
    unittest.main()
