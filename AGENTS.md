# AGENTS.md — Claude Configuration Collection Guide

This guide explains how to use this Claude configuration collection and documents all available agents (Claude instances specialized for different tasks).

## 🔍 Maintainer Information

**Maintainer & Author**: Mr.B.Lab  
**Repository**: @torqlab/claude  
**License**: MIT  

This collection is maintained exclusively by Mr.B.Lab. All documentation, skills, hooks, and conventions are authored and maintained by Mr.B.Lab.

## Quick Links

- **README.md** - Project overview, skills table, installation guide
- **For agents**: See "Available Agents" section below
- **For skills**: See README.md skills table
- **For rules**: `./.claude/rules/` directory

## What This Repository Contains

**TORQ Claude** is a shared collection of:

1. **Custom Skills** (`./.claude/skills/`) - Specialized tools for GitHub automation, changelog generation, UI design, and skill development
2. **Open-Source Skills** (`skills-lock.json`) - Pre-built skills from Anthropic's skill library
3. **Development Hooks** (`./.claude/hooks/`) - Automated quality checks during development
4. **Project Rules** (`./.claude/rules/`) - Coding conventions and workflows

Every TORQ repository uses this collection via a **symlink to `.claude/`**, ensuring consistency across all projects.

## Repository Purpose

Provide a **centralized, reusable collection** of Claude development configurations that:
- Standardize AI-driven workflows across TORQ repositories
- Reduce duplication of skills, hooks, and conventions
- Enable consistent code generation and automation practices
- Support specialized development workflows (changelog generation, PR automation, UI design)

## Installation: Adding This Collection to Your Project

### For a New Project

```bash
# From your-torq-repo/ directory
ln -s ../claude/.claude .claude

# Verify it works
ls -l .claude
# Output: .claude -> ../claude/.claude
```

### For an Existing Project

If your project already has a `.claude/` directory:

```bash
# Backup existing configuration
mv .claude .claude.backup

# Create symlink to shared collection
ln -s ../claude/.claude .claude

# Merge important configs if needed
cat .claude.backup/settings.json | jq . > /tmp/backup.json
# Review and manually merge if necessary
```

### Gitignore Configuration

Add `.claude` to `.gitignore` **if not already there**:

```gitignore
# Claude Code
.claude
```

Since `.claude` is symlinked, it shouldn't be committed. If you want to track the symlink itself (recommended for teams), you can commit it:

```bash
git add .claude
git commit -m "Add Claude configuration collection via symlink"
```

Git automatically tracks symlinks correctly.

## Available Agents

Claude Code supports multiple specialized "agents" — Claude instances configured for specific tasks. All agents are organized in the table below:

### Core Agents

| Agent | Role | When to Use | Trigger |
|-------|------|-----------|---------|
| **General Purpose Agent** | Default agent for exploring code, understanding architecture, and answering questions | Open-ended questions, codebase exploration, debugging | Automatic (default for exploratory tasks) |
| **Explore Agent** | Fast agent specialized in finding files by pattern and searching code | Find files matching glob patterns, search keywords across codebase | Use Glob/Grep tools or ask exploratory questions |
| **Plan Agent** | Software architect for designing implementation strategies | Planning new features, architecture decisions, multi-step implementations | Use `EnterPlanMode` for complex implementation tasks |
| **Claude Code Guide Agent** | Expert on Claude Code features, CLI, API, and Anthropic SDK | Questions about Claude Code, API usage, prompt caching, model versions | Auto-triggered for "Can Claude...", "How do I...", "Does Claude..." questions |
| **Security Review Agent** | Specialized security review for pending code changes | Run before merging sensitive code (auth, payments, data handling) | Use `/security-review` skill |
| **Skill Creator Agent** | Develop new Claude skills from scratch or improve existing ones | Building and testing new skills | Use `/skill-creator` skill |

## Using Specialized Agents

### With Plan Mode (For Complex Implementation)

```bash
# Start planning mode
/plan

# Or use EnterPlanMode in code to trigger architecture planning
```

The plan agent will:
1. Explore relevant code files
2. Understand existing patterns
3. Design implementation approach
4. Present options for your approval
5. Provide step-by-step plan before coding starts

### With Skill Creator (For Building Skills)

```bash
/skill-creator
```

This interactive workflow helps:
1. Define what the skill should do
2. Write initial draft
3. Create and run test cases
4. Evaluate results with metrics
5. Iterate until production-ready
6. Optimize triggering description

### With Security Review (For Sensitive Changes)

```bash
/security-review
```

Runs comprehensive security analysis:
- OWASP vulnerability checks
- Authentication & authorization review
- Data handling & privacy checks
- Dependency security audit
- API security analysis

## Custom Project-Specific Skills

| Skill | Purpose | Usage | Location |
|-------|---------|-------|----------|
| **pr-open** | Create pull requests on GitHub from changelog entries with branch validation | `/pr-open` | [./.claude/skills/pr-open/SKILL.md](./.claude/skills/pr-open/SKILL.md) |
| **create-changelog** | Generate accurate changelog entries following Keep a Changelog standard | `/create-changelog` | [./.claude/skills/create-changelog/SKILL.md](./.claude/skills/create-changelog/SKILL.md) |
| **github-mcp-setup** | Configure GitHub MCP with GitHub App authentication | `/github-mcp-setup` | [./.claude/skills/github-mcp-setup/SKILL.md](./.claude/skills/github-mcp-setup/SKILL.md) |
| **frontend-design** | Build distinctive, production-grade UI components | `/frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) |
| **skill-creator** | Create, test, and iteratively improve new Claude skills | `/skill-creator` | [anthropics/skills](https://github.com/anthropics/skills) |

## Custom Skills Details

### 1. **pr-open** — Create Pull Requests
**Location**: `./.claude/skills/pr-open/SKILL.md`  
**Purpose**: Automate PR creation from changelog entries with branch validation  
**Usage**: `/pr-open` (or `--base="develop"` to override defaults)  
**Features**:
- Reads latest changelog entry
- Validates branch matches ticket ID
- Creates draft PR with formatted body
- Smart defaults: current branch, main base, torqlab/torq repo

### 2. **create-changelog** — Generate Changelog Entries
**Location**: `./.claude/skills/create-changelog/SKILL.md`  
**Purpose**: Create accurate changelog entries from git diffs (Keep a Changelog standard)  
**Usage**: `/create-changelog`  
**Features**:
- Analyzes branch diffs vs. main
- Categorizes changes (Added/Changed/Fixed/Removed/Security)
- Extracts ticket ID from branch name
- Generates SemVer version
- Updates CHANGELOG.md and package.json

### 3. **github-mcp-setup** — Configure GitHub Integration
**Location**: `./.claude/skills/github-mcp-setup/SKILL.md`  
**Purpose**: Complete setup workflow for GitHub MCP with GitHub App auth  
**Usage**: `/github-mcp-setup`  
**Covers**:
- Create GitHub App with fine-grained permissions
- Generate and store credentials
- Configure .mcp.json for your project
- Troubleshoot connection issues

### 4. **skill-creator** — Build New Skills
**Location**: `./.claude/skills/skill-creator/SKILL.md`  
**Purpose**: Full workflow for creating and improving Claude skills  
**Usage**: `/skill-creator`
**Workflow**:
1. Interview about skill purpose & use cases
2. Write initial SKILL.md draft
3. Create test cases
4. Run skill through test prompts
5. Evaluate with metrics
6. Iterate based on feedback
7. Optimize description for better triggering

### 5. **frontend-design** — Build Production UIs
**Location**: Open-source from anthropics/skills
**Purpose**: Create distinctive, production-grade frontend interfaces  
**Usage**: `/frontend-design`  
**Covers**:
- UI component design with aesthetic direction
- Production-grade HTML/CSS/React code
- Typography, colors, animations, layouts
- Avoids generic "AI aesthetic"

## Project Conventions

This collection recommends consistent development practices:

**Code Standards**:
- ✅ `const` for variable declarations
- ✅ Arrow functions: `const fn = () => {}`
- ✅ Clear function naming
- ✅ Modular code structure

**Quality Checks**:
- Write clear, testable code
- Document complex logic
- Test before merging
- Use agent skills for code review when needed

## How to Update This README

This README serves as the main documentation for agents and skills. When updating:

1. **Update the skills table** when adding/removing skills
2. **Document new agents** in the "Available Agents" section
3. **Keep installation steps** clear and accurate
4. **Link to skill SKILL.md files** for detailed documentation
5. **Explain purpose** of the collection in the first section

**For agents**: This document explains what agents are available and when to use them. Detailed agent instructions are in individual SKILL.md files or project rules.

## Referencing This Collection in Other Projects

### Symlink Pattern

```bash
# From any TORQ repository
ln -s ../claude/.claude .claude

# Verify
ls -l .claude
# Output: .claude -> ../claude/.claude
```

This single symlink gives you:
- ✅ All custom skills
- ✅ All agent skills plugins
- ✅ Settings and configurations

### No Additional Setup

Once the symlink is created, Claude Code automatically:
1. Discovers all skills from `./.claude/skills/`
2. Loads open-source skills from `skills-lock.json`
3. Loads enabled plugins from settings
4. Applies configurations

## Adding New Skills to This Collection

### Creating a Custom Skill

```bash
# Create skill directory structure
mkdir -p .claude/skills/my-skill/{references,scripts}

# Write skill definition
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does and when to use it
license: MIT
metadata:
  author: Your Name
---

# My Skill

[Detailed instructions...]
EOF

# Add to this collection (commit to git)
git add .claude/skills/my-skill/
git commit -m "Add my-skill for [purpose]"
```

### Using skill-creator Skill

For a guided workflow:

```bash
/skill-creator
```

This interactive process:
1. Helps define skill requirements
2. Drafts initial SKILL.md
3. Creates and runs test cases
4. Evaluates with quantitative metrics
5. Iterates until ready
6. Optimizes description for triggering

## Common Workflows

### Workflow 1: Create a Pull Request
1. Make changes in a feature branch
2. Run `git diff main...HEAD` to see changes
3. Create changelog: `/create-changelog`
4. Open pull request: `/pr-open`
5. Review PR body and merge when ready

### Workflow 2: Plan a Major Feature
1. Use `/plan` (or `EnterPlanMode`) to start planning
2. Claude explores codebase and understands architecture
3. Presents implementation plan with options
4. Once approved, follow the step-by-step plan
5. Code changes automatically pass quality checks (hooks)

### Workflow 3: Build a New UI Component
1. Describe the component and its purpose
2. Use `/frontend-design` skill
3. Get production-grade code with distinctive aesthetics
4. Copy to your project and integrate

### Workflow 4: Create a Custom Skill
1. Describe what the skill should do
2. Use `/skill-creator` for guided workflow
3. Follow test → evaluate → iterate loop
4. Add to `./.claude/skills/` when ready
5. Commit to this collection

## Troubleshooting

### Symlink Not Working

```bash
# Check if symlink exists
ls -l .claude

# If broken, remove and recreate
rm .claude
ln -s ../claude/.claude .claude

# Verify
ls -l .claude
```

### Skills Not Loading

1. Verify `.claude/skills/` exists: `ls .claude/skills/`
2. Check skill SKILL.md has required frontmatter
3. Restart Claude Code to reload skills
4. Review `.claude/settings.json` for hook errors

### Plugin Configuration Issues

1. Check plugin configuration in `.claude/settings.json`
2. Verify enabled plugins: `"enabledPlugins": { "agent-skills@addy-agent-skills": true }`
3. Restart Claude Code to reload plugins

## Agent Skills Plugin (@addy-agent-skills)

This collection includes the complete **@addy-agent-skills** plugin suite — 30+ specialized agent skills for every phase of development. Source: [`@addy-agent-skills/agent-skills`](https://github.com/addyosmani/agent-skills/tree/main)

| Skill | Category | Purpose | Source |
|-------|----------|---------|--------|
| **ship** | Workflow | Run pre-launch checklist with parallel specialist personas | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **spec** | Workflow | Write structured specifications before implementation | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **plan** | Workflow | Break work into small verifiable tasks with dependencies | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **build** | Workflow | Implement tasks incrementally with validation | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **test** | Workflow | Test-driven development with failing tests first | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **review** | Workflow | Five-axis code review (correctness, readability, architecture, security, performance) | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **idea-refine** | Workflow | Diverge and converge on ideas before building | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **interview-me** | Workflow | Extract actual requirements vs. assumptions | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **frontend-ui-engineering** | Domain | Production-quality UI building | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **api-and-interface-design** | Domain | Stable API and module boundary design | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **performance-optimization** | Domain | Profiling and optimization strategies | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **security-and-hardening** | Domain | Vulnerability hardening and OWASP hardening | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **ci-cd-and-automation** | Domain | Pipeline setup and automation | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **documentation-and-adrs** | Domain | Architecture decision records and docs | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **incremental-implementation** | Practice | Ship changes in small, verifiable steps | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **test-driven-development** | Practice | TDD patterns and practices | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-review-and-quality** | Practice | Multi-axis code review patterns | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **source-driven-development** | Practice | Ground decisions in official documentation | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **doubt-driven-development** | Practice | Adversarial review before decisions | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **git-workflow-and-versioning** | Practice | Git practices and version management | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **debugging-and-error-recovery** | Specialized | Systematic root-cause analysis | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **context-engineering** | Specialized | Optimize agent context and prompts | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **deprecation-and-migration** | Specialized | Plan and execute migrations | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **browser-testing-with-devtools** | Specialized | Real browser testing via DevTools MCP | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **using-agent-skills** | Specialized | Discover and invoke agent skills | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-simplify** | Specialized | Simplify code for clarity | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-simplification** | Specialized | Simplify code for clarity and maintainability | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **spec-driven-development** | Specialized | Create specs before coding | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **shipping-and-launch** | Specialized | Prepare production launches | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **planning-and-task-breakdown** | Specialized | Break work into ordered tasks | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |

## Reference Files

- **Skills Registry**: `./skills-lock.json` — Open-source skills from anthropics/skills
- **Agent Skills Plugin**: `@addy-agent-skills/agent-skills` — 30+ specialized development skills
- **Settings**: `./.claude/settings.json` — Plugin configuration

## Support

For questions or issues:
- Check individual skill SKILL.md files for detailed documentation
- Review project conventions in `./.claude/rules/`
- Use `/skill-creator` for building new skills
- Refer to README.md for installation and skills overview

---

**Last updated**: 2026-06-04  
**Collection**: @torqlab/claude  
**Maintainer**: Mr.B.Lab  
**License**: MIT
