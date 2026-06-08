---
name: semantic-release
description: |
  Guide to implementing and maintaining automated versioning and release workflows using semantic-release, conventional commits, and OIDC-based publishing. Use this skill whenever the user asks about: setting up semantic versioning, implementing automated releases, writing conventional commit messages, configuring semantic-release, managing npm package publishing, understanding version bumping rules, migrating from manual releases, troubleshooting release workflows, or implementing release automation best practices. This skill covers semver concepts, commit message formats, the automated release process, OIDC authentication, configuration, real-world examples, and troubleshooting strategies.
compatibility: "git, npm, GitHub Actions"
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

**Scope** (optional): Area affected — e.g., `api`, `auth`, `db`, `types`, `docs`. Can include ticket ID: `api(#123)` or `api(#123, docs)`. Helps readers scan the log.

**Subject** (required): Concise description (50 chars or less, imperative mood, no period).

**Body** (optional): Detailed explanation of *why* and *what*. Wrap at 72 chars. Include motivation, contraints, tradeoffs.

**Footer** (optional): 
- Reference issues: `Closes #123`, `Fixes #456` (links commit to issue, auto-closes on merge)
- Ticket ID: `Ticket: #123` or `Issue: #123` for explicit tracking
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-Authored-By: Name <email>`

### Branch Naming Convention

Use this pattern to associate branches with tickets:

```
<type>/<ticket-id>-<description>
```

**Examples:**
- `feat/55-query-athlete` — Feature branch for issue #55
- `fix/42-race-condition` — Bug fix for issue #42
- `chore/123-upgrade-deps` — Maintenance for issue #123

This links your branch history to your issue tracker and makes it easy to trace commits back to requirements. When your PR merges, the commit messages automatically reference the ticket ID.

---

## Complete Development Workflow

This is the end-to-end workflow from starting work on a feature to pushing commits for release.

### 1. Create a Feature Branch

**Always base new branches on `main`:**

```bash
# Fetch latest from remote
git fetch origin

# Create and checkout a new branch from main
git checkout -b <type>/<task-id>-<description> origin/main
```

**Examples:**
```bash
git checkout -b feat/55-add-rate-limiting origin/main
git checkout -b fix/42-resolve-race-condition origin/main
git checkout -b chore/123-upgrade-dependencies origin/main
```

**Why base on `main`?** Ensures your branch includes all latest changes and release commits from the main branch, preventing conflicts and merge issues later.

### 2. Make Changes and Commit

Write code, tests, and documentation with proper conventional commit messages:

```bash
# Stage your changes
git add <files>

# Commit with conventional format
git commit -m "feat(api, #55): add rate limiting support

Implements exponential backoff for API rate limits, protecting
endpoints from abuse. Adds configuration options for max requests
per window and cooldown duration.

Closes #55"
```

**Commit message checklist:**
- ✓ Type is valid (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`)
- ✓ Includes task ID in scope or footer: `feat(api, #55)` or `Closes #55`
- ✓ Subject is under 50 characters and imperative mood
- ✓ Body explains *why*, not just *what*
- ✓ Footer references the issue: `Closes #X` or `Fixes #X`

### 3. Push to Remote

When ready to create a pull request or share your work:

```bash
# Push your branch to remote
git push origin <type>/<task-id>-<description>
```

**Or use the shorthand if git tracks the branch:**
```bash
git push -u origin HEAD
```

The `-u` flag sets the upstream branch, so future `git push` commands work without specifying the remote.

**What happens on push:**
- GitHub sees your branch with the task ID in the name
- Commits with `Closes #X` are linked to the issue
- CI/CD workflows may trigger (e.g., tests, linting)
- Your branch is ready for a pull request

### 4. Create a Pull Request

```bash
# Option A: Via GitHub CLI
gh pr create --title "feat(api): add rate limiting support" \
  --body "Implements exponential backoff for API rate limits.

Closes #55"

# Option B: Via GitHub web interface
# Open https://github.com/org/repo/pull/new/<branch-name>
```

**PR best practices:**
- Use the same conventional format as commit messages
- Reference the task in the description
- Link related issues with `Closes #55`, `Fixes #42`
- Request reviews from team members

### 5. Code Review and Merge

```bash
# After approval, merge to main
# (via GitHub UI or command line)
```

**Automatic on merge:**
- semantic-release analyzes commits since last release
- Determines version bump based on commit types
- Updates CHANGELOG.md with auto-generated notes
- Publishes to npm (if applicable)
- Creates GitHub release with release notes
- Closes linked issues automatically

### Complete Example Workflow

```bash
# 1. Start from main
git fetch origin
git checkout -b feat/55-rate-limiting origin/main

# 2. Make changes
echo "rate limit logic" > src/rate-limiter.ts
git add src/rate-limiter.ts

# 3. Commit with conventional format
git commit -m "feat(api, #55): add rate limiting support

Implements exponential backoff for API rate limits.

Closes #55"

# 4. Push to remote
git push -u origin feat/55-rate-limiting

# 5. Create PR (via GitHub UI or CLI)
gh pr create --title "feat(api, #55): add rate limiting support" \
  --body "Implements exponential backoff.

Closes #55"

# 6. After approval, merge to main via GitHub UI
# semantic-release automatically:
# - Detects the feature commit
# - Bumps MINOR version
# - Generates changelog
# - Publishes to npm
# - Creates GitHub release
# - Closes issue #55
```

### Branch Management

**Keep branches clean:**
- Delete local branch after merge: `git branch -d feat/55-rate-limiting`
- Delete remote branch: `git push origin --delete feat/55-rate-limiting`
- Or use GitHub UI to auto-delete on PR merge

**Check your branches:**
```bash
git branch -a                    # List all branches
git log --oneline -10            # View recent commits
git log --graph --all --oneline  # Visual branch history
```

### Real-world examples

**Feature with issue reference (closes ticket):**
```
feat(auth): implement OAuth 2.0 support

Adds OAuth 2.0 authentication flow with PKCE support, allowing
users to authenticate via external providers. Implements token
refresh logic and session management.

Closes #55
```

**Feature from task/ticket branch:**
```
# Branch: feat/55-oauth-implementation
feat(auth): implement OAuth 2.0 support

Adds OAuth 2.0 authentication flow with PKCE support, allowing
users to authenticate via external providers. Implements token
refresh logic and session management.

Closes #55
```

When merged, this commit automatically closes issue #55 and the branch history shows the ticket ID.

**Bug fix with ticket reference:**
```
fix(types): correct athlete response interface

The StravaAthlete type was missing the profile_photo field,
causing type mismatches in athlete detail endpoints. Added the
missing field and updated related interfaces.

Fixes #42
```

**Performance improvement with ticket:**
```
perf(db): add index to email lookup

Reduces athlete email lookup from 500ms to 50ms by adding
a database index on the email column. Improves search performance
for the admin user management page.

Related to #89
```

**Breaking change with multiple tickets:**
```
feat!: redesign API response structure

BREAKING CHANGE: response format changed from XML to JSON.
All clients must update parsing logic. Migration guide in docs.

Addresses: #123, #124, #125
Closes #126

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

Linking commits to ticket IDs creates an audit trail connecting requirements to implementation. When reviewing releases or debugging issues, you can trace back to the original request, discussion, and context.

### Methods to include ticket IDs

**1. In the footer (recommended for automation):**
```
feat(api): add rate limiting support

Implements exponential backoff for API rate limits.

Closes #55
```

The `Closes #55` footer automatically closes the GitHub issue when the commit is merged.

**2. In the scope:**
```
feat(api, #55): add rate limiting support
```

This puts the ticket ID front-and-center in the commit log.

**3. In branch names (for traceability):**
```
feat/55-add-rate-limiting
chore/55-sync
fix/42-race-condition
```

When you use `git log --oneline` or view PR history, the ticket ID appears in the branch name, making it easy to connect commits to issues.

**4. Multiple tickets in one commit:**
```
feat(auth): implement OAuth 2.0 and GitHub App integration

Adds OAuth 2.0 support (#55) and GitHub MCP integration (#56).
Handles session management and token refresh.

Closes #55
Closes #56
```

### How semantic-release uses ticket references

When semantic-release generates the changelog and release notes, it automatically:
1. **Parses `Closes #X` and `Fixes #X`** footer lines
2. **Converts them to hyperlinks** in the generated CHANGELOG.md
3. **Links each release to its issues** on GitHub
4. **Creates a complete audit trail** from requirement (issue) → commit → release

**Example generated changelog entry:**
```
## [1.4.0] - 2026-06-08

### Features
- **api**: Add rate limiting support ([#55](https://github.com/org/repo/issues/55))
- **auth**: Implement OAuth 2.0 ([#42](https://github.com/org/repo/issues/42))

### Bug Fixes
- **db**: Fix race condition in query cache ([#89](https://github.com/org/repo/issues/89))
```

### Configuration for ticket tracking

To customize how semantic-release links tickets in changelogs, update `.releaserc.json`:

```json
{
  "plugins": [
    ["@semantic-release/release-notes-generator", {
      "preset": "angular",
      "presetConfig": {
        "issueUrlFormat": "https://github.com/org/repo/issues/{{id}}",
        "compareUrlFormat": "https://github.com/org/repo/compare/{{previousTag}}...{{currentTag}}"
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
