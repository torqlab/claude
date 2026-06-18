---
name: js-project-structure
description: |
  Initialize new JavaScript/TypeScript projects from the TORQ template with standardized structure. Use this skill whenever: user asks to create a new JavaScript/TypeScript project, user needs a project initialized with TORQ standards (semantic versioning, conventional commits, git hooks), user wants standardized tooling and configuration (TypeScript, ESLint, Prettier, Bun), or user needs GitHub repository setup. This skill guides you through: collecting project metadata, validating project naming, creating a GitHub repository from the template (using gh repo create --template), cloning the project, installing dependencies and git hooks, customizing configuration, and verifying the setup.
compatibility: "git, gh CLI, bash, bun/npm"
---

## Overview

This skill initializes new JavaScript/TypeScript projects from the TORQ template repository. It provides a standardized project structure aligned with TORQ Project Standards, ensuring consistency across all projects in the organization.

**Key principle:** All new projects use GitHub's template feature (`gh repo create --template torqlab/js-project-template`), which creates a new independent repository with the template as a starting point. This is the canonical, supported way to initialize TORQ projects.

---

## Project Metadata

### Required Information

Before initializing, collect the following:

| Field | Example | Notes |
|-------|---------|-------|
| `project_name` | `my-lib` | Lowercase, no spaces, alphanumeric + hyphens |
| `project_scope` (optional) | `@torq` | Npm scope for scoped packages (e.g., `@torq/my-lib`) |
| `project_description` | `A utility library for X` | Short description for package.json |
| `create_github` | yes/no | Whether to create GitHub repo immediately |
| `github_org` (if yes) | `torqlab` | Organization where repo will be created |

---

## Initialization Workflow

### Step 1: Collect Project Metadata

Agent must gather project information from the user.

**Required fields:**
- `project_name` — Project identifier (required)
- `project_description` — What the project does (required)
- `github_org` — GitHub organization where repo will be created (required)

**Optional fields:**
- `project_scope` — NPM scope (default: unscoped)
- `visibility` — Repository visibility (default: public)

**Example interaction:**

```
Let me gather project information:

1️⃣ Project name? (e.g., my-lib)
   → my-validator

2️⃣ Project description? (e.g., A utility for X)
   → Schema validation library for TypeScript

3️⃣ GitHub organization? (e.g., torqlab)
   → torqlab

4️⃣ NPM scope? (optional, e.g., @torq)
   → @torq

5️⃣ Repository visibility? (public/private, default: public)
   → public
```

---

### Step 2: Validate Project Name

Project name must follow naming conventions:

| Rule | Valid | Invalid | Reason |
|------|-------|---------|--------|
| Lowercase | `my-lib` | `My-Lib`, `MYLIB` | npm standards |
| No spaces | `my-lib` | `my lib` | Git/npm compatibility |
| Alphanumeric + hyphens | `my-lib-v2` | `my_lib`, `my.lib` | Standard format |
| Not reserved | `my-lib` | `test`, `core` | Avoid conflicts |

**If invalid:**

```
❌ Project name invalid: "My Lib"

Valid names:
- Use lowercase (my-lib)
- Use hyphens for spaces
- Alphanumeric + hyphens only

Please provide a valid project name.
```

Stop. Collect new name and re-validate.

---

### Step 3: Create Repository from Template

Use GitHub's `gh repo create --template` command to initialize:

```bash
gh repo create <org>/<project-name> \
  --template torqlab/js-project-template \
  --<visibility> \
  --description "<project_description>"
```

Where:
- `<org>/<project-name>` — GitHub organization and repository name
- `--template torqlab/js-project-template` — Source template repository
- `--public` or `--private` — Repository visibility
- `--description` — Short description for GitHub and npm

**Report on success:**

```
✅ Repository created from template
   URL: https://github.com/<org>/<project-name>
   Template: torqlab/js-project-template
   Visibility: <public|private>
```

**If creation fails:**

```
❌ Repository creation failed

Troubleshoot:
1. Verify GitHub organization exists
2. Verify you have permissions to create repositories
3. Verify gh CLI is authenticated: gh auth status
4. Try again or report error

Command: gh repo create <org>/<project-name> --template torqlab/js-project-template
```

Stop and ask user to resolve.

---

### Step 4: Clone Repository

Clone the newly created repository to local machine:

```bash
git clone https://github.com/<org>/<project-name>.git
cd <project-name>
```

**Report:**

```
✅ Repository cloned locally
   Path: <project-name>/
   Remote: origin (→ https://github.com/<org>/<project-name>.git)
```

---

### Step 5: Install Dependencies

Install project dependencies using bun (or npm as fallback):

```bash
# Prefer bun if available
if command -v bun &> /dev/null; then
  bun install
else
  npm install
fi
```

This automatically:
- Installs npm dependencies (ESLint, Prettier, Bun test runner, etc.)
- Runs `npm run prepare` (initializes Husky git hooks)
- Validates `eslint.config.mjs` and `.prettierrc`

**Report:**

```
✅ Dependencies installed
   Package manager: <bun|npm>
   Location: <project-name>/node_modules
   Git hooks: Installed via Husky
```

---

### Step 6: Customize Project Metadata

Update `package.json` with project-specific information:

```bash
# Edit package.json and update:
# - "name": Full name or scoped name (e.g., @torq/my-validator)
# - "description": Short description from step 1
# - "version": Start at "0.1.0" (semantic-release will manage)
# - "author": Project author info
# - "homepage": GitHub repository URL
# - "repository.url": GitHub repository URL
```

**If scoped package:**
```json
{
  "name": "@torq/my-validator",
  "description": "Schema validation library for TypeScript"
}
```

**If unscoped package:**
```json
{
  "name": "my-validator",
  "description": "Schema validation library for TypeScript"
}
```

**Report:**

```
✅ Package metadata customized
   Name: <name>
   Description: <description>
   Version: 0.1.0 (managed by semantic-release)
```

---

### Step 7: (Optional) Configure `.claude` Symlink

If this project is part of the TORQ monorepo, link shared skills and configuration:

```bash
ln -s ../../.claude .claude
```

This enables access to shared TORQ skills and standards. Skip if standalone project.

**Report:**

```
✅ Monorepo symlink configured (if applicable)
   Linked: .claude → ../../.claude
```

---

### Step 8: Verify Setup

Display project structure and next steps:

```
✅ Project setup complete!

📋 Project structure:
   <project-name>/
   ├── .github/workflows/     # CI/CD workflows (verify.yml, publish.yml)
   ├── .husky/                # Git hooks (commit-msg, pre-push)
   ├── src/                   # TypeScript source code
   │   ├── index.ts           # Entry point
   │   └── index.test.ts      # Test example
   ├── package.json           # Project metadata, scripts, dependencies
   ├── tsconfig.json          # TypeScript configuration (strict mode)
   ├── eslint.config.mjs      # ESLint rules (immutability, line length)
   ├── .prettierrc            # Prettier formatting (quotes, semicolons)
   ├── commitlint.config.js   # Commit message validation
   ├── .releaserc.json        # Semantic-release configuration
   ├── .mcp.json              # GitHub MCP server config
   ├── .env.example           # Environment template
   └── README.md              # Project documentation

🚀 Next steps:
   1. cd <project-name>
   2. Edit package.json (name, description, author, etc.)
   3. Create feature branch: git checkout -b feat/1-description
   4. Start coding in src/
   5. Commit with conventional format: feat: add feature
   6. Push branch and create PR
   7. Merge to main for automatic versioning & publishing

📚 Standards:
   - Git: Conventional commits with scopes
   - Versioning: Semantic versioning (feat → minor, fix → patch)
   - Code: TypeScript strict mode, ESLint, Prettier
   - Testing: Bun test runner (src/**/*.test.ts)
   - Publishing: Automatic via semantic-release on main merge (OIDC trusted)

📖 Resources:
   - Template: https://github.com/torqlab/js-project-template
   - Standards: .claude/skills/js-project-structure/references/TORQ_PROJECT_STANDARDS.md
```

---

## Standards Overview

### Commit Format (Conventional Commits)

```
<type>(<scope>, #<ticket_id>): <subject>

<body (optional)>

Addresses #<ticket_id>
```

**Types:** `feat`, `fix`, `perf`, `chore`, `docs`, `refactor`, `test`

**Example:** `feat(api, #42): add rate limiting to endpoints`

### Branch Naming

```
<type>/<ticket_id>-<description>
```

**Example:** `feat/42-rate-limiting`

### Code Quality

- **TypeScript:** Strict mode, ES2022 target
- **Linting:** ESLint with immutability rules (const-only)
- **Formatting:** Prettier (100 chars, 2 spaces, single quotes)
- **Testing:** Bun test runner (no config needed)

### Publishing

- **Automatic:** On merge to main
- **Versioning:** Semantic versioning
  - `feat` → MINOR bump
  - `fix`/`perf` → PATCH bump
  - `feat!` → MAJOR bump
- **Registry:** npm (OIDC Trusted Publishing)

---

## Examples

### Basic Project (Unscoped)

```
User: "Create a new project called url-parser for parsing URLs in the torqlab org"

Agent collects → project_name: url-parser, description: "URL parsing library", org: torqlab
Agent validates → ✅ Valid
Agent creates repo → ✅ gh repo create torqlab/url-parser --template torqlab/js-project-template
Agent clones → ✅ Repository cloned locally
Agent installs → ✅ Dependencies installed, git hooks configured
Agent customizes → ✅ package.json updated
Agent finalizes → ✅ Project ready for development
```

### Scoped Project with Private Repository

```
User: "Initialize a new project @torq/schema-validator, a TypeScript schema validator, make it private, in the torqlab org"

Agent collects → project_name: schema-validator, scope: @torq, org: torqlab, visibility: private
Agent validates → ✅ Valid
Agent creates repo → ✅ gh repo create torqlab/schema-validator --template torqlab/js-project-template --private
Agent clones → ✅ Repository cloned locally
Agent installs → ✅ All dependencies installed
Agent customizes → ✅ Full name: @torq/schema-validator
Agent finalizes → ✅ Private project ready
```

---

## Important Notes

- **Template Authority:** Always use `gh repo create --template torqlab/js-project-template`. This is the canonical, GitHub-approved way to initialize TORQ projects.
- **GitHub Template Feature:** This uses GitHub's native template repository feature, not git cloning. Creates a new independent repository with no link to template history.
- **Configuration Customization:** `package.json` MUST be edited after cloning to set correct name, description, author, and repository URLs.
- **No Manual Git History Reset:** GitHub template feature automatically creates clean git history — no need to `rm -rf .git`.
- **Monorepo Optional:** `.claude` symlink is optional and only for projects within the TORQ monorepo.
- **One Project at a Time:** Initialize one project per request. Multiple projects require separate executions.
- **Required Authentication:** `gh` CLI must be authenticated. User can verify with: `gh auth status`

---

## Future Enhancements

- **Project variants:** Support different template variants (CLI, library, web app, API server)
- **Environment guidance:** Help configure `.env` for OIDC/GitHub App setup
- **Branch rulesets:** Guide through GitHub branch protection rules (not copied from template)
- **First feature workflow:** Create initial feature branch and example commit
- **Documentation scaffolding:** Generate API docs from TypeScript types

---

## References

For detailed information about TORQ project standards, conventions, and best practices, see:
- [TORQ Project Standards](./references/TORQ_PROJECT_STANDARDS.md) — Complete guide to TypeScript/Node.js conventions, version control, testing, CI/CD, and more
