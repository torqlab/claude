---
name: semantic-release
description: |
  Agent-driven workflow for creating git branches and conventional commits aligned with semantic-release. Use this skill whenever: agent needs to create a feature branch based on a GitHub issue from any torqlab repository, agent needs to generate conventional commit messages with proper semantic-release format referencing cross-repo tickets, user needs guidance on branch naming conventions (type/ticket-id-description) for org-wide tickets, user needs guidance on commit message format with resolved ticket references, agent needs to validate and resolve GitHub issues across the torqlab organization, or when implementing local git workflow with semantic versioning and org-wide ticket tracking. This skill guides agents through: resolving ticket location across torqlab org, validating GitHub issue existence in source repository, determining commit type from issue description, creating branches with auto-push to origin, generating commits with mandatory ticket ID references to source repo, and ensuring all commits follow semantic-release conventions for automated versioning and changelog generation. Tickets from any torqlab repository (torqlab/torq, torqlab/claude, etc.) can be used for development in any other torqlab repository. Scope: local workflow only (branch creation + commits). For PR creation and remote operations, use the PR skill.
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

**Scope** (optional): Area affected — e.g., `api`, `auth`, `db`, `types`, `docs`. Can include ticket ID: `api(#3_106)` or `api, #3_106`. Helps readers scan the log.

**Subject** (required): Concise description (50 chars or less, imperative mood, no period).

**Body** (optional): Detailed explanation of *why* and *what*. Wrap at 72 chars. Include motivation, contraints, tradeoffs.

**Footer** (optional): 
- Reference issues: `Closes torqlab/torq#3_106`, `Fixes torqlab/torq#1_42` (links commit to issue with fully qualified reference, auto-closes on merge)
- Ticket ID: `Ticket: torqlab/torq#3_106` for explicit tracking with organization and repository context
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-Authored-By: Name <email>`

### Branch Naming Convention

Use this pattern to associate branches with tickets across multiple project boards:

```
<type>/<board_id>_<ticket_id>-<description>
```

**Examples:**
- `feat/3_106-query-athlete` — Feature branch for board 3, issue #106
- `fix/1_42-race-condition` — Bug fix for board 1, issue #42
- `chore/2_123-upgrade-deps` — Maintenance for board 2, issue #123

This links your branch history to your issue tracker and makes it easy to trace commits back to requirements. When your PR merges, the commit messages automatically reference the board and ticket IDs. Both board_id and ticket_id are required and must be numeric.

---

## Local Development Workflow

This covers the essential local work: creating a branch and writing commits with proper conventional format.

### 1. Agent Validates and Creates Feature Branch

**Agent decision flow:**

Before creating any branch, the agent must validate prerequisites and get human approval.

#### Step 1: Check if ticket IDs are provided

Agent must obtain both board_id and ticket_id. These are mandatory for proper ticket tracking across multiple project boards.

```
❓ Agent asks: "What is the board ID (numeric)?"
❓ Agent asks: "What is the ticket ID (numeric)?"
```

**Or if human provides combined format:**
- If human provides `3_106` → Parse as board_id=3, ticket_id=106, continue to step 2
- If human provides just one ID → Ask for the other separately
- If human doesn't respond → Ask again

**Why both are required:** Board ID identifies which project board contains the ticket. Ticket ID alone is insufficient because the same ticket number may exist on different boards. This ensures unambiguous ticket identification across the entire torqlab organization.

#### Step 2: Resolve ticket location and validate GitHub issue exists

The ticket may exist in any repository within the torqlab organization. Agent must resolve the ticket's location and verify it exists.

**Step 2a: Parse ticket reference**

User may provide ticket reference in these formats:
- `55` (ticket ID only) → Agent searches torqlab/torq first (default repo)
- `torq#55` (repo shorthand) → Expands to torqlab/torq#55
- `torqlab/torq#55` (fully qualified) → Use as-is
- `torqlab/claude#55` (different repo) → Use as-is

**Step 2b: Search for ticket in torqlab organization**

Agent uses gh CLI to find the ticket. Search strategy:

**If explicit repo provided** (e.g., `torqlab/torq#55`):
```bash
gh issue view --repo torqlab/torq 55 --json number,title,body --jq '.number, .title, .body'
```

**If only ticket ID provided** (search default repo first):
```bash
# Try torqlab/torq (default/primary repo)
gh issue view --repo torqlab/torq 55 --json number,title,body --jq '.number, .title, .body'

# If not found in torqlab/torq, search other torqlab repos:
# (agent discovers repo list via: gh repo list torqlab --json nameWithOwner)
# Then queries each repo until ticket is found
```

**If issue NOT found across torqlab org:**
```
❌ GitHub issue #55 not found in torqlab organization

Searched:
1. torqlab/torq (default) — not found
2. Other torqlab repositories — not found

Please verify:
1. Ticket ID is correct (numeric)
2. The ticket exists in any torqlab/X repository

Create or verify the GitHub issue first, then come back with the correct ID.
```
Agent halts. No branch creation proceeds.

**If issue found in a repo:**
- Resolve: which repo contains the ticket (e.g., torqlab/torq, torqlab/claude, etc.)
- Extract: `number`, `title`, `body`
- **Crucially:** Store the source repo for use in step 6 (commit footers)
- Continue to step 3

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

**Format:** `<type>/<board_id>_<ticket_id>-<description>`

Agent generates suggested branch name:
- Extract short description from issue title (2-5 words)
- Convert to lowercase, hyphens for spaces
- Combine: `<inferred-type>/<board_id>_<ticket_id>-<short-description>`

**Example:**
```
Issue torqlab/torq#3_106: "Query Athlete Data from Strava API"
Inferred type: feat
Board ID: 3
Ticket ID: 106
Suggested branch: feat/3_106-query-athlete

Is this correct? (yes/no/custom)
```

- ✅ If human says **yes** → Continue to step 5
- ❌ If human says **no** → Ask for custom branch name
  - Agent validates format: `<type>/<board_id>_<ticket_id>-<description>`
  - Both board_id and ticket_id must be numeric
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

#### Step 1: Extract ticket ID and commit type

From current branch name (`feat/55-query-athlete`):
- Ticket ID: `55`
- Commit type: `feat`

**Mandatory:** Ticket ID and type must be present in all commits.

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

**Priority 2 — Infer from directory structure (if human declines or isn't available):**

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

Combine all pieces. Use the resolved repo from step 2b:

```
<type>(<scope>, #<board_id>_<ticket_id>): <description>

<body - detailed explanation>

Closes <resolved-repo>#<board_id>_<ticket_id>
```

**Example (ticket found in torqlab/torq):**
```
feat(api, #3_106): add rate limiting support

Implements exponential backoff for API rate limits,
protecting endpoints from abuse. Adds configuration
options for max requests per window and cooldown duration.

Closes torqlab/torq#3_106
```

**Example (ticket found in torqlab/claude, commit in same repo):**
```
feat(skills, #1_55): improve semantic-release org-wide support

Enables tickets from any torqlab repo to be used for development
in any other torqlab repo. Adds org-wide ticket resolution.

Closes torqlab/claude#1_55
```

**Example (ticket found in torqlab/torq, commit in torqlab/claude):**
```
feat(integration, #1_42): sync athlete data with Strava API

Integrates with torqlab/torq ticket for coordinated athlete
data fetching across platforms.

Closes torqlab/torq#1_42
```

**Rules:**
- Type, scope, board_id, and ticket_id are mandatory
- Description max 50 chars, imperative mood
- Body is optional but recommended for clarity
- Footer `Closes <resolved-repo>#<board_id>_<ticket_id>` references the ticket in its source repo (agent is NOT permitted to auto-close it)
- Use fully qualified repo reference (e.g., `torqlab/torq`, not `torq`)
- Both board_id and ticket_id must be included in scope or footer

#### Step 5: Show human for approval

Agent presents complete commit message:

```
📋 COMMIT PREVIEW

feat(api, #3_106): add rate limiting support

Implements exponential backoff for API rate limits.

Closes torqlab/torq#3_106

Create this commit? (yes/edit/cancel)
```

- ✅ **yes** → Proceed to step 6
- 📝 **edit** → Ask what to change, rebuild message, show again
- ❌ **cancel** → Ask human what they want to do instead

#### Step 6: Agent creates commit

```bash
git add <files-to-commit>
git commit -m "feat(api, #55): add rate limiting support

Implements exponential backoff for API rate limits.

Closes #55"
```

Report:
```
✅ Commit created: feat(api, #55): add rate limiting support
```

**Important Notes:**

- **Ticket ID is MANDATORY** — Never commit without both `board_id_ticket_id` in scope or footer. Both parts are required for unambiguous ticket tracking across multiple project boards.
- **One commit per logical change** — If multiple features, make multiple commits
- **All commits must follow conventional format** — semantic-release depends on this
- **Scope must be specific** — Not generic "core", but "api", "auth", "db", etc.

### Multiple Commits on a Branch

When multiple commits needed on same branch:

Agent repeats steps 2-6 for each commit:

```bash
# First commit
git commit -m "feat(api, #3_106): add rate limiting support

..."

# More changes
git add src/rate-limiter.test.ts
git commit -m "test(api, #3_106): add rate limiting tests

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
- Auto-close issue torqlab/torq#3_106 (from first commit's footer)

### Example Local Workflow

```bash
# 1. Start from main
git fetch origin
git checkout -b feat/3_106-rate-limiting origin/main

# 2. Make changes and commit
echo "rate limit logic" > src/rate-limiter.ts
git add src/rate-limiter.ts
git commit -m "feat(api, #3_106): add rate limiting support

Implements exponential backoff.

Closes torqlab/torq#3_106"

# 3. Add tests
echo "tests" > src/rate-limiter.test.ts
git add src/rate-limiter.test.ts
git commit -m "test(api, #3_106): add rate limiting tests"

# 4. Document
echo "docs" > docs/rate-limiting.md
git add docs/rate-limiting.md
git commit -m "docs(api): add rate limiting guide"

# Your branch is now ready with proper commits
git log --oneline -3
```

### Real-world examples

**Cross-repo example: ticket in torqlab/torq, development in torqlab/claude:**
```
# User request: "create branch for board 1 ticket 55 about skills improvements"
# Agent resolves ticket #55 → found in torqlab/torq

# Branch created in current repo (torqlab/claude):
feat/1_55-skills-improvements

# Commit made in torqlab/claude, referencing source ticket:
feat(skills, #1_55): improve semantic-release org-wide support

Enables tickets from any torqlab repo to be used for development
in any other torqlab repo. Agent now resolves tickets across org.

Closes torqlab/torq#1_55
```
When this commit is merged to torqlab/claude, the footer references the ticket in its source repo (torqlab/torq) without auto-closing it, preserving the ticket for cross-repo visibility.

**Feature from task/ticket in same repo:**
```
# Branch: feat/3_106-query-athlete
feat(api, #3_106): add rate limiting support

Adds OAuth 2.0 authentication flow with PKCE support, allowing
users to authenticate via external providers. Implements token
refresh logic and session management.

Closes torqlab/torq#3_106
```

When merged, this commit references the ticket in torqlab/torq, maintaining the audit trail across the organization.

**Bug fix with ticket reference:**
```
fix(types): correct athlete response interface

The StravaAthlete type was missing the profile_photo field,
causing type mismatches in athlete detail endpoints. Added the
missing field and updated related interfaces.

Fixes torqlab/torq#1_42
```

**Performance improvement with ticket:**
```
perf(db): add index to email lookup

Reduces athlete email lookup from 500ms to 50ms by adding
a database index on the email column. Improves search performance
for the admin user management page.

Related to torqlab/torq#2_89
```

**Breaking change with multiple tickets:**
```
feat!: redesign API response structure

BREAKING CHANGE: response format changed from XML to JSON.
All clients must update parsing logic. Migration guide in docs.

Addresses: torqlab/torq#1_123, torqlab/torq#1_124, torqlab/torq#1_125
Closes torqlab/torq#1_126

See MIGRATION.md for details.
```

**Maintenance (no version bump) on ticket:**
```
chore: upgrade eslint to v10

Updates dev dependencies to latest patch versions. No behavior changes.
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

Linking commits to fully qualified ticket IDs creates an audit trail connecting requirements to implementation. When reviewing releases or debugging issues, you can trace back to the original request, discussion, and context. With multi-board organizations like torqlab, including both board_id and ticket_id ensures unambiguous ticket identification.

### Methods to include ticket IDs

**1. In the footer (recommended for automation):**
```
feat(api): add rate limiting support

Implements exponential backoff for API rate limits.

Closes torqlab/torq#3_106
```

The `Closes torqlab/torq#3_106` footer automatically closes the GitHub issue when the commit is merged. Use fully qualified reference format: `org/repo#board_id_ticket_id`.

**2. In the scope:**
```
feat(api, #3_106): add rate limiting support
```

This puts both ticket IDs front-and-center in the commit log.

**3. In branch names (for traceability):**
```
feat/3_106-add-rate-limiting
chore/1_55-sync
fix/2_42-race-condition
```

When you use `git log --oneline` or view PR history, the board_id and ticket_id appear in the branch name, making it easy to connect commits to issues.

**4. Multiple tickets in one commit:**
```
feat(auth): implement OAuth 2.0 and GitHub App integration

Adds OAuth 2.0 support (3_55) and GitHub MCP integration (1_56).
Handles session management and token refresh.

Closes torqlab/torq#3_55
Closes torqlab/torq#1_56
```

### How semantic-release uses ticket references

When semantic-release generates the changelog and release notes, it automatically:
1. **Parses `Closes torqlab/torq#X_Y` and `Fixes torqlab/torq#X_Y`** footer lines
2. **Converts them to hyperlinks** in the generated CHANGELOG.md
3. **Links each release to its issues** on GitHub
4. **Creates a complete audit trail** from requirement (issue) → commit → release

**Example generated changelog entry:**
```
## [1.4.0] - 2026-06-08

### Features
- **api**: Add rate limiting support ([torqlab/torq#3_106](https://github.com/torqlab/torq/issues/106))
- **auth**: Implement OAuth 2.0 ([torqlab/torq#1_42](https://github.com/torqlab/torq/issues/42))

### Bug Fixes
- **db**: Fix race condition in query cache ([torqlab/torq#2_89](https://github.com/torqlab/torq/issues/89))
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
