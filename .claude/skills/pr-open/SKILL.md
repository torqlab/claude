---
name: pr-open
description: Creates a pull request on GitHub by reading the latest changelog entry. All parameters optional with smart defaults. Validates current branch matches ticket ID. Extracts ticket ID and description from CHANGELOG.md and formats the PR with proper "# Changelog" header.
argument-hint: "[--head] [--base] [--owner] [--repo]"
license: MIT
metadata:
  author: Mr.B.Lab
---

# Open Pull Request Skill

## Context

You are a GitHub automation assistant specialized in creating pull requests directly from changelog entries. This skill provides a consistent, changelog-driven interface for PR creation that can be invoked directly by users or orchestrated by other skills (like `plan-ticket-implementation`).

The skill reads the latest changelog entry from CHANGELOG.md, extracts ticket information, and creates a PR with proper formatting: the PR title and description are derived from the changelog to ensure consistency between changelog and PR documentation.

## Task

- Read the latest changelog entry from CHANGELOG.md
- Extract ticket ID, title, and description from the changelog
- Determine current git branch automatically
- Validate that current branch matches the ticket (ID and title)
- Apply meaningful defaults for all parameters (99% use case defaults)
- Format PR body with "# Changelog" header followed by the changelog entry
- Create the PR using GitHub MCP tools
- Handle common GitHub errors gracefully
- Return PR metadata (URL, number, status)

## Instructions

### 1. Get Current Git Branch

Automatically determine the current working branch:

```bash
git branch --show-current
```

**Example output**: `feat/0-ticket-flow`

This becomes the default source branch (`head`) for the PR.

### 2. Read Latest Changelog Entry

Read `CHANGELOG.md` and extract the most recent entry:

```bash
cat CHANGELOG.md | head -50
```

Parse the entry to extract:
- **Ticket ID**: From the section heading, e.g., `[<Ticket-ID> Title](url)` → extract the number
- **Ticket Title**: The full title from the heading
- **Changelog Body**: All content under the ticket heading (Added/Changed/Fixed/Removed/Security sections)

**Entry Format** (example):
```markdown
## [6.1.0] - 2026-03-31

### [0 Add Ticket Planning and Pull Request Creation Skills](https://github.com/torqlab/torq/issues/0)

### Added
- **open-pull-request skill** - Generic GitHub PR creation tool
  ...details...
```

Extract:
- Ticket ID: `0`
- Ticket Title: `Add Ticket Planning and Pull Request Creation Skills`
- Description: Everything under "### Added" onwards

### 3. Apply Parameter Defaults

Set defaults for all optional parameters (99% use case):
- **`head`**: Current git branch (from step 1)
  - Can be overridden: `--head="custom-branch"`
- **`base`**: `main` (default target branch)
  - Can be overridden: `--base="develop"`
- **`owner`**: `torqlab` (default GitHub organization)
  - Can be overridden: `--owner="other-org"`
- **`repo`**: `torq` (default repository)
  - Can be overridden: `--repo="other-repo"`

**All parameters are optional** - skill runs with sensible defaults.

### 4. Validate Branch Matches Ticket

Before creating the PR, verify that the current branch name is correct for this ticket:

**Validation Logic:**
1. Extract ticket ID from changelog (step 2)
2. Extract ticket title from changelog (step 2)
3. Get current branch name (step 1)
4. Check if current branch contains ticket ID:
   - Current branch: `feat/0-ticket-flow` → contains `0` ✅
   - Ticket ID: `0` → match ✅

**Valid branch patterns** (all acceptable):
- `plan/0-*` - Planning branch for ticket 0
- `feat/0-*` or `feature/0-*` - Feature branch for ticket 0
- `impl/0-*` or `implementation/0-*` - Implementation branch for ticket 0
- `fix/0-*` or `hotfix/0-*` - Hotfix branch for ticket 0
- `bugfix/0-*` - Bugfix branch for ticket 0

**Branch validation failure handling:**

If current branch does NOT contain the ticket ID:

```
❌ Branch Validation Failed

Current branch: my-random-branch
Changelog ticket: #0 - Add Ticket Planning and Pull Request Creation Skills

The current branch doesn't match the ticket from CHANGELOG.md.

Suggested branch name: feat/0-ticket-planning-pull-request-creation-skills

Would you like me to:
1. Suggest you create/switch to: feat/0-ticket-planning-pull-request-creation-skills
2. Continue anyway with current branch (not recommended)
3. Provide a different branch name

Enter choice (1/2/3) or provide custom branch name:
```

**Upon user confirmation**, proceed with the chosen branch.

### 5. Pre-Creation Checks

Before calling `gh_create_pull_request()`:
- Verify `head` branch differs from `base` branch
- Verify repository format is valid
- Show user a summary of what will be created:
  ```
  Creating PR from changelog entry:
  - Ticket: #[ID] - [Title]
  - Repository: [owner]/[repo]
  - From: [head] → [base]
  - Body: # Changelog\n\n[first 100 chars of changelog description]...
  ```

### 6. Construct PR Title and Body

**PR Title:**
Extract from changelog entry heading: `[Ticket-ID Title](issue-link)`
- Format: `[ID] Title` (e.g., `0 Add Ticket Planning and Pull Request Creation Skills`)

**PR Body:**
Format with "# Changelog" header as first line, followed by changelog entry content:
```markdown
# Changelog

### [ID Title](issue-link)

### Added
- item 1
- item 2

### Changed
- item 1
```

Ensure the "# Changelog" header appears on the first line of the body.

### 7. PR Creation

Call GitHub MCP `gh_create_pull_request()` with:
- `title`: Constructed from changelog entry: `[ID] Title`
- `body`: Body with "# Changelog" header + changelog entry content
- `head`: The source branch name (validated in step 4)
- `base`: The target branch (defaults to "main")
- `draft`: **true** (always create as draft PR to ensure careful review of agent-created content)

**Note**: GitHub MCP is currently scoped to `torqlab/torq`. For other organizations, manual setup may be required.

Draft mode ensures:
- PR signals it was created by an agent and needs careful review
- Prevents accidental merging before human approval
- Requires explicit conversion to "Ready for review" status

### 8. Error Handling

Handle these common GitHub errors:

#### 401 Unauthorized
- **Cause**: GitHub MCP token invalid or expired
- **Solution**: Inform user to check GITHUB_MCP_TOKEN in .env file
- **Message**: "Authentication failed. Verify GITHUB_MCP_TOKEN in .env is valid and not expired."

#### 403 Forbidden
- **Cause**: Token lacks PR creation permissions
- **Solution**: User needs to regenerate token with PR write permission
- **Message**: "Permission denied. Verify GitHub token has 'pull_requests:write' permission."

#### 404 Not Found
- **Cause**: Branch doesn't exist or repository not found
- **Solution**: List available branches or verify repo name
- **Message**: "Branch [branch-name] not found. Common branches: main, develop, release/*"

#### 409 Conflict
- **Cause**: Merge conflict between branches
- **Solution**: Suggest user resolve conflicts in the branch
- **Message**: "Merge conflict detected. Please resolve conflicts in [head] branch before creating PR."

#### 422 Unprocessable Entity
- **Cause**: Invalid parameters or duplicate PR
- **Solution**: Check if PR already exists or parameters are invalid
- **Message**: "Invalid parameters or PR already exists. Verify branch names and repository."

#### 429 Too Many Requests
- **Cause**: GitHub rate limit exceeded
- **Solution**: Wait before retrying
- **Message**: "Rate limit exceeded. Please wait a few minutes and try again."

### 9. Success Response

On successful PR creation, return:
```
✅ Pull request created successfully!

PR Details:
- URL: https://github.com/[owner]/[repo]/pull/[number]
- Number: #[number]
- Title: [title]
- Status: Open
- From: [head] → [base]

Next steps: Review, request changes, or merge when ready.
```

## Usage Examples

### Simplest Invocation (99% use case)

**Just run with no parameters:**

```
/open-pull-request
```

The skill will:
1. Get current branch (e.g., `feat/0-ticket-flow`)
2. Read CHANGELOG.md
3. Extract latest entry: #0 - Add Ticket Planning and Pull Request Creation Skills
4. Validate current branch contains ticket ID `0` ✅
5. Use defaults: `owner=torqlab`, `repo=torq`, `base=main`
6. Create PR with title: `0 Add Ticket Planning and Pull Request Creation Skills`
7. Format body with "# Changelog" header + changelog entry
8. Create PR on GitHub and return URL

### With Custom Base Branch

```
/open-pull-request --base="develop"
```

Uses current branch as `head`, everything else as defaults. Useful for PRs against non-main branches.

### With All Explicit Parameters

```
/open-pull-request \
  --head="hotfix/0-urgent-fix" \
  --base="release/1.0" \
  --owner="torqlab" \
  --repo="torq"
```

Overrides all defaults explicitly.

### Branch Validation in Action

**Scenario:** You're on branch `my-random-feature`

```
/open-pull-request

❌ Branch Validation Failed

Current branch: my-random-feature
Changelog ticket: #0 - Add Ticket Planning and Pull Request Creation Skills

The current branch doesn't match the ticket from CHANGELOG.md.

Suggested branch name: feat/0-ticket-planning-pull-request-creation-skills

Would you like me to:
1. Suggest you create/switch to: feat/0-ticket-planning-pull-request-creation-skills
2. Continue anyway with current branch (not recommended)
3. Provide a different branch name

Enter choice (1/2/3) or provide custom branch name: 1

✅ Suggestion accepted!

Next step: Create and switch to the branch:
  git checkout -b feat/0-ticket-planning-pull-request-creation-skills
  git push -u origin feat/0-ticket-planning-pull-request-creation-skills

Then run /open-pull-request again to create the PR.
```

### Programmatic Invocation (from other skills)

From `plan-ticket-implementation` skill:

```
1. After generating changelog entry on current branch

2. Invoke skill with only custom parameters if needed:
   /open-pull-request --base="main"

3. All defaults applied automatically:
   - head: current branch (from git)
   - owner: "torqlab"
   - repo: "torq"

4. Skill reads CHANGELOG.md

5. Validates branch name matches ticket

6. Extracts latest entry and creates PR

7. Returns PR metadata (URL, number, status)
```

## Default Parameter Reference

| Parameter | Default | Override |
|-----------|---------|----------|
| `head` | Current git branch | `--head="branch-name"` |
| `base` | `main` | `--base="develop"` |
| `owner` | `torqlab` | `--owner="other-org"` |
| `repo` | `torq` | `--repo="other-repo"` |

**99% Use Case:** Just run `/open-pull-request` with no parameters from your feature branch.

## Integration Points

### GitHub MCP Tools

The skill uses:
- `gh_create_pull_request(title, body, head, base, draft)` - Creates PR
- Error handling for rate limits and conflicts

### Used By

This skill can be invoked by:
- Users directly via `/open-pull-request` command
- `plan-ticket-implementation` skill - for creating plan PRs
- Other workflow automation skills

### Project Conventions

Follows TORQ conventions:
- Arrow functions and const (internal implementation)
- No nested functions
- JSDoc for all functions (internal)
- Proper error handling and messaging

## Common Scenarios

### Scenario 1: User Creates PR Manually
1. User runs `/open-pull-request` with all parameters
2. Skill validates parameters
3. Displays confirmation summary
4. Creates PR on GitHub
5. Returns PR URL to user

### Scenario 2: Orchestrated PR Creation
1. `plan-ticket-implementation` skill calls `open-pull-request`
2. Parameters prepared from issue/changelog context
3. Skill creates PR silently (no user confirmation needed)
4. Returns PR metadata for further processing

### Scenario 3: Error Recovery
1. PR creation fails (e.g., branch conflict)
2. Skill catches error and reports specific issue
3. Provides guidance on resolving the issue
4. Offers option to retry or adjust parameters

## Important Notes

- **All Parameters Optional**: The skill is designed for 99% use case where you just run `/open-pull-request` with no parameters
  - Current git branch is used automatically as source branch
  - Defaults: `base=main`, `owner=torqlab`, `repo=torq`
  - Override any default by providing parameter: `--base="develop"`

- **Changelog Required**: The skill reads CHANGELOG.md from the current working directory (repository root)
  - CHANGELOG.md must exist and contain at least one entry
  - Latest entry is extracted and used for PR title and body
  - Entry format must follow Keep a Changelog standard with `### [ID Title](url)` heading

- **Branch Validation**: Current branch is validated against ticket ID from changelog
  - Current branch must contain the ticket ID (e.g., branch `feat/0-fix` contains ticket ID `0`)
  - Branch should follow patterns: `plan/*`, `feat/*`, `impl/*`, `fix/*`, `hotfix/*`, `bugfix/*`
  - If validation fails, skill suggests correct branch name and asks for user approval
  - User can create/switch to suggested branch or override with different branch name

- **Repository Scope**: GitHub MCP is currently scoped to `torqlab/torq` repository
  - The skill accepts `owner` and `repo` parameters for future extensibility
  - Currently only `torqlab/torq` is supported via GitHub MCP

- **Branch Requirements**: Both `head` and `base` branches must exist in the repository before creating the PR

- **PR Body Format**: Automatically prefixed with `# Changelog` on the first line
  - Followed by the full changelog entry from CHANGELOG.md
  - Supports full GitHub Flavored Markdown (GFM)

- **Draft PRs**: Always created in draft mode (`draft: true`)
  - Signals to reviewers that content was agent-generated
  - Prevents accidental merging before human review
  - Requires explicit "Ready for review" conversion to enable merging

- **Permissions**: Requires GitHub token with `pull_requests:write` permission (fine-grained token recommended)

## Rate Limiting

GitHub API has rate limits:
- Standard: 5,000 requests per hour per user
- PR creation counts as 1 request

If rate limited (429 error), wait 1 hour for reset or check your quota with GitHub settings.

## Success Criteria

The skill successfully creates a PR when:
- ✅ CHANGELOG.md exists and contains at least one entry
- ✅ Latest changelog entry is properly formatted with `### [ID Title](url)` heading
- ✅ Current git branch is obtained successfully
- ✅ Current branch matches ticket ID from changelog (branch contains ID, e.g., `feat/0-*` for ticket 0)
- ✅ User approves branch name if validation required
- ✅ Optional parameters provided and validated (all have defaults)
- ✅ GitHub MCP token is valid and has correct permissions
- ✅ Both `head` and `base` branches exist
- ✅ No merge conflicts between branches
- ✅ PR doesn't already exist
- ✅ GitHub API responds successfully
- ✅ PR is created in draft mode
- ✅ PR body starts with "# Changelog" followed by changelog entry

If any condition fails, the skill provides clear error message and guidance on resolution.