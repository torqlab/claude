---
name: js-project-structure
description: |
  Set up a new TypeScript/Node.js project or align an existing one with TORQ standards. This skill initializes complete project structure with semantic versioning, automated npm publishing, git validation, and CI/CD workflows.

  Use this skill whenever: user needs to create a new JavaScript/TypeScript project, user wants to bootstrap a new package with proper tooling, user needs to align an existing project with TORQ standards, user is setting up a new npm-publishable library, or any context mentioning TypeScript/Node.js project initialization.

  The skill handles: creating GitHub repository (optional), cloning template, customizing config files, installing dependencies, setting up git hooks, validating all configurations, and providing next steps for development.

  Scope: TypeScript/Node.js projects using Bun, semantic versioning, conventional commits, and automated publishing.

compatibility: "git, gh CLI, bun, npm, Node.js 24+"
---

# JS Project Structure

A comprehensive skill for setting up TypeScript/Node.js projects that follow TORQ standards.

## When to Use This Skill

- ✅ Creating a new npm-publishable library or package
- ✅ Starting a new TypeScript project from scratch
- ✅ Aligning an existing project with torq conventions
- ✅ Setting up automated semantic versioning and publishing
- ✅ Ensuring consistent project structure across torq monorepo

## What This Skill Provides

When you use this skill, you get:

- **TypeScript** with strict type checking and dual-format builds (ESM + CJS)
- **Git Hooks** (Husky) for validating commits and branches before push
- **Commit Validation** (commitlint) enforcing conventional commits with required scope
- **Branch Validation** (validate-branch-name) enforcing semantic naming (`<type>/<ticket_id>-<description>`)
- **Code Quality** (ESLint + Prettier) with integrated configuration to avoid conflicts
- **Testing Framework** (Bun test runner) included and pre-configured
- **CI/CD Workflows** (GitHub Actions) for automated testing, linting, building, and publishing
- **Semantic Versioning** (semantic-release) that automatically determines version bumps and publishes to npm
- **OIDC Trusted Publishing** for secure, keyless publishing to npm

## Prerequisites

Before using this skill, ensure you have:

- ✅ GitHub account (for repository creation)
- ✅ GitHub CLI (`gh`) installed and authenticated
- ✅ Bun or Node.js 24+ installed locally
- ✅ (Optional) GitHub App credentials configured in `.env` for publishing

**Important Note on Branch Rulesets**: GitHub does not automatically clone branch rulesets when creating repositories from templates. After creating your repository from this template, you must manually configure branch rulesets in your repository settings (see Phase 5 below). This ensures your project enforces the same protection rules as other TORQ projects.

## Quick Start

1. **Gather project info:**
   - Project name (e.g., `my-awesome-lib`)
   - Project scope (optional, e.g., `@torqlab/my-awesome-lib`)
   - Project description
   - Whether to create a remote GitHub repository now

2. **Run skill:**
   The skill will clone the torq template, customize files, install dependencies, and initialize git hooks.

3. **Start coding:**
   Create a feature branch with semantic naming and start writing code!

4. **Publish automatically:**
   When merged to main, semantic-release automatically publishes to npm with no manual steps.

---

## Step-by-Step Workflow

### Phase 1: Gather Project Information

The skill will ask you:

**Project Metadata**
```
Project name? (e.g., my-awesome-lib)
Project scope? (optional, e.g., @torqlab; press enter to skip)
Project description? (e.g., A library that does cool things)
```

**Repository Setup**
```
Create a remote GitHub repository? (yes/no)
If yes:
  - GitHub organization? (e.g., torqlab, or your-username)
  - Public or private? (public/private)
```

### Phase 2: Clone and Customize Template

The skill will:

1. **Clone template:**
   ```
   Clone from: https://github.com/torqlab/js-project-template
   ```

2. **Create repository** (if requested):
   ```bash
   gh repo create <name> --template torqlab/js-project-template ...
   ```

3. **Customize files:**
   - `package.json`: Update name, version, description, repository URLs
   - `.env.example`: Provide setup instructions
   - `.github/workflows`: Configure for your setup (npm registry, provenance)

### Phase 3: Install Dependencies and Hooks

The skill will:

1. **Install npm dependencies:**
   ```bash
   bun install
   ```

2. **Install git hooks:**
   ```bash
   npm run prepare  # Installs husky hooks
   ```

3. **Verify hooks are working:**
   - Test commit message validation
   - Test branch name validation
   - Confirm linting and formatting work

### Phase 4: Validate and Test

The skill validates:

- ✅ All configuration files are valid JSON/YAML/JS
- ✅ Git hooks installed correctly
- ✅ Bun/npm dependencies installed
- ✅ ESLint and Prettier initialized
- ✅ TypeScript compilation works
- ✅ Test runner functional

Shows you the structure:
```
your-project/
├── .github/workflows/      # CI/CD (test, lint, publish)
├── .husky/                 # Git hooks (commit, push validation)
├── src/                    # Source code
├── dist/                   # Build output (generated)
├── index.ts                # Entry point
├── package.json            # Project metadata
├── tsconfig.json           # TypeScript strict mode
├── eslint.config.mjs       # Code quality rules
├── .prettierrc              # Formatting rules
├── commitlint.config.js    # Commit validation
├── .releaserc.json         # Semantic versioning config
└── README.md               # Documentation
```

### Phase 5: Configure Branch Rulesets (Manual)

**IMPORTANT**: GitHub does not automatically clone branch rulesets when creating repositories from templates. Rulesets must be configured manually for each new repository.

After your repository is created, configure branch rulesets:

1. **Go to repository settings** → Rulesets
2. **Reference existing ruleset** from torqlab/strava-api:
   - Enforce on: `main` branch
   - Rules:
     - Restrict deletions
     - Require linear history
     - Require pull request with:
       - Squash merge only
       - Dismiss stale reviews on new push
       - Require review thread resolution
     - Required status checks: Build, Check Formatting, Lint, Test

**Alternatively**, use GitHub API to clone rulesets programmatically:
```bash
gh api repos/torqlab/strava-api/rulesets/13422315 | \
  gh api repos/<your-org>/<your-repo>/rulesets --input -
```

For full details, see [GitHub Branch Rulesets Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

---

### Phase 6: Next Steps

The skill prints actionable next steps:

1. **Create a feature branch:**
   ```bash
   git checkout -b feat/1-your-first-feature
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "feat(scope, #1): description of your feature"
   ```

3. **Push and create PR:**
   ```bash
   git push -u origin feat/1-your-first-feature
   ```

4. **Merge to main:**
   When PR is approved and merged, semantic-release automatically:
   - Analyzes commits since last release
   - Determines version bump (major/minor/patch)
   - Updates CHANGELOG.md
   - Publishes to npm
   - Creates GitHub release tag

---

## Git Workflow

### Branch Naming Convention

All branches must follow this pattern:

```
<type>/<ticket_id>-<description>
```

**Examples:**
- `feat/1-add-user-auth`
- `fix/42-resolve-race-condition`
- `chore/99-upgrade-dependencies`
- `docs/15-update-readme`

**Rules:**
- Type: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`
- Ticket ID: numeric (required)
- Description: lowercase, hyphens for spaces

**Special branches allowed:**
- `main`
- `master`
- `develop`

### Conventional Commit Format

All commits must follow this format:

```
<type>(<scope>, #<ticket_id>): <subject>

<body (optional)>

Addresses #<ticket_id>
```

**Example:**
```
feat(api, #1): add user authentication

Implements OAuth 2.0 with JWT tokens. Adds refresh token rotation
and session management for secure user sessions.

Addresses #1
```

**Rules:**
- Type: `feat`, `fix`, `perf`, `chore`, `docs`, `refactor`, `test`
- Scope: REQUIRED (e.g., `api`, `types`, `auth`, `db`)
- Subject: imperative mood, max 50 characters, no period
- Ticket ID: numeric (in scope or footer)
- Footer: `Addresses #<ticket_id>` to link to GitHub issue

### Semantic Versioning

Commits determine version bumps automatically:

| Type | Bump | Example |
|------|------|---------|
| `feat` | MINOR | `1.0.0` → `1.1.0` |
| `fix` | PATCH | `1.0.0` → `1.0.1` |
| `perf` | PATCH | `1.0.0` → `1.0.1` |
| `feat!` | MAJOR | `1.0.0` → `2.0.0` (breaking change) |
| `chore`, `docs`, `test` | NONE | No version bump |

---

## Git Hooks

This project includes three automated git hooks:

### 1. pre-commit Hook (Before each commit)

Runs code formatting and fixing:

```bash
# Git runs this automatically before commit is saved
bun run format      # Auto-format code with Prettier
bun run lint:fix    # Auto-fix ESLint issues
```

**Checks:**
- ✅ Code is formatted to standards
- ✅ Auto-fixable linting issues are resolved

**Effect:** Files are automatically formatted and fixed before committing. Review changes if needed.

### 2. commit-msg Hook (After commit message entered)

Validates commit message format:

```bash
# Git runs this automatically
npx commitlint --edit "$1"
```

**Checks:**
- ✅ Has type (`feat`, `fix`, etc.)
- ✅ Has scope (never empty)
- ✅ Follows conventional format
- ✅ Subject is under 50 chars

**If validation fails:**
```
❌ Subject must not be empty
   Fix: git commit --amend
```

### 3. pre-push Hook (Before push to remote)

Runs full validation before allowing push:

```bash
# Git runs this automatically before push
bun run build       # Full build (types, ESM, CJS)
tsc --noEmit        # TypeScript type checking
bun run test        # Run all tests
bun run lint        # ESLint check
bun run format:check  # Prettier check
npx validate-branch-name  # Branch naming check
```

**Checks:**
- ✅ Project builds successfully
- ✅ TypeScript types are valid
- ✅ All tests pass
- ✅ Code passes linting
- ✅ Code is properly formatted
- ✅ Branch name follows pattern

**If any check fails, push is blocked.** Fix the issue and try again.

---

## Project Scripts

Available npm scripts:

```bash
# Development
bun run build         # Full TypeScript build (types + ESM + CJS)
bun run build:types   # Generate .d.ts type declarations
bun run build:esm     # Build ES module format
bun run build:cjs     # Build CommonJS format

# Code Quality
bun run lint          # Run ESLint
bun run lint:fix      # Auto-fix ESLint issues
bun run format        # Auto-format with Prettier
bun run format:check  # Check if formatting is correct

# Testing
bun test              # Run all tests with Bun

# Type Checking
tsc --noEmit          # Check TypeScript types without emitting

# Git Hooks
npm run prepare       # Install/update git hooks

# Build Output
bun run clean         # Remove dist/ directory
```

---

## Configuration Files

### package.json

Project metadata and dependencies. Key sections:

- `"type": "module"` — Uses ES modules
- `"main"`, `"module"`, `"types"` — Dual-format exports (ESM + CJS)
- `"engines": { "node": "24.x" }` — Requires Node.js 24
- `"scripts"` — Available npm commands
- `"devDependencies"` — Build and validation tools
- `"publishConfig.provenance"` — Enables OIDC trusted publishing

### tsconfig.json

TypeScript compilation settings:

- `"strict": true` — Enforces strict type checking
- `"target": "ES2022"` — Modern JavaScript syntax
- `"declaration": true` — Generates `.d.ts` files

### eslint.config.mjs

Code quality rules:

- ✅ Immutability: Only `const`, no `let`/`var`
- ✅ Max line length: 100 characters
- ✅ JSDoc required for all functions
- ✅ Node builtins use `node:` prefix
- ✅ ESLint + Prettier integration (no conflicts)

### .prettierrc

Code formatting rules:

- 100-character print width
- Single quotes for strings
- Trailing commas in objects/arrays
- 2-space indentation
- Semicolons required

### .releaserc.json

Semantic-release configuration:

- Release branch: `main`
- Plugins: commit analyzer, changelog generator, npm publisher, git committer
- Enables OIDC trusted publishing (keyless, secure)

### .mcp.json

GitHub Model Context Protocol for Claude Code:

- Configures GitHub API access
- References `.env` for credentials

---

## Publishing to npm

### Automatic Publishing (No Manual Steps!)

1. **Make changes on feature branch:**
   ```bash
   git checkout -b feat/1-my-feature
   # ... make changes ...
   git commit -m "feat(core, #1): add feature"
   git push -u origin feat/1-my-feature
   ```

2. **Create and merge PR:**
   - Create PR on GitHub
   - Merge to `main`

3. **GitHub Actions runs automatically:**
   - Runs all tests, linting, formatting, builds
   - semantic-release analyzes commits
   - Determines version (major/minor/patch)
   - Updates CHANGELOG.md
   - Publishes to npm with OIDC token (keyless!)
   - Creates GitHub release with tag

**Result:** Your package is published to npm with zero manual steps!

### OIDC Trusted Publishing

This project uses GitHub-to-npm OIDC trust, which is:

- **Secure:** No long-lived credentials stored in GitHub
- **Automatic:** Token generated and exchanged at publish time
- **Auditable:** npm records which GitHub repo published each version
- **Keyless:** No `NPM_TOKEN` needed in secrets

Setup is automatic — just ensure your GitHub Actions workflow has:
```yaml
permissions:
  id-token: write
```

---

## Environment Setup (.env)

### For Local Development

Create `.env` file (git-ignored):

```env
# GitHub App credentials (optional, needed for publishing)
GITHUB_APP_ID=your-app-id
GITHUB_APP_PRIVATE_KEY_PATH=/path/to/private-key.pem
GITHUB_INSTALLATION_ID=your-installation-id
```

### For Publishing on CI/CD

GitHub Actions automatically handles:
- OIDC token generation
- npm authentication
- No secrets needed in GitHub

---

## Troubleshooting

### Issue: Git Hooks Not Running

**Symptom:** Bad commits were created, branch validation didn't trigger

**Solution:**
```bash
npm run prepare  # Reinstall hooks
git log --oneline -1  # Verify latest commit
```

**Check installed hooks:**
```bash
ls -la .husky/
```

You should see `commit-msg` and `pre-push` files (executable).

### Issue: Commit Message Rejected

**Symptom:**
```
❌ Subject must not be empty
```

**Cause:** Commit message doesn't follow conventional format

**Fix:**
```bash
# Edit the commit message
git commit --amend

# Format must be: type(scope): subject
# Example: feat(api): add user authentication
```

### Issue: Branch Name Rejected on Push

**Symptom:**
```
❌ Branch name must match pattern: <type>/<ticket_id>-<description>
```

**Solution:** Rename branch (or create new one with correct name)
```bash
# If on wrong branch, rename it
git branch -m feat/1-correct-name

# Or push new branch and delete old
git checkout -b feat/1-correct-name
git push -u origin feat/1-correct-name
git branch -d old-branch-name
```

### Issue: ESLint or Prettier Fails on Push

**Symptom:**
```
❌ ESLint found 3 errors
```

**Solution:**
```bash
# Auto-fix formatting
bun run format

# Manually fix linting errors
bun run lint

# Commit fixes
git add .
git commit -m "fix(code): resolve linting errors"
```

### Issue: Tests Fail on Pre-Push

**Symptom:**
```
❌ FAIL src/index.test.ts
```

**Solution:**
```bash
# Run tests locally to see details
bun test

# Fix code and tests
git add .
git commit -m "test(core): fix failing tests"
```

### Issue: Semantic-Release Not Publishing

**Symptom:** Merged PR but package not on npm

**Checks:**
1. Main branch protection allows semantic-release commits
2. npm organization is correct in `package.json`
3. GitHub Actions workflow has correct permissions
4. Check GitHub Actions logs

---

## Monorepo Setup (.claude Symlink)

If using torq monorepo pattern:

```bash
# Link shared configuration
ln -s ../../.claude .claude
```

This links to shared skills, hooks, and settings across projects.

---

## Quick Reference

| Task | Command |
|------|---------|
| Install deps | `bun install` |
| Run tests | `bun test` |
| Lint code | `bun run lint` |
| Format code | `bun run format` |
| Build project | `bun run build` |
| Check dry-run publish | `npx semantic-release --dry-run` |
| Reinstall hooks | `npm run prepare` |

| Commit Type | Example | Bump |
|---|---|---|
| feat | `feat(api): add feature` | MINOR |
| fix | `fix(bug): resolve issue` | PATCH |
| perf | `perf(db): optimize query` | PATCH |
| chore | `chore(deps): update packages` | NONE |
| docs | `docs: update readme` | NONE |

---

## Next Steps

1. ✅ Project is initialized with standard tooling
2. 📝 Create your first feature branch: `git checkout -b feat/1-my-feature`
3. 💻 Write code and tests
4. 🔀 Create PR and merge to main
5. 🚀 semantic-release publishes automatically

For questions or issues, refer to:
- [Semantic Release Docs](https://semantic-release.gitbook.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Bun Documentation](https://bun.sh/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
