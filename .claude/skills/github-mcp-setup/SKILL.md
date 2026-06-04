---
name: github-mcp-setup
description: Configure GitHub Model Context Protocol (MCP) server for Claude Code using GitHub App authentication. Use when setting up Claude Code to integrate with GitHub repositories for code review, PR management, issue tracking, or other GitHub automation tasks. Provides complete setup workflow from GitHub App creation through configuration in Claude Code projects.
license: MIT
metadata:
  author: Mr.B.Lab
---

# GitHub MCP Configuration

## Overview

This skill guides you through configuring GitHub MCP (Model Context Protocol) for Claude Code using GitHub App-based authentication. Unlike Personal Access Tokens (PATs), GitHub Apps provide fine-grained permissions, better security, and cleaner audit trails. This configuration enables Claude to read repository data, manage PRs, track issues, and automate GitHub workflows.

## Setup Workflow

Follow these steps sequentially to configure GitHub MCP in any repository.

### Step 1: Create a GitHub App

1. Go to [GitHub App settings](https://github.com/settings/apps) (Settings → Developer settings → GitHub Apps)
2. Click **New GitHub App**
3. Fill in the form:
   - **App name**: Choose a descriptive name (e.g., `claude-code-automation`, `repo-name-mcp`)
   - **Homepage URL**: Can be your repo URL or a placeholder like `https://example.com`
   - **Webhook URL**: Leave blank (Claude Code doesn't use webhooks)
   - **Webhook active**: Uncheck this
4. Leave other fields at defaults and click **Create GitHub App**

### Step 2: Configure Permissions

After creating the app, navigate to its settings page and configure permissions. The exact permissions depend on your use case, but for general GitHub operations, set read/write permissions on:

- **Repository**: Contents (read), Pull requests (read/write), Issues (read/write), Discussions (read)
- **Account**: Email (read)

Adjust permissions based on what operations you need (for example, if only reading code, set Contents to read-only).

### Step 3: Generate and Store Credentials

On the app settings page:

1. **App ID**: Copy from the "About" section at the top
2. **Private Key**: Scroll to "Private keys" → **Generate private key**. A PEM file downloads — save it securely in your project as `.github/app-private-key.pem`
3. **Installation ID**: Go to app settings → **Install App** → choose your user/org → confirm. After installation, the URL will contain the installation ID (e.g., `https://github.com/settings/installations/12345678`)

### Step 4: Configure Environment Variables

Add credentials to your `.env` file:

```env
GITHUB_APP_ID=<app-id>
GITHUB_APP_PRIVATE_KEY_PATH=.github/app-private-key.pem
GITHUB_INSTALLATION_ID=<installation-id>
```

**Security**: Add `.github/app-private-key.pem` to `.gitignore` to prevent credentials from being committed. The environment variables point to the key file rather than embedding the key itself.

### Step 5: Configure .mcp.json

Create or update `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "env": {
        "GITHUB_APP_ID": "${GITHUB_APP_ID}",
        "GITHUB_APP_PRIVATE_KEY_PATH": "${GITHUB_APP_PRIVATE_KEY_PATH}",
        "GITHUB_INSTALLATION_ID": "${GITHUB_INSTALLATION_ID}"
      }
    }
  }
}
```

The `env` block references your `.env` variables using `${VARIABLE_NAME}` syntax — Claude Code will substitute them at runtime.

### Step 6: Restart Claude Code

After configuration, restart Claude Code or reload the project. The GitHub MCP server should now be available for Claude to use. Verify by running a GitHub-related task (e.g., asking Claude to review a PR or fetch issue details).

## Common Use Cases

**Code Review**: Claude analyzes PR diffs and provides review comments
**Issue Automation**: Claude reads issues and creates related PRs or draft solutions  
**Repository Management**: Claude queries repo metadata, commits, and branch info
**Workflow Automation**: Claude orchestrates multi-step GitHub operations (create PR → add labels → request reviewers)

## Troubleshooting

### Authentication Fails

**Problem**: MCP server errors with auth failures  
**Solution**: Verify `.env` values match exactly. Check that `.github/app-private-key.pem` exists and is readable. Confirm Installation ID is correct (it's numeric and found in installation settings).

### Insufficient Permissions

**Problem**: Claude requests fail with permission errors  
**Solution**: Return to GitHub App settings and verify the app has required permissions. Permissions must be granted at the app level (not individual repos). After changing permissions, you may need to reinstall the app.

### Connection Issues

**Problem**: MCP server won't connect  
**Solution**: Confirm `.mcp.json` syntax is valid JSON. Check that the URL `https://api.githubcopilot.com/mcp/` is accessible from your network. Restart Claude Code after making configuration changes.

## Next Steps

After setup, use your configured GitHub MCP server by asking Claude Code to perform GitHub tasks:
- "Review this PR for security issues"
- "Create a GitHub issue for this bug"
- "Check the status of recent commits"

For more details on GitHub App permissions and capabilities, see the [GitHub App documentation](https://docs.github.com/en/apps).
