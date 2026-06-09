---
name: semantic-release
description: |
  Agent-driven workflow for creating git branches and conventional commits aligned with semantic-release. Use this skill whenever: agent needs to create a feature branch based on a GitHub issue in the current repository, agent needs to generate conventional commit messages with proper semantic-release format referencing tickets, user needs guidance on branch naming conventions (type/ticket-id-description), user needs guidance on commit message format with resolved ticket references, agent needs to validate GitHub issue existence in the current repository, or when implementing local git workflow with semantic versioning and ticket tracking. This skill guides agents through: validating GitHub issue existence in the current repository only, determining commit type from issue description, creating branches with auto-push to origin, generating commits with mandatory ticket ID references, and ensuring all commits follow semantic-release conventions for automated versioning and changelog generation. Scope: local workflow only (branch creation + commits). For PR creation and remote operations, use the PR skill.
compatibility: "git, gh CLI, GitHub API"
---

## Core Concepts

### Semantic Versioning (semver)
Versioning follows MAJOR.MINOR.PATCH:

| Type | Bumps | Examples | When to use |
|------|-------|----------|-----------|
| `feat` | MINOR | `feat(api): add rate limiting` | New backward-compatible features |
| `fix` | PATCH | `fix(bug): resolve race condition` | Bug fixes and patches |
| `perf` | PATCH | `perf(db): optimize queries` | Performance improvements |
| `feat!` or `BREAKING CHANGE:` | MAJOR | `feat!: remove legacy endpoint` | Breaking API changes |
| `chore` | — | `chore: update deps` | Maintenance (no bump) |
| `docs` | — | `docs: add API guide` | Documentation (no bump) |
| `refactor` | — | `refactor: simplify logic` | Code changes, no behavior change (no bump) |
| `test` | — | `test: add edge cases` | Test additions (no bump) |

**Key principle:** Version numbers communicate API stability to consumers. Breaking changes deserve MAJOR bumps; safe additions get MINOR; fixes get PATCH.

---

## Conventional Commits Format

All commits must follow this standardized format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Structure breakdown

**Type** (required): Classifies the change. Use the table above.

**Scope** (optional): Area affected — e.g., `api`, `auth`, `db`, `types`, `docs`. Can include ticket ID: `api(#106)` or `api, #106`. Helps readers scan the log.

**Subject** (required): Concise description (50 chars or less, imperative mood, no period).

**Body** (optional): Detailed explanation of *why* and *what*. Wrap at 72 chars. Include motivation, constraints, tradeoffs.

**Footer** (optional): 
- Reference issues: `Addresses #106`, `Closes #42` (links commit to issue; use `Addresses` for cross-repo work to preserve ticket for other PRs)
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-Authored-By: Name <email>`

### Branch Naming Convention

Use this pattern to associate branches with tickets in the current repository:

```
<type>/<ticket_id>-<description>
```

**Examples:**
- `feat/106-query-athlete` — Feature branch for issue #106
- `fix/42-race-condition` — Bug fix for issue #42
- `chore/123-upgrade-deps` — Maintenance for issue #123

This links your branch history to your issue tracker and makes it easy to trace commits back to requirements. When your PR merges, the commit messages automatically reference the ticket IDs. Ticket ID is required and must be numeric.

---

## Local Development Workflow

This covers the essential local work: creating a branch and writing commits with proper conventional format.

### 1. Agent Validates and Creates Feature Branch

**Agent decision flow:**

Before creating any branch, the agent must validate prerequisites and get human approval.

#### Step 1: Check if ticket ID is provided

Agent must obtain the ticket ID. This is mandatory for proper ticket tracking.

```
❓ Agent asks: "What is the GitHub issue ID? (numeric)"
```

**Or if human provides ID directly:**
- If human provides `106` → Use as ticket_id, continue to step 2
- If human provides `#106` → Strip hash, use `106`, continue to step 2
- If human doesn't respond → Ask again

**Why required:** Ticket ID uniquely identifies the GitHub issue in the current repository.

#### Step 2: Validate GitHub issue exists

The ticket MUST exist in the current repository. Agent validates it exists.

**Step 2a: Parse ticket reference**

Always search the current repository only:
- `106` (ticket ID only) → Resolve in current repository
- `#106` (with hash) → Strip hash and resolve in current repository

**Step 2b: Search for ticket in current repository**

Agent uses gh CLI to find the ticket:

```bash
# Validate issue exists in current repo
gh issue view <ticket_id> --json number,title,body
```

**If issue NOT found:**

```
❌ GitHub issue #106 not found in this repository

Please verify:
1. Issue ID is correct (numeric)
2. The issue exists in the current repository

Create or verify the GitHub issue first, then come back with the correct ID.
```

Agent halts. No branch creation proceeds.

**If issue found:**

Extract and store:
- Issue `number`
- Issue `title`
- Issue `body`

Continue to step 3.

---

#### Step 3: Determine commit type from issue

Using the issue found in step 2, agent analyzes title and description to infer commit type:

- **`feat`** — New feature or capability
  - Keywords: "add", "implement", "enable", "support"
  - Example: "Add rate limiting to API" → `feat`

- **`fix`** — Bug fix or defect resolution
  - Keywords: "fix", "resolve", "correct", "bug", "issue"
  - Example: "Fix race condition in cache" → `fix`

- **`perf`** — Performance improvement
  - Keywords: "optimize", "speed up", "improve performance", "faster"
  - Example: "Optimize database queries" → `perf`

- **`chore`** — Maintenance, tooling, dependencies
  - Keywords: "update", "upgrade", "deps", "maintenance"
  - Example: "Upgrade dependencies" → `chore`

- **`docs`** — Documentation only
  - Keywords: "document", "guide", "README", "docs"
  - Example: "Add API documentation" → `docs`

- **`refactor`** — Code refactoring (no behavior change)
  - Keywords: "refactor", "restructure", "simplify", "improve code"
  - Example: "Simplify authentication logic" → `refactor`

- **`test`** — Test additions (no behavior change)
  - Keywords: "test", "add coverage", "add tests"
  - Example: "Add unit tests for rate limiter" → `test`

If type is ambiguous, agent asks human:
```
Based on issue title and description, is this a:
  a) feat (new feature)
  b) fix (bug fix)
  c) chore (maintenance)
  d) other (specify)
```

#### Step 4: Generate and confirm branch name

**Format:** `<type>/<ticket_id>-<description>`

Agent generates suggested branch name:
- Extract short description from issue title (2-5 words)
- Convert to lowercase, hyphens for spaces
- Combine: `<inferred-type>/<ticket_id>-<short-description>`

**Example:**
```
Issue #106: "Query Athlete Data from Strava API"
Inferred type: feat
Ticket ID: 106
Suggested branch: feat/106-query-athlete

Is this correct? (yes/no/custom)
```

- ✅ If human says **yes** → Continue to step 5
- ❌ If human says **no** → Ask for custom branch name
  - Agent validates format: `<type>/<ticket_id>-<description>`
  - ticket_id must be numeric
  - If invalid → Ask to reformat and re-validate
- If human provides **custom** → Use it after validation

#### Step 5: Agent creates and pushes branch

Once approved:

```bash
# Fetch latest from remote
git fetch origin

# Create and checkout branch from main
git checkout -b <approved-branch-name> origin/main

# Push to origin
git push -u origin <approved-branch-name>
```

**Report to human:**
```
✅ Branch created and pushed

Branch: <approved-branch-name>
URL: https://github.com/<owner>/<repo>/tree/<approved-branch-name>
Local: <approved-branch-name> (checked out)

Ready for commits!
```

**Why base on `main`?** Ensures your branch includes all latest changes and release commits, preventing conflicts when your work is integrated.

### 2. Agent Generates Conventional Commits

**Prerequisites:**
- ✅ Branch created with ticket ID (from section 1)
- ✅ Changes staged or ready to commit

**Agent workflow:**

#### Step 1: Extract ticket ID and commit type from branch name

From current branch name (e.g., `feat/55-skills-alignment`):
- Type: `feat`
- Ticket ID: `55`
- Description: `skills-alignment`

**Mandatory:** All of these must be present in the branch name. Ticket ID is required.

#### Step 2: Determine scope (with human approval priority)

**Priority 1 — Ask human (preferred):**

Agent lists changed files and asks:
```
Changed files:
  - src/api/rate-limiter.ts
  - src/types/index.ts
  - tests/rate-limiter.test.ts

What is the scope? (e.g., "api", "types", "core")
Or press Enter to use: <primary-scope-suggestion>
```

- ✅ If human provides scope → Use it
- ✅ If human presses Enter → Use suggested scope
- ✅ If human says "multiple" or "general" → Use no scope

**Priority 2 — Infer from directory structure (if human declines):**

Agent analyzes top-level directories:
```
src/
  ├── api/          ← Most files changed here
  ├── types/
  └── utils/
```

Inferred scope: `api` (directory with most changes)

**NEVER use generic scope like "core"** — scopes must be specific and meaningful.

#### Step 3: Get commit description from human

Agent asks for short description:
```
Commit description (imperative mood, max 50 chars):
  Examples: "add rate limiting", "fix race condition"
  
Your description:
```

**Validation:**
- ✅ Imperative mood (starts with verb: add, fix, remove, update)
- ✅ Max 50 characters
- ✅ No period at end
- ✅ Lowercase (except proper nouns)

If invalid → Tell human why and ask for revision.

**Example valid descriptions:**
- ✅ "add rate limiting support"
- ✅ "fix race condition in cache"
- ✅ "update dependencies to 2.0"
- ❌ "Added rate limiting" (not imperative)
- ❌ "add rate limiting support for API requests." (too long, has period)

#### Step 4: Build commit message

Combine all pieces:

```
<type>(<scope>, #<ticket_id>): <description>

<body - detailed explanation>

Addresses #<ticket_id>
```

**Example:**
```
feat(api, #106): add rate limiting support

Implements exponential backoff for API rate limits,
protecting endpoints from abuse. Adds configuration
options for max requests per window and cooldown duration.

Addresses #106
```

**Example (different repo context):**
```
feat(skills, #55): improve semantic-release org-wide support

Enables tickets from any torqlab repo to be used for development
in any other torqlab repo. Agent now resolves tickets in current
repo only.

Addresses #55
```

**Rules:**
- Type, scope, and ticket_id are mandatory in scope or subject
- Description max 50 chars, imperative mood
- Body is optional but recommended for clarity
- Footer `Addresses #<ticket_id>` references the ticket in current repo
- Use only ticket_id in footer (not board_id_ticket_id)
- GitHub issue link resolves to: `https://github.com/<owner>/<repo>/issues/<ticket_id>`

#### Step 5: Show human for approval

Agent presents complete commit message:

```
📋 COMMIT PREVIEW

feat(api, #106): add rate limiting support

Implements exponential backoff for API rate limits.

Addresses #106

Create this commit? (yes/edit/cancel)
```

- ✅ **yes** → Proceed to step 6
- 📝 **edit** → Ask what to change, rebuild message, show again
- ❌ **cancel** → Ask human what they want to do instead

#### Step 6: Agent creates commit

```bash
git add <files-to-commit>
git commit -m "feat(api, #106): add rate limiting support

Implements exponential backoff for API rate limits.

Addresses #106"
```

Report:
```
✅ Commit created: feat(api, #106): add rate limiting support
```

**Important Notes:**

- **Ticket ID is MANDATORY** — Never commit without ticket_id in scope or footer. Required for unambiguous ticket tracking.
- **One commit per logical change** — If multiple features, make multiple commits
- **All commits must follow conventional format** — semantic-release depends on this
- **Scope must be specific** — Not generic "core", but "api", "auth", "db", etc.

### Multiple Commits on a Branch

When multiple commits needed on same branch:

Agent repeats steps 2-6 for each commit:

```bash
# First commit
git commit -m "feat(api, #106): add rate limiting support

..."

# More changes
git add src/rate-limiter.test.ts
git commit -m "test(api, #106): add rate limiting tests

..."

# Even more changes
git add docs/rate-limiting.md
git commit -m "docs(api): document rate limiting

..."
```

When merged, semantic-release will:
- See all three commits
- Recognize `feat` type → MINOR version bump
- Include all commits in changelog
- Reference ticket #106 (from first commit's footer)

### Example Local Workflow

```bash
# 1. Start from main
git fetch origin
git checkout -b feat/106-rate-limiting origin/main

# 2. Make changes and commit
echo "rate limit logic" > src/rate-limiter.ts
git add src/rate-limiter.ts
git commit -m "feat(api, #106): add rate limiting support

Implements exponential backoff.

Addresses #106"

# 3. Add tests
echo "tests" > src/rate-limiter.test.ts
git add src/rate-limiter.test.ts
git commit -m "test(api, #106): add rate limiting tests"

# 4. Document
echo "docs" > docs/rate-limiting.md
git add docs/rate-limiting.md
git commit -m "docs(api): add rate limiting guide"

# Your branch is now ready with proper commits
git log --oneline -3
```

### Real-world examples

**Feature from issue in same repo:**
```
# Branch: feat/106-query-athlete
feat(api, #106): add rate limiting support

Adds OAuth 2.0 authentication flow with PKCE support, allowing
users to authenticate via external providers. Implements token
refresh logic and session management.

Addresses #106
```

When merged, this commit references the ticket in the current repo, maintaining the audit trail.

**Bug fix with ticket reference:**
```
fix(types, #42): correct athlete response interface

The StravaAthlete type was missing the profile_photo field,
causing type mismatches in athlete detail endpoints. Added the
missing field and updated related interfaces.

Addresses #42
```

**Performance improvement with ticket:**
```
perf(db, #89): add index to email lookup

Reduces athlete email lookup from 500ms to 50ms by adding
a database index on the email column. Improves search performance
for the admin user management page.

Addresses #89
```

**Breaking change:**
```
feat!(api, #123): redesign API response structure

BREAKING CHANGE: response format changed from XML to JSON.
All clients must update parsing logic. Migration guide in docs.

Addresses #123

See MIGRATION.md for details.
```

**Maintenance (no version bump) on ticket:**
```
chore(deps, #55): upgrade eslint to v10

Updates dev dependencies to latest patch versions. No behavior changes.

Addresses #55
```

---

## Automated Release Workflow

### The process (fully automated)

1. **Merge PR to `main`** → GitHub Actions workflow triggered
2. **semantic-release analyzes commits** since last release
3. **Determines version bump** based on commit types (MAJOR/MINOR/PATCH or no release)
4. **Updates CHANGELOG.md** with auto-generated release notes from commits
5. **Updates package.json** with new version
6. **Publishes to npm** with the new version tag
7. **Creates GitHub release** with tag and release notes
8. **Auto-commits** CHANGELOG.md and package.json back to main

**Result:** Zero manual steps. Versioning is deterministic and auditable.

### Why no manual steps?

- **Consistency:** Every release uses the same process
- **Audit trail:** Git commits are the source of truth
- **Speed:** Released in seconds, not hours
- **Safety:** Removes human error from version bumping

---

## OIDC Trusted Publishing (npm authentication)

### Why OIDC over NPM_TOKEN?

Traditional NPM_TOKEN approach:
- ❌ Secrets stored in GitHub (exposure risk)
- ❌ Tokens shared across repos (broad scope)
- ❌ Manual rotation required
- ❌ No proof of origin

OIDC Trusted Publishing:
- ✅ No secrets in GitHub
- ✅ Tokens auto-scoped to this repo only
- ✅ Short-lived (minutes, not permanent)
- ✅ Cryptographic proof package came from this repo
- ✅ Automatic token exchange during CI
- ✅ Audit trail via OIDC provider (GitHub)

### Setup (automatic — no action needed)

GitHub Actions provides OIDC token automatically. Requires:

**In workflow YAML:**
```yaml
permissions:
  id-token: write      # Allow OIDC token creation
  contents: write      # Allow git commits back to repo
```

**In package.json:**
```json
{
  "publishConfig": {
    "provenance": true,
    "registry": "https://registry.npmjs.org/"
  }
}
```

The `provenance: true` setting signs each package, proving it originated from this GitHub repository. npm validates the OIDC token automatically during `npm publish`.

**That's it.** No manual configuration needed — GitHub handles token generation, semantic-release handles the publish command.

---

## Configuration

### .releaserc.json (main config file)

Typical production setup:

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github"
  ]
}
```

### Common customizations

**Multiple release branches (next/beta/canary):**
```json
{
  "branches": [
    "main",
    { "name": "next", "prerelease": true },
    { "name": "beta", "prerelease": true }
  ]
}
```

**Custom commit analyzer rules:**
```json
{
  "plugins": [
    ["@semantic-release/commit-analyzer", {
      "releaseRules": [
        { "type": "refactor", "scope": "core", "release": "patch" },
        { "type": "docs", "release": "patch" }
      ],
      "parserOpts": { "noteKeywords": ["BREAKING", "SECURITY"] }
    }]
  ]
}
```

**Custom changelog format:**
```json
{
  "plugins": [
    ["@semantic-release/release-notes-generator", {
      "preset": "angular",
      "presetConfig": {
        "types": [
          { "type": "feat", "section": "Features" },
          { "type": "fix", "section": "Bug Fixes" },
          { "type": "perf", "section": "Performance" }
        ]
      }
    }]
  ]
}
```

---

## Ticket ID Integration

### Why track ticket IDs?

Linking commits to ticket IDs creates an audit trail connecting requirements to implementation. When reviewing releases or debugging issues, you can trace back to the original request, discussion, and context. In the simplified structure, ticket ID uniquely identifies the issue in the current repository.

### Methods to include ticket IDs

**1. In the footer (recommended for automation):**
```
feat(api): add rate limiting support

Implements exponential backoff for API rate limits.

Closes #106
```

The `Closes #106` footer automatically closes the GitHub issue when the commit is merged.

**2. In the scope:**
```
feat(api, #106): add rate limiting support
```

This puts the ticket ID front-and-center in the commit log.

**3. In branch names (for traceability):**
```
feat/106-add-rate-limiting
chore/55-sync
fix/42-race-condition
```

When you use `git log --oneline` or view PR history, the ticket_id appears in the branch name, making it easy to connect commits to issues.

### How semantic-release uses ticket references

When semantic-release generates the changelog and release notes, it automatically:
1. **Parses `Closes #X` and `Addresses #X`** footer lines
2. **Converts them to hyperlinks** in the generated CHANGELOG.md
3. **Links each release to its issues** on GitHub
4. **Creates a complete audit trail** from requirement (issue) → commit → release

**Example generated changelog entry:**
```
## [1.4.0] - 2026-06-09

### Features
- **api**: Add rate limiting support ([#106](https://github.com/torqlab/torq/issues/106))
- **auth**: Implement OAuth 2.0 ([#42](https://github.com/torqlab/torq/issues/42))

### Bug Fixes
- **db**: Fix race condition in query cache ([#89](https://github.com/torqlab/torq/issues/89))
```

### Configuration for ticket tracking

To customize how semantic-release links tickets in changelogs, update `.releaserc.json`:

```json
{
  "plugins": [
    ["@semantic-release/release-notes-generator", {
      "preset": "angular",
      "presetConfig": {
        "issueUrlFormat": "https://github.com/torqlab/torq/issues/{{id}}",
        "compareUrlFormat": "https://github.com/torqlab/torq/compare/{{previousTag}}...{{currentTag}}"
      }
    }]
  ]
}
```

This ensures all issue links point to your GitHub repository.

---

## Local Testing

### Preview what would be released

Before pushing to production, test semantic-release locally:

```bash
# Dry-run: shows what would be released without making changes
npx semantic-release --dry-run

# With debug output to see detailed logs
DEBUG=semantic-release:* npx semantic-release --dry-run

# Test against a specific branch
npx semantic-release --dry-run --branch main
```

The dry-run output shows:
- Commits analyzed since last release
- Determined version bump (MAJOR/MINOR/PATCH or "no release")
- Generated changelog entries
- What would be published to npm
- What GitHub release would be created

### Debugging a specific commit

If a commit isn't being detected correctly:

```bash
# Show how semantic-release parses commits
DEBUG=semantic-release:commit-analyzer npx semantic-release --dry-run
```

Look for log lines like: `"commit 123abc matches type 'feat': bumps MINOR"`

---

## Preventing Unintended Releases

Use `[skip release]` or `[skip-release]` in commit messages to suppress automatic publishing:

```
chore: update readme [skip release]
```

Or in the commit body:
```
fix: minor doc update

This doesn't warrant a release.

[skip-release]
```

This is useful for:
- Documentation-only changes you want in git but not released
- Temporary test commits that shouldn't trigger CI publishing
- Changelog updates you want to manual-edit before releasing

---

## Troubleshooting

### Release not triggered

**Checklist:**
- ✓ Commit message follows conventional commits format
- ✓ Commits are on the `main` branch (or configured release branch)
- ✓ No `[skip release]` flag in commit message
- ✓ Workflow has permission to create GitHub releases and tags

**Debug:**
```bash
npx semantic-release --dry-run
```

If no release is shown, check:
- Commit type is valid (feat, fix, perf, etc.)
- No typos in type (e.g., `feat` not `feature`)

### Wrong version bumped

**Cause:** Incorrect commit type detected.

**Check:**
- Is `BREAKING CHANGE:` footer present? (triggers MAJOR)
- Is type prefixed with `!`? (e.g., `fix!:` triggers MAJOR)
- Is commit type correct? (feat → MINOR, fix → PATCH)

**Fix:** Update commit message and re-push.

### GitHub token issues

**Error:** "Unauthorized" or "insufficient permissions"

**Fixes:**
- Verify workflow permissions in `.github/workflows/release.yml`:
  ```yaml
  permissions:
    id-token: write
    contents: write
  ```
- Check GitHub Actions settings allow token creation
- Verify branch protection rules allow semantic-release to auto-commit

### npm publishing fails

**Error:** "npm ERR! auth" or "OIDC token exchange failed"

**Fixes:**
- Verify `publishConfig.provenance: true` in package.json
- Check npm registry is correct: `https://registry.npmjs.org/`
- Confirm GitHub OIDC is configured for npm (one-time setup)
- Run dry-run to verify config: `npx semantic-release --dry-run`

---

## Migration from Manual Releases

### Before (manual process)
1. Developer manually bumps version in package.json
2. Developer writes changelog entries (often incomplete or inconsistent)
3. Developer runs `npm publish`
4. Developer creates GitHub tag and release manually
5. High error rate, inconsistent versioning

### After (automated with semantic-release)
1. Merge PR with properly formatted conventional commits
2. GitHub Actions automatically analyzes commits, bumps version, generates changelog, publishes, creates release
3. Zero manual steps, consistent versioning, full audit trail

### During migration

1. **Set baseline version** — update package.json to current version (e.g., `1.3.1`)
2. **Deploy configuration** — add .releaserc.json and update workflows
3. **Make first release** — run `npx semantic-release` manually to verify setup
4. **Verify GitHub release** — check that tag and release notes were created
5. **Document for team** — share commit message format guide
6. **Update CI/CD** — configure workflow to run `semantic-release` on every merge to main
7. **Archive old process** — remove manual version bumping steps

### Handling existing commits

If migrating a repo with non-conventional commits:
- Future commits use conventional format
- Old commits are ignored (semantic-release only analyzes since last tag)
- First release may have no changelog entries if baseline commit is old
- This is fine — establish convention going forward

---

## Implementation Checklist

Use this to set up semantic-release in a new project:

- [ ] Install: `npm install --save-dev semantic-release @semantic-release/{commit-analyzer,release-notes-generator,changelog,npm,github}`
- [ ] Create `.releaserc.json` with plugins
- [ ] Update `package.json` with `publishConfig.provenance: true`
- [ ] Create or update CI/CD workflow (e.g., `.github/workflows/release.yml`)
- [ ] Test locally: `npx semantic-release --dry-run`
- [ ] Push to main and verify GitHub Actions runs `semantic-release`
- [ ] Check GitHub for new release tag and npm for new version
- [ ] Document commit message format for team (share this guide)
- [ ] Remove manual version bumping from processes
- [ ] Archive old release documentation

---

## Quick Reference

| Task | Command |
|------|---------|
| Preview release | `npx semantic-release --dry-run` |
| Debug commits | `DEBUG=semantic-release:* npx semantic-release --dry-run` |
| Manual release (testing) | `npx semantic-release` |
| Check version | `npm view . version` |
| View git log | `git log --oneline -10` |
| Format check | Check last 5 commits match conventional format |

| Commit Type | Bumps | Example |
|---|---|---|
| `feat` | MINOR | `feat(api): add endpoint` |
| `fix` | PATCH | `fix(bug): resolve issue` |
| `perf` | PATCH | `perf: optimize` |
| `feat!` | MAJOR | `feat!: breaking change` |
| `chore` | — | `chore: deps` |
| `docs` | — | `docs: update` |

---

## References

- [Semantic Versioning (semver.org)](https://semver.org/)
- [Conventional Commits (conventionalcommits.org)](https://www.conventionalcommits.org/)
- [semantic-release docs](https://semantic-release.gitbook.io/)
- [npm Trusted Publishing](https://docs.npmjs.com/cli/v8/configuring-npm/package-json#publishconfig)
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Commit message best practices](https://chris.beams.io/posts/git-commit/)
