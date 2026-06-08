---
name: pr
description: |
  Guide for creating and updating pull requests aligned with semantic-release workflows. Use this skill whenever the user is creating or updating a PR to ensure it: follows conventional commit rules, includes semantic versioning impact (MAJOR/MINOR/PATCH), references ticket IDs, validates commits are properly formatted, and maintains alignment with automated release processes. This skill integrates with semantic-release to transform raw commits into semantic PRs with version bump predictions and automated changelog integration.
argument-hint: "[--head] [--base] [--owner] [--repo]"
license: MIT
metadata:
  author: Mr.B.Lab
---

# Pull Request Skill (Semantic-Release Aligned)

## Context

You are a GitHub automation assistant specialized in creating pull requests that follow semantic-release workflows. This skill ensures PRs are not just code delivery mechanisms, but semantic containers that trigger automated versioning, changelog generation, and npm publishing.

The skill analyzes branch names and commits to determine version impact, validates conventional commit format, and creates PRs with semantic metadata that enables semantic-release to function correctly.

## Key Principle

Semantic-release operates on **commit metadata**. Your PR must:
1. Have commits that follow conventional format: `type(scope): description`
2. Include ticket references in branch name or commit footers
3. Clearly communicate what version bump it will trigger
4. Link commits to GitHub issues for traceability

## Task

- Determine current git branch automatically
- Extract ticket ID and commit type from branch name
- Analyze commits between branch and main to predict version bump
- Validate branch naming follows semantic-release convention
- Validate commits follow conventional commit format
- Fetch ticket title from GitHub
- Generate PR title: `<ticket-id> <ticket-title>`
- Generate PR body with semantic release impact section
- Create PR with semantic metadata

---

## Instructions

### 1. Get Current Git Branch

Automatically determine the working branch:

```bash
git branch --show-current
```

**Example output:** `feat/55-query-athlete`

This is used as the default source branch (`head`) for the PR.

### 2. Extract Ticket ID and Type from Branch Name

Parse the branch name using semantic-release convention: `<type>/<ticket-id>-<description>`

**Examples:**
- `feat/55-query-athlete` → type: `feat`, ticket: `55`
- `fix/42-race-condition` → type: `fix`, ticket: `42`
- `chore/123-deps` → type: `chore`, ticket: `123`

**Validation:**
- ✅ Branch matches pattern `<type>/<ticket-id>-<rest>`
- ✅ Type is valid: `feat`, `fix`, `perf`, `chore`, `docs`, `refactor`, `test`
- ✅ Ticket ID is numeric: `\d+`

**If validation fails:**
```
❌ Branch Name Invalid

Current branch: my-random-branch
Expected pattern: <type>/<ticket-id>-<description>

Examples:
  - feat/55-add-rate-limiting
  - fix/42-resolve-race-condition
  - chore/123-upgrade-deps

Type must be one of: feat, fix, perf, chore, docs, refactor, test

Please create a branch matching the pattern and try again.
```

### 3. Analyze Commits for Version Bump

Analyze commits between current branch and main to determine what version bump semantic-release will trigger:

```bash
git log origin/main..HEAD --format="%H %s %b"
```

**Commit Analysis Steps:**

1. **Check for BREAKING CHANGE** — If any commit body contains "BREAKING CHANGE:" → **MAJOR bump**
   ```
   fix: resolve race condition
   
   BREAKING CHANGE: Response structure changed from XML to JSON
   ```

2. **Check for feat commits** — If type is `feat` → **MINOR bump**
   ```
   feat(api): add rate limiting support
   ```

3. **Check for fix/perf commits** — If type is `fix` or `perf` → **PATCH bump**
   ```
   fix(db): resolve query timeout
   perf: optimize athlete lookup
   ```

4. **Check for other commits** — `chore`, `docs`, `refactor`, `test` → **NO version bump**
   ```
   docs: add API guide
   chore: update dependencies
   ```

5. **Determine primary type:**
   - If both `feat` and `fix` exist → use `feat` (higher impact)
   - If breaking change exists → use breaking change (highest impact)
   - Otherwise use the highest-impact type found

**Example analysis:**
```
Commit 1: feat(api, #55): add rate limiting
  → Type: feat, Scope: api, Impact: MINOR

Commit 2: test(api, #55): add rate limiting tests
  → Type: test, Impact: NO BUMP

Commit 3: docs(api): document rate limiting
  → Type: docs, Impact: NO BUMP

Primary Type: feat
Version Bump: MINOR ✅
```

### 4. Validate Conventional Commit Format

For each commit, validate:

```
<type>(<scope>): <subject>
```

**Validation checklist:**
- ✅ Type is valid (`feat`, `fix`, `perf`, `chore`, `docs`, `refactor`, `test`)
- ✅ Subject is imperative mood and under 50 chars
- ✅ No period at end of subject
- ✅ Optional scope is lowercase, no spaces
- ✅ Optional footer references issues: `Closes #X`, `Fixes #X`

**If invalid:**
```
⚠️ Commit Format Issue

Commit: "added rate limiting feature"
Issues:
  - ❌ Not imperative mood (should be "add" not "added")
  - ❌ Missing type prefix (should start with "feat:", "fix:", etc)
  - ❌ No issue reference in body or footer

Correct format:
feat(api): add rate limiting support

Implements exponential backoff for API rate limits.
Protects endpoints from abuse with configurable windows.

Closes #55
```

### 5. Fetch Ticket Title from GitHub

Extract ticket ID (e.g., `55` from `feat/55-...`) and fetch the GitHub issue title:

```bash
gh issue view 55 --json title --jq '.title'
```

**Example:**
- Ticket ID: `55`
- GitHub Issue #55 Title: "Query Athlete Data"
- Use in PR title: `55 Query Athlete Data`

**Fallback:** If issue doesn't exist, construct from branch name:
- Branch: `feat/55-query-athlete` → Use: `55 Query Athlete`

### 6. Construct PR Title

Format: `<ticket-id> <ticket-title>`

**Examples:**
- Branch `feat/55-query-athlete`, GitHub issue title "Query Athlete Data" → PR title: `55 Query Athlete Data`
- Branch `fix/42-race-condition`, GitHub issue title "Fix Race Condition in Cache" → PR title: `42 Fix Race Condition in Cache`

This maintains consistency with existing PR naming while supporting semantic-release traceability.

### 7. Construct PR Body

Create body with two main sections: Semantic Release Impact + Changelog

**Template:**

```markdown
# Semantic Release Impact

📦 **Type:** [feat|fix|perf|chore|docs|refactor|test] | 🔼 **Version:** [MAJOR|MINOR|PATCH|none] | 🎫 **Ticket:** #[ID]

**Scope:** [scope from commits, or "general"]
**Breaking Changes:** [yes/no - detail if yes]
**Commits:** [X commits analyzed]

---

# Changelog

## [Ticket ID Title]

[Extracted from CHANGELOG.md if available, or summary from commits]

---

📚 **Learn More:** See the [semantic-release skill](/semantic-release) for commit formatting rules and automated release workflow details.
```

**Example (MINOR bump, feat commit):**

```markdown
# Semantic Release Impact

📦 **Type:** feat | 🔼 **Version:** MINOR | 🎫 **Ticket:** #55

**Scope:** api
**Breaking Changes:** No
**Commits:** 3 commits analyzed

- feat(api, #55): add rate limiting support
- test(api, #55): add rate limiting tests
- docs(api): document rate limiting

---

# Changelog

## [55 Query Athlete Data]

### Added
- Rate limiting support for API endpoints
- Exponential backoff for rate-limited requests
- Configuration options for max requests per window

---

📚 **Learn More:** See the [semantic-release skill](/semantic-release) for commit formatting rules.
```

**Example (PATCH bump, fix commit):**

```markdown
# Semantic Release Impact

📦 **Type:** fix | 🔼 **Version:** PATCH | 🎫 **Ticket:** #42

**Scope:** db
**Breaking Changes:** No
**Commits:** 1 commit analyzed

- fix(db, #42): resolve race condition in query cache

---

# Changelog

## [42 Fix Race Condition in Query Cache]

### Fixed
- Race condition in database query cache that caused stale data returns
- Added query locking to prevent concurrent cache updates

---

📚 **Learn More:** See the [semantic-release skill](/semantic-release) for commit formatting rules.
```

**Example (NO bump, chore/docs commits):**

```markdown
# Semantic Release Impact

📦 **Type:** chore, docs | 🔼 **Version:** none | 🎫 **Ticket:** #123

**Scope:** general
**Breaking Changes:** No
**Commits:** 2 commits analyzed

- chore: update dependencies
- docs: add API guide

---

# Changelog

## [123 Update Dependencies and Docs]

### Changed
- Updated dev dependencies to latest versions
- Added comprehensive API endpoint documentation

---

📚 **Learn More:** See the [semantic-release skill](/semantic-release) for commit formatting rules.
```

### 8. Pre-Creation Checks

Before calling GitHub MCP to create the PR:

1. **Verify parameters:**
   - ✅ `head` differs from `base`
   - ✅ Both branches exist
   - ✅ `owner`/`repo` format valid
   - ✅ Branch matches semantic-release pattern

2. **Validate commits:**
   - ✅ All commits follow conventional format
   - ✅ At least one commit is a version bump (feat/fix/perf) OR user acknowledges no-bump PR
   - ✅ Ticket ID found in branch name

3. **Warn if:**
   - ⚠️ Branch doesn't follow `<type>/<ticket-id>-...` pattern
   - ⚠️ Commits don't follow conventional format
   - ⚠️ Multiple commit types with different scopes (complexity)
   - ⚠️ No ticket ID found

4. **Show summary:**
   ```
   Creating PR from semantic-release branch:
   - Branch: [head]
   - Ticket: [ticket-id] - [ticket-title]
   - Type: [type]
   - Version Bump: [MAJOR/MINOR/PATCH/none]
   - Commits: [count]
   - Target: [base] branch

   Proceed? (yes/no)
   ```

### 9. Apply Parameter Defaults

Set defaults (99% use case):
- **`head`**: Current git branch (from step 1)
  - Override: `--head="custom-branch"`
- **`base`**: `main` (target branch)
  - Override: `--base="develop"`
- **`owner`**: `torqlab`
  - Override: `--owner="other-org"`
- **`repo`**: `torq`
  - Override: `--repo="other-repo"`

**All parameters are optional** — skill runs with sensible defaults.

### 10. PR Creation

Call GitHub MCP `gh_create_pull_request()`:
- `title`: `<ticket-id> <ticket-title>`
- `body`: Semantic Release Impact + Changelog (from step 7)
- `head`: Source branch (validated)
- `base`: Target branch
- `draft`: **true** (always draft to ensure human review of agent-generated content)

Draft mode ensures:
- Signals PR was agent-created and needs review
- Prevents accidental merge before human approval
- Requires explicit "Ready for review" conversion

### 11. Error Handling

**401 Unauthorized**
```
❌ Authentication failed

Check GITHUB_MCP_TOKEN or GitHub CLI credentials are valid and not expired.
```

**403 Forbidden**
```
❌ Permission denied

Verify GitHub token has 'pull_requests:write' permission.
```

**404 Not Found**
```
❌ Branch or repository not found

Verify:
- Branch name is correct: [head]
- Repository exists: [owner]/[repo]
- Branch has been pushed to remote
```

**422 Invalid Parameters**
```
❌ Invalid PR parameters

Check:
- Branch names are valid
- No existing PR from [head] to [base]
- Both branches exist in repository
```

---

## Usage Examples

### Simplest Invocation (99% use case)

**From your feature branch, just run:**

```bash
/pr
```

The skill will:
1. Get current branch: `feat/55-query-athlete`
2. Extract type: `feat`, ticket: `55`
3. Fetch GitHub issue #55 title: "Query Athlete Data"
4. Analyze commits between branch and main
5. Detect version bump: MINOR
6. Use defaults: `owner=torqlab`, `repo=torq`, `base=main`
7. Create PR with title: `55 Query Athlete Data`
8. Add semantic impact section to body
9. Create as draft PR
10. Return PR URL

### With Custom Base Branch

```bash
/pr --base="develop"
```

Uses current branch as `head`, everything else default. Useful for PRs against non-main branches.

### With All Explicit Parameters

```bash
/pr \
  --head="feat/55-query-athlete" \
  --base="main" \
  --owner="torqlab" \
  --repo="torq"
```

### Success Response

```
✅ Pull request created successfully!

PR Details:
- URL: https://github.com/torqlab/torq/pull/123
- Number: #123
- Title: 55 Query Athlete Data
- Status: Draft
- From: feat/55-query-athlete → main

Semantic Release Info:
- Type: feat
- Version Bump: MINOR
- Commits: 3

Next steps: Review, request changes, or mark as "Ready for review".
```

---

## Real-World Scenarios

### Scenario 1: Feature with Issue Reference

**Branch:** `feat/55-add-rate-limiting`
**Commits:**
```
feat(api): add rate limiting support
test(api): add rate limiting tests
```
**GitHub Issue #55:** "Add Rate Limiting to API"

**PR Created:**
- Title: `55 Add Rate Limiting to API`
- Semantic Impact: MINOR bump (feat detected)
- Body includes commit analysis and changelog

### Scenario 2: Bug Fix

**Branch:** `fix/42-resolve-race-condition`
**Commits:**
```
fix(db): resolve race condition in cache
```
**GitHub Issue #42:** "Fix Race Condition in Query Cache"

**PR Created:**
- Title: `42 Fix Race Condition in Query Cache`
- Semantic Impact: PATCH bump (fix detected)
- Body highlights that this is a bug fix with no new features

### Scenario 3: Breaking Change

**Branch:** `feat/99-redesign-response`
**Commits:**
```
feat!: redesign API response structure

BREAKING CHANGE: response format changed from XML to JSON
```
**GitHub Issue #99:** "Redesign API Response Format"

**PR Created:**
- Title: `99 Redesign API Response Format`
- Semantic Impact: MAJOR bump (breaking change detected)
- Body highlights breaking change and migration requirements

---

## Validation Reference

### Valid Branch Names
- ✅ `feat/55-add-feature`
- ✅ `fix/42-resolve-bug`
- ✅ `perf/99-optimize-db`
- ✅ `chore/123-update-deps`
- ✅ `docs/88-add-guide`
- ✅ `refactor/77-simplify-logic`
- ✅ `test/66-add-coverage`

### Invalid Branch Names
- ❌ `feature/add-something` (missing ticket ID and type)
- ❌ `55-add-feature` (missing type prefix)
- ❌ `feat-55-add-feature` (invalid format)
- ❌ `my-random-branch` (no semantic info)

### Valid Commit Messages
```
feat(api): add rate limiting support

Implements exponential backoff for API rate limits.

Closes #55
```

```
fix(db): resolve race condition

Fixes concurrent cache update issue.

Fixes #42
```

```
chore: update dependencies

[skip release]
```

### Invalid Commit Messages
```
Added rate limiting feature          ❌ (not conventional format)
feat: add rate limiting               ❌ (missing ticket reference)
FEAT(API): ADD RATE LIMITING          ❌ (not lowercase)
fix: resolve bug #42                  ❌ (ticket should be in footer or scope)
```

---

## Integration with Semantic-Release

This skill works in concert with semantic-release:

1. **You create a PR** using `/pr` skill
2. **PR describes version impact** based on commit analysis
3. **You or team reviews** the PR and commits
4. **PR merges to main** with semantic-release commits intact
5. **GitHub Actions triggers** semantic-release workflow
6. **semantic-release analyzes commits**, bumps version, generates changelog
7. **Automatic npm publish** happens with version tag and release notes

Your PR is the **planning layer** that predicts what semantic-release will do automatically.

---

## Important Notes

- **All Parameters Optional:** Just run `/pr` with no parameters from your feature branch
  - Current git branch used automatically
  - Defaults: `base=main`, `owner=torqlab`, `repo=torq`

- **Branch Convention Required:** Branch must follow `<type>/<ticket-id>-<description>` pattern
  - Enables automatic ticket ID extraction
  - Aligns with semantic-release conventions
  - If invalid, skill provides guidance on fixing

- **Commits Must Be Conventional:** All commits must follow `<type>(<scope>): <subject>` format
  - semantic-release depends on this for version detection
  - Skill validates and warns if format is incorrect
  - Prevents broken releases from malformed commits

- **Ticket ID Mandatory:** Branch must contain numeric ticket ID
  - Used to fetch GitHub issue title
  - Links commits to requirements
  - Enables automatic issue closing via `Closes #X` footer

- **Draft Mode Always:** PRs created as draft by default
  - Signals agent-generated content needs review
  - Prevents accidental merge before human approval
  - Requires explicit "Ready for review" action

- **Validation Matters:** Skill validates branch naming and commit format upfront
  - Catches issues before PR creation
  - Prevents failed releases post-merge
  - Guides users to correct format with clear error messages

---

## Success Criteria

The skill successfully creates a semantic-release-aligned PR when:

- ✅ Current git branch obtained successfully
- ✅ Branch follows `<type>/<ticket-id>-<description>` pattern
- ✅ Type is valid: `feat`, `fix`, `perf`, `chore`, `docs`, `refactor`, `test`
- ✅ Ticket ID is numeric
- ✅ All commits follow conventional commit format
- ✅ Commits can be analyzed to determine version bump
- ✅ GitHub issue with ticket ID exists (or ticket info derived from branch)
- ✅ PR title follows format: `<ticket-id> <ticket-title>`
- ✅ PR body includes Semantic Release Impact section with type, scope, version bump, breaking changes
- ✅ Both `head` and `base` branches exist
- ✅ No merge conflicts
- ✅ PR doesn't already exist
- ✅ GitHub MCP token valid with correct permissions
- ✅ PR created in draft mode
- ✅ User receives clear success message with PR URL and semantic info

If any condition fails, skill provides actionable error message and guidance.

---

## Related Skills

- **[semantic-release](/semantic-release)** — Understand conventional commits, version bumping rules, and automated release workflow
- **[skill-creator](/skill-creator)** — Create and test new skills (if extending PR creation workflows)

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [semantic-release docs](https://semantic-release.gitbook.io/)
- [GitHub PR API](https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28)