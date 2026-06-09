---
name: pr
description: |
  Agent-driven GitHub PR creation workflow aligned with semantic-release conventions for multi-board ticket management. Use this skill whenever: agent needs to create a pull request from a semantic-release branch, user requests to create or update a PR, agent needs to validate commits before PR creation, agent needs to generate PR title in format "<board_id>-<ticket_id> <ticket-title>", agent needs to auto-generate PR body from commits, or when PR creation requires explicit human approval. This skill guides agents through: validating PR parameters and commits with multi-board ticket IDs, generating PR title and body from semantic-release data, showing human a preview of the PR, requesting explicit human approval before creation, and creating PRs via gh CLI or GitHub MCP. Scope: remote workflow only (PR creation/updates). For local branch and commit work, use the semantic-release skill. Critical: Agent must NEVER create PR without explicit human approval. Both board_id and ticket_id are required. PR body is always auto-generated from commits—no manual description needed.
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

Parse the branch name using semantic-release convention: `<type>/<board_id>_<ticket_id>-<description>`

**Examples:**
- `feat/3_106-query-athlete` → type: `feat`, board_id: `3`, ticket_id: `106`
- `fix/1_42-race-condition` → type: `fix`, board_id: `1`, ticket_id: `42`
- `chore/2_123-deps` → type: `chore`, board_id: `2`, ticket_id: `123`

**Validation:**
- ✅ Branch matches pattern `<type>/<board_id>_<ticket_id>-<rest>`
- ✅ Type is valid: `feat`, `fix`, `perf`, `chore`, `docs`, `refactor`, `test`
- ✅ Both board_id and ticket_id are numeric: `\d+_\d+`

**If validation fails:**
```
❌ Branch Name Invalid

Current branch: my-random-branch
Expected pattern: <type>/<board_id>_<ticket_id>-<description>

Examples:
  - feat/3_106-add-rate-limiting
  - fix/1_42-resolve-race-condition
  - chore/2_123-upgrade-deps

Type must be one of: feat, fix, perf, chore, docs, refactor, test
Both board_id and ticket_id must be numeric.

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
Commit 1: feat(api, #3_106): add rate limiting
  → Type: feat, Scope: api, Ticket: 3_106, Impact: MINOR

Commit 2: test(api, #3_106): add rate limiting tests
  → Type: test, Ticket: 3_106, Impact: NO BUMP

Commit 3: docs(api): document rate limiting
  → Type: docs, Impact: NO BUMP

Primary Type: feat
Version Bump: MINOR ✅
Ticket: 3_106 (from scope)
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
- ✅ Optional footer references issues: `Closes torqlab/torq#3_106`, `Fixes torqlab/torq#1_42`
- ✅ Ticket ID in scope or footer matches branch format: `#board_id_ticket_id`

**If invalid:**
```
⚠️ Commit Format Issue

Commit: "added rate limiting feature"
Issues:
  - ❌ Not imperative mood (should be "add" not "added")
  - ❌ Missing type prefix (should start with "feat:", "fix:", etc)
  - ❌ No ticket reference or wrong format (should be "Closes torqlab/torq#3_106" not "#55")

Correct format:
feat(api, #3_106): add rate limiting support

Implements exponential backoff for API rate limits.
Protects endpoints from abuse with configurable windows.

Closes torqlab/torq#3_106
```

### 5. Fetch Ticket Title from GitHub or Generate from Commits

Extract ticket ID and board ID (e.g., `3` and `106` from `feat/3_106-...`) and try to fetch the GitHub issue title:

```bash
gh issue view torqlab/torq#3_106 --json title --jq '.title'
```

**Priority order for ticket title:**

1. **GitHub Issue Title** — If the issue exists, use it:
   - Branch: `feat/3_106-query-athlete`
   - GitHub Issue torqlab/torq#3_106 Title: "Query Athlete Data"
   - Use in PR title: `3-106 Query Athlete Data`

2. **Generated from Commits** — If issue doesn't exist, analyze commits and generate descriptive title:
   - Analyze all commits for the primary feature/change
   - Use imperative mood (same as commit subjects)
   - Capitalize first letter
   - Keep concise and descriptive
   - Example: Commits `feat(skills, #3_106): add semantic-release universal reusable skill` → PR title: `3-106 Add Semantic-Release Universal Reusable Skill`

3. **Fallback from Branch Name** — Last resort:
   - Branch: `feat/3_106-query-athlete` → Use: `3-106 Query Athlete`
   - Capitalize words, convert hyphens to spaces

### 6. Construct PR Title

**REQUIRED Format:** `<board_id>-<ticket_id> <ticket-title>`

The ticket title must always be derived from one of these sources in order of preference:
1. GitHub issue title (if issue exists)
2. Generated descriptively from commit messages (if issue doesn't exist)
3. Branch name as fallback

**Examples:**
- Branch `feat/3_106-query-athlete`, GitHub issue exists → PR title: `3-106 Query Athlete Data`
- Branch `chore/1_23-claude-symlink`, no issue, commits include `feat(skills, #1_23): add semantic-release...` → PR title: `1-23 Add Semantic-Release Universal Reusable Skill`
- Branch `fix/2_42-race-condition`, GitHub issue exists → PR title: `2-42 Fix Race Condition in Cache`

This format ensures:
- Consistent PR naming across the project
- Both board_id and ticket_id appear first for easy multi-board reference
- Semantic-release can parse and link commits to tickets
- Descriptive titles help with code review and navigation

### 7. Agent Constructs Auto-Generated PR Body

PR body is **always auto-generated** from commits — no manual description needed.

#### Body Structure

```markdown
# Semantic Release Impact

📦 **Type:** [feat|fix|perf|chore|docs|refactor|test] | 🔼 **Version:** [MAJOR|MINOR|PATCH|none] | 🎫 **Ticket:** torqlab/torq#[board_id]_[ticket_id]

**Scope:** [scope from commits, or "general"]
**Breaking Changes:** [yes/no - detail if yes]
**Commits:** [X commits analyzed]

---

## Summary of Changes

[Extracted from commit messages and bodies]

---

📚 **Learn More:** See the [semantic-release skill](/semantic-release) for commit formatting rules and automated release workflow details.
```

#### Agent Workflow

1. **Get commits between head and base:**
   ```bash
   git log base..head --format="%H %s %b"
   ```

2. **Extract from commits:**
   - **Type:** From first commit (e.g., `feat`, `fix`, `perf`)
   - **Scope:** From commit scopes (e.g., `api`, `auth`)
   - **Ticket ID:** Extract board_id and ticket_id from branch name (e.g., `3_106`)
   - **Breaking changes:** Check for `BREAKING CHANGE:` in commit bodies
   - **Version bump:** Apply semantic-release rules (see section 3 in semantic-release skill)

3. **Extract summary of changes:**
   - Take commit subjects and bodies
   - Group by type (Features, Fixes, Performance, etc.)
   - Format as bullet list
   - Example:
     ```markdown
     ## Summary of Changes
     
     ### Features
     - Add rate limiting support for API endpoints
     - Add configuration options for max requests per window
     
     ### Tests
     - Add rate limiting tests for backoff behavior
     ```

4. **Fill template with extracted data**

5. **No manual description needed** — Body is deterministic from commits only


### 8. Agent Validates PR Parameters

Before requesting human approval, agent must verify all prerequisites.

#### Validation Checklist

Agent checks ALL of these:

1. **Branch parameters:**
   - ✅ `head` branch exists and is different from `base`
   - ✅ `base` branch exists (usually `main`)
   - ✅ Head branch matches semantic-release pattern: `<type>/<board_id>_<ticket_id>-<description>`
   - ✅ Both board_id and ticket_id are numeric

2. **Commits:**
   - ✅ All commits follow conventional format: `<type>(<scope>, #<board_id>_<ticket_id>): <description>`
   - ✅ Both board_id and ticket_id found in branch name
   - ✅ All commits include ticket reference `#board_id_ticket_id` in scope or footer: `Closes torqlab/torq#board_id_ticket_id`
   - ✅ At least one commit is version-impacting (feat/fix/perf) OR no-bump acknowledged

3. **GitHub issue:**
   - ✅ GitHub issue exists (use fully qualified reference: torqlab/torq#board_id_ticket_id)
   - ✅ Can fetch issue title and details

**If validation fails:**

Agent stops and reports which check failed:

```
❌ Validation failed

Issue:
- Branch format incorrect or commits don't reference both board_id and ticket_id
- Examples of violations:
  - "feat/55-thing" (missing board_id, should be "feat/3_55-thing")
  - "fix: bug #42" (missing board_id and incorrect footer format, should be "Closes torqlab/torq#3_42")
  - Commits lack ticket ID in scope or footer

Action:
1. Fix branch name or commits to include both board_id and ticket_id
2. Try PR creation again
```

Agent does NOT proceed to approval gate until all validations pass.

### 9. Agent Requests Explicit Human Approval

**CRITICAL RULE:** Agent must NEVER create PR without explicit human approval.

After validation passes, agent must show human a summary and wait for approval.

#### Step 1: Build PR preview

Agent compiles:
- Ticket ID and title (from GitHub issue)
- Branch names (head → base)
- Commit list (from `git log`)
- Version bump prediction (from semantic-release analysis)
- PR body (generated in section 7)

#### Step 2: Show human the PR summary

```
📋 PULL REQUEST PREVIEW

Title: <ticket-id> <ticket-title>
From: <head-branch> → <base-branch>
Draft: Yes (requires manual "Ready for review")

Semantic Release Impact:
- Type: <type>
- Version Bump: <MAJOR|MINOR|PATCH|none>
- Ticket: #<ticket-id>
- Commits: <count>

Commits to include:
- <commit-1>
- <commit-2>
- <commit-3>

PR body preview:
<first 300 chars of body>
...

[Full body shown in separate section]
```

#### Step 3: Agent requests approval

```
Ready to create this PR? (yes/no/edit)
```

**Agent must accept:**
- Simple answers: `yes` or `no`
- Inline edits: `yes, but change title to "..."` or `no, fix X first`

**If human says `yes`:**
- ✅ Proceed to section 10 (PR Creation)

**If human says `no`:**
- ❌ Ask: "What would you like to change?"
- Wait for human feedback
- Show preview again after changes

**If human provides edits inline:**
- Parse the request (change title, fix scope, etc.)
- Apply changes to PR data
- Show updated preview
- Ask for final approval

### 10. Apply Parameter Defaults

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
1. Get current branch: `feat/3_106-query-athlete`
2. Extract type: `feat`, board_id: `3`, ticket: `106`
3. Fetch GitHub issue torqlab/torq#3_106 title: "Query Athlete Data"
4. Analyze commits between branch and main
5. Detect version bump: MINOR
6. Use defaults: `owner=torqlab`, `repo=torq`, `base=main`
7. Create PR with title: `3-106 Query Athlete Data`
8. Add semantic impact section to body with fully qualified ticket reference
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
  --head="feat/3_106-query-athlete" \
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
- Title: 3-106 Query Athlete Data
- Status: Draft
- From: feat/3_106-query-athlete → main

Semantic Release Info:
- Type: feat
- Version Bump: MINOR
- Ticket: torqlab/torq#3_106
- Commits: 3

Next steps: Review, request changes, or mark as "Ready for review".
```

---

## Real-World Scenarios

### Scenario 1: Feature with Issue Reference

**Branch:** `feat/3_106-add-rate-limiting`
**Commits:**
```
feat(api, #3_106): add rate limiting support
test(api, #3_106): add rate limiting tests
```
**GitHub Issue torqlab/torq#3_106:** "Add Rate Limiting to API"

**PR Created:**
- Title: `3-106 Add Rate Limiting to API`
- Semantic Impact: MINOR bump (feat detected)
- Body includes ticket reference: torqlab/torq#3_106

### Scenario 2: Bug Fix

**Branch:** `fix/1_42-resolve-race-condition`
**Commits:**
```
fix(db, #1_42): resolve race condition in cache
```
**GitHub Issue torqlab/torq#1_42:** "Fix Race Condition in Query Cache"

**PR Created:**
- Title: `1-42 Fix Race Condition in Query Cache`
- Semantic Impact: PATCH bump (fix detected)
- Body highlights that this is a bug fix with no new features

### Scenario 3: Breaking Change

**Branch:** `feat/2_99-redesign-response`
**Commits:**
```
feat!(api, #2_99): redesign API response structure

BREAKING CHANGE: response format changed from XML to JSON
```
**GitHub Issue torqlab/torq#2_99:** "Redesign API Response Format"

**PR Created:**
- Title: `2-99 Redesign API Response Format`
- Semantic Impact: MAJOR bump (breaking change detected)
- Body highlights breaking change and migration requirements

---

## Validation Reference

### Valid Branch Names
- ✅ `feat/3_106-add-feature`
- ✅ `fix/1_42-resolve-bug`
- ✅ `perf/2_99-optimize-db`
- ✅ `chore/4_123-update-deps`
- ✅ `docs/5_88-add-guide`
- ✅ `refactor/1_77-simplify-logic`
- ✅ `test/3_66-add-coverage`

### Invalid Branch Names
- ❌ `feature/add-something` (missing board_id, ticket_id and type)
- ❌ `55-add-feature` (missing board_id, ticket_id and type prefix)
- ❌ `feat/55-add-feature` (missing board_id)
- ❌ `feat-3-106-add-feature` (invalid format)
- ❌ `my-random-branch` (no semantic info)

### Valid Commit Messages
```
feat(api, #3_106): add rate limiting support

Implements exponential backoff for API rate limits.

Closes torqlab/torq#3_106
```

```
fix(db, #1_42): resolve race condition

Fixes concurrent cache update issue.

Closes torqlab/torq#1_42
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
fix: resolve bug #42                  ❌ (incomplete ticket format, should be #1_42)
fix(db, #42): bug fix                 ❌ (missing board_id in ticket reference)
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

- **Branch Convention Required:** Branch must follow `<type>/<board_id>_<ticket_id>-<description>` pattern
  - Enables automatic board_id and ticket_id extraction
  - Aligns with semantic-release conventions
  - Both IDs required for multi-board project structure
  - If invalid, skill provides guidance on fixing

- **Commits Must Be Conventional:** All commits must follow `<type>(<scope>, #<board_id>_<ticket_id>): <subject>` format
  - semantic-release depends on this for version detection
  - Skill validates and warns if format is incorrect
  - Prevents broken releases from malformed commits
  - Ticket reference in footer must be fully qualified: `Closes torqlab/torq#board_id_ticket_id`

- **Ticket ID Mandatory (Both Parts):** Branch must contain both board_id and ticket_id
  - Used to fetch GitHub issue title from multi-board system
  - Links commits to requirements across project boards
  - Enables automatic issue closing via fully qualified footer
  - Composite ID ensures proper ticket tracking in complex organization

- **Draft Mode Always:** PRs created as draft by default
  - Signals agent-generated content needs review
  - Prevents accidental merge before human approval
  - Requires explicit "Ready for review" action

- **Validation Matters:** Skill validates branch naming and commit format upfront
  - Catches issues before PR creation
  - Prevents failed releases post-merge
  - Enforces multi-board ticket format consistency
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