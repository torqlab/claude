---
name: git-branch
description: |
  Create git branches with semantic-release naming conventions for the current repository. Use this skill whenever: user asks to create a git branch (e.g., "create a branch for issue #55"), user needs to create a feature/bug/chore branch with proper naming, user wants branch names that follow type/ticket_id-description format, or user needs GitHub issue validation and branch creation. This skill guides you through: obtaining the ticket ID, validating GitHub issue existence in the current repository, determining commit type from issue content, generating compliant branch names, and creating/pushing branches with proper naming. Scope: local branch creation and management only. For commits, use semantic-release skill. For PR operations, use PR skill.
compatibility: "git, gh CLI, GitHub API"
---

## Overview

This skill creates git branches with semantic-release naming conventions for issues in the current repository. It handles issue validation, branch name generation, and branch creation with a clear validation workflow.

**Key principle:** Branch names encode ticket metadata (`ticket_id`), making it easy to trace commits back to GitHub issues in the current repository.

---

## Branch Naming Convention

All branches follow this format:

```
<type>/<ticket_id>-<description>
```

| Component | Example | Notes |
|-----------|---------|-------|
| `type` | `feat`, `fix`, `chore` | Inferred from GitHub issue content |
| `ticket_id` | `106` | Numeric identifier for issue (required) |
| `description` | `query-athlete` | 2-5 words from issue title, lowercase, hyphens for spaces |

**Examples:**
- `feat/106-query-athlete` — Feature branch for issue #106
- `fix/42-race-condition` — Bug fix for issue #42
- `chore/123-upgrade-deps` — Maintenance for issue #123

The `ticket_id` uniquely identifies the GitHub issue in the current repository.

---

## Branch Creation Workflow

### Step 1: Obtain Ticket ID

Agent must collect the ticket ID from the user. This is mandatory.

**If user provides ID directly:** `106` → Use as ticket_id
**If user provides with hash:** `#106` → Strip hash and use `106`
**If user doesn't provide:** Ask for the numeric ticket ID

```
❓ Agent asks: "What is the GitHub issue ID? (numeric)"
```

---

### Step 2: Validate GitHub Issue in Current Repository

The ticket MUST exist in the current repository. Agent validates it exists locally.

#### Search Strategy

**Always search the current repository:**
```bash
# Get current repository from git config
REPO=$(git config --get remote.origin.url | sed 's/.*://;s/\.git$//')

# Validate issue exists in current repo
gh issue view <ticket_id> --json number,title,body
```

**If issue NOT found:**

```
❌ GitHub issue #55 not found in this repository

Please verify:
1. Issue ID is correct (numeric)
2. The issue exists in the current repository

Create or verify the GitHub issue first, then come back with the correct ID.
```

Stop. No branch creation proceeds.

**If issue found:**

Extract and store:
- Issue `number`
- Issue `title`
- Issue `body`

Continue to step 3.

---

### Step 3: Determine Commit Type from Issue

Analyze the **resolved GitHub issue** title and description to infer the commit type. The issue's actual content is the source of truth.

| Type | Keywords | Example |
|------|----------|---------|
| `feat` | add, implement, enable, support, new | "Add rate limiting to API" |
| `fix` | fix, resolve, correct, bug, issue | "Fix race condition in cache" |
| `perf` | optimize, speed up, improve performance, faster | "Optimize database queries" |
| `chore` | update, upgrade, deps, maintenance, remove, deprecate | "Upgrade dependencies" or "Remove legacy API" |
| `docs` | document, guide, README, docs | "Add API documentation" |
| `refactor` | refactor, restructure, simplify, improve code | "Simplify authentication logic" |
| `test` | test, add coverage, add tests | "Add unit tests for rate limiter" |

**Important:** Type is inferred from the actual GitHub issue content, not from the user's task description.

**If type is ambiguous, ask human:**

```
Based on the GitHub issue title and description, is this a:
  a) feat (new feature)
  b) fix (bug fix)
  c) chore (maintenance/removal)
  d) perf (performance)
  e) docs (documentation)
  f) refactor (code refactoring)
  g) test (test additions)
```

---

### Step 4: Generate and Confirm Branch Name

**Format:** `<type>/<ticket_id>-<description>`

Agent generates suggested branch name from issue:
1. Extract short description from issue title (2-5 words)
2. Convert to lowercase, hyphens for spaces
3. Combine with type and ID: `<type>/<ticket_id>-<short-description>`

**Example:**

```
Issue #106: "Query Athlete Data from Strava API"
Inferred type: feat
Ticket ID: 106
Suggested branch: feat/106-query-athlete

Is this correct? (yes/no/custom)
```

**Validation:**

- ✅ If human says **yes** → Continue to step 5
- ❌ If human says **no** → Ask for custom branch name
  - Validate format: `<type>/<ticket_id>-<description>`
  - ticket_id must be numeric
  - If invalid → Explain issue and ask to reformat
- If human provides **custom** → Validate format and use it

---

### Step 5: Create and Push Branch

Once approved, create the branch from main:

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

**Why base on `main`?** Ensures your branch includes all latest changes and release commits, preventing conflicts when integrated.

---

## Examples

### Feature Branch

```
User: "Create a branch for issue #106 — Query Athlete Data from Strava API"

Agent resolves ticket → Found #106 in current repo
Agent infers type → feat (keywords: "Query", "Data")
Agent generates → feat/106-query-athlete
Agent creates → ✅ Branch created
```

### Bug Fix

```
User: "I'm working on the fix for issue #42"

Agent resolves #42 → Found in current repo
Agent infers type → fix (keywords: "Fix", "bug", "race condition")
Agent generates → fix/42-race-condition
Agent creates → ✅ Branch created
```

### Maintenance Task

```
User: "Create a branch for ticket 123 — upgrade dependencies"

Agent resolves ticket_id=123
Agent searches → Found #123 in current repo
Agent infers type → chore (keywords: "upgrade", "dependencies")
Agent generates → chore/123-upgrade-deps
Agent creates → ✅ Branch created
```

---

## Important Notes

- **Ticket ID Required:** ticket_id is mandatory for proper tracking. Never create a branch without it.
- **Ticket Must Exist:** GitHub issue must exist in the current repository. Verify before proceeding.
- **Current Repository Only:** Issues are always resolved from the current repository only. No cross-repository searching.
- **Format Validation:** Branch names must follow the strict format. Numeric IDs are required; hyphens in descriptions are mandatory.
- **One Branch Per Request:** Create one branch at a time. If user needs multiple branches, run this workflow multiple times.

---

## Future Enhancements (Progressive Disclosure)

This skill currently handles branch creation only. Future versions will add:
- **Branch deletion:** Remove local and remote branches safely
- **Branch switching:** Switch between branches with validation
- **Branch listing:** List branches with ticket metadata
- **Branch cleanup:** Bulk operations on stale branches

For now, use standard git commands for these operations.
