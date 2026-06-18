#!/usr/bin/env python3
"""
Test suite for js-project-structure skill.
Tests project initialization, validation, and setup workflows.
Designed to run in GitHub Actions CI/CD pipeline.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestProjectInitialization(unittest.TestCase):
    """Test project initialization workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_project_local_unscoped(self):
        """Test local project initialization without scope."""
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        result = subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Init failed: {result.stderr}")
        self.assertTrue((Path(self.temp_dir) / "test-lib").exists())
        self.assertTrue((Path(self.temp_dir) / "test-lib" / "package.json").exists())

    def test_init_project_local_scoped(self):
        """Test local project initialization with scope."""
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        result = subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "@torqlab",
                "A scoped test library",
                "no",
                "",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Init failed: {result.stderr}")

        package_json_path = Path(self.temp_dir) / "test-lib" / "package.json"
        with open(package_json_path) as f:
            package_data = json.load(f)
        self.assertEqual(package_data["name"], "@torqlab/test-lib")

    def test_project_structure_complete(self):
        """Verify all required project files are created."""
        required_files = [
            "package.json",
            "tsconfig.json",
            "eslint.config.mjs",
            ".prettierrc",
            "commitlint.config.js",
            ".releaserc.json",
            ".mcp.json",
            ".env.example",
            "README.md",
            ".github/workflows/verify.yml",
            ".github/workflows/publish.yml",
            ".husky/commit-msg",
            ".husky/pre-push",
            "src/index.ts",
            "src/index.test.ts",
        ]

        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )

        project_dir = Path(self.temp_dir) / "test-lib"
        for file_path in required_files:
            full_path = project_dir / file_path
            self.assertTrue(
                full_path.exists(), f"Required file missing: {file_path}"
            )


class TestProjectValidation(unittest.TestCase):
    """Test project validation scripts."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # Initialize a test project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )
        self.project_dir = Path(self.temp_dir) / "test-lib"

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_validate_setup_passes(self):
        """Test validation script passes on valid project."""
        script_path = Path(__file__).parent / "scripts" / "validate-setup.sh"
        result = subprocess.run(
            ["bash", str(script_path), str(self.project_dir)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Validation failed: {result.stderr}")


class TestPackageJsonConfiguration(unittest.TestCase):
    """Test package.json configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # Initialize a test project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )
        self.project_dir = Path(self.temp_dir) / "test-lib"

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_package_json_valid(self):
        """Verify package.json is valid JSON."""
        package_json_path = self.project_dir / "package.json"
        with open(package_json_path) as f:
            data = json.load(f)
        self.assertIn("name", data)
        self.assertIn("version", data)
        self.assertIn("description", data)

    def test_package_json_has_scripts(self):
        """Verify package.json has required scripts."""
        package_json_path = self.project_dir / "package.json"
        with open(package_json_path) as f:
            data = json.load(f)

        required_scripts = [
            "build",
            "build:types",
            "build:esm",
            "build:cjs",
            "lint",
            "format",
            "format:check",
        ]
        scripts = data.get("scripts", {})
        for script in required_scripts:
            self.assertIn(script, scripts, f"Missing script: {script}")

    def test_package_json_dependencies(self):
        """Verify required dependencies are listed."""
        package_json_path = self.project_dir / "package.json"
        with open(package_json_path) as f:
            data = json.load(f)

        dev_deps = data.get("devDependencies", {})
        required = ["typescript", "eslint", "prettier", "husky"]
        for dep in required:
            self.assertIn(dep, dev_deps, f"Missing dependency: {dep}")


class TestConfigurationFiles(unittest.TestCase):
    """Test configuration file validity."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # Initialize a test project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )
        self.project_dir = Path(self.temp_dir) / "test-lib"

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tsconfig_valid(self):
        """Verify tsconfig.json is valid JSON."""
        tsconfig_path = self.project_dir / "tsconfig.json"
        with open(tsconfig_path) as f:
            data = json.load(f)
        self.assertIn("compilerOptions", data)
        self.assertTrue(data["compilerOptions"].get("strict", False))

    def test_eslint_config_exists(self):
        """Verify eslint.config.mjs exists."""
        eslint_path = self.project_dir / "eslint.config.mjs"
        self.assertTrue(eslint_path.exists())

    def test_prettier_config_valid(self):
        """Verify .prettierrc is valid JSON."""
        prettier_path = self.project_dir / ".prettierrc"
        with open(prettier_path) as f:
            data = json.load(f)
        self.assertIn("printWidth", data)
        self.assertIn("semi", data)

    def test_commitlint_config_valid(self):
        """Verify commitlint.config.js exists and is readable."""
        commitlint_path = self.project_dir / "commitlint.config.js"
        self.assertTrue(commitlint_path.exists())

    def test_releaserc_valid(self):
        """Verify .releaserc.json is valid JSON."""
        releaserc_path = self.project_dir / ".releaserc.json"
        with open(releaserc_path) as f:
            data = json.load(f)
        self.assertIn("branches", data)
        self.assertIn("plugins", data)


class TestGitSetup(unittest.TestCase):
    """Test git repository setup."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # Initialize a test project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )
        self.project_dir = Path(self.temp_dir) / "test-lib"

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_git_initialized(self):
        """Verify .git directory exists."""
        git_dir = self.project_dir / ".git"
        self.assertTrue(git_dir.exists())

    def test_git_branch_main(self):
        """Verify default branch is main."""
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout.strip(), "main")

    def test_initial_commit_exists(self):
        """Verify initial commit was created."""
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
        )
        self.assertGreater(len(result.stdout.strip().split("\n")), 0)

    def test_initial_commit_message(self):
        """Verify initial commit has expected message."""
        result = subprocess.run(
            ["git", "log", "--format=%B", "-n", "1"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
        )
        self.assertIn("chore: initialize project", result.stdout)


class TestHuskyHooks(unittest.TestCase):
    """Test Husky git hooks installation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # Initialize a test project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )
        self.project_dir = Path(self.temp_dir) / "test-lib"

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_commit_msg_hook_installed(self):
        """Verify commit-msg hook is installed."""
        hook_path = self.project_dir / ".husky" / "commit-msg"
        self.assertTrue(hook_path.exists())

    def test_pre_push_hook_installed(self):
        """Verify pre-push hook is installed."""
        hook_path = self.project_dir / ".husky" / "pre-push"
        self.assertTrue(hook_path.exists())


class TestInputValidation(unittest.TestCase):
    """Test input validation and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_project_name_required(self):
        """Verify script fails without project name."""
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        result = subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_duplicate_project_fails(self):
        """Verify script fails if project already exists."""
        # Create first project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )

        # Try to create again
        result = subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "Another library",
                "no",
                "",
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)


class TestSourceCodeGeneration(unittest.TestCase):
    """Test generated source code structure."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)

        # Initialize a test project
        script_path = Path(__file__).parent / "scripts" / "init-project.sh"
        subprocess.run(
            [
                "bash",
                str(script_path),
                "test-lib",
                "",
                "A test library",
                "no",
                "",
            ],
            capture_output=True,
        )
        self.project_dir = Path(self.temp_dir) / "test-lib"

    def tearDown(self):
        """Clean up temp files."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_src_directory_exists(self):
        """Verify src/ directory is created."""
        src_dir = self.project_dir / "src"
        self.assertTrue(src_dir.exists())

    def test_index_ts_exists(self):
        """Verify src/index.ts is created."""
        index_ts = self.project_dir / "src" / "index.ts"
        self.assertTrue(index_ts.exists())

    def test_test_file_exists(self):
        """Verify example test file is created."""
        test_file = self.project_dir / "src" / "index.test.ts"
        self.assertTrue(test_file.exists())

    def test_github_workflows_exist(self):
        """Verify GitHub workflow files are created."""
        verify_wf = self.project_dir / ".github" / "workflows" / "verify.yml"
        publish_wf = self.project_dir / ".github" / "workflows" / "publish.yml"
        self.assertTrue(verify_wf.exists())
        self.assertTrue(publish_wf.exists())


if __name__ == "__main__":
    unittest.main()
