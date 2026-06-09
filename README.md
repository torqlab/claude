# TORQ Claude Configuration Collection

A shared collection of Claude configurations, skills, hooks, and conventions for the TORQ project. This repository provides a unified set of AI development tools used across multiple TORQ repositories via symlinks.

## Overview

This is a **project-level Claude collection** that serves as a centralized source of truth for Claude development practices. Every TORQ repository can reference this collection via a symlink, ensuring consistent configurations, skills, and conventions across all projects.

**Primary Development Methodology**: This collection uses **Addy Osmani's agent-skills workflow** as the foundation for structured, collaborative development. This proven framework breaks work into clear phases with specialized agents, testing strategies, and quality gates—enabling faster iteration while maintaining code quality and reliability.

**Key purpose**: Enable standardized AI-driven development workflows, code generation, and automation while maintaining quality standards through shared hooks, rules, and custom skills.

## What's Included

### 📦 Skills

This collection includes both **NPM-based open-source skills** and **custom project-specific skills**.

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| **align-skills-documentation** | Custom | Automatically synchronizes README.md and AGENTS.md documentation by discovering all available skills from custom files,... | [./.claude/skills/align-skills-documentation/SKILL.md](./.claude/skills/align-skills-documentation/SKILL.md) |
| **git-branch** | Custom | Create git branches with semantic-release naming conventions for the current repository. | [./.claude/skills/git-branch/SKILL.md](./.claude/skills/git-branch/SKILL.md) |
| **github-mcp-setup** | Custom | Configure GitHub Model Context Protocol (MCP) server for Claude Code using GitHub App authentication. | [./.claude/skills/github-mcp-setup/SKILL.md](./.claude/skills/github-mcp-setup/SKILL.md) |
| **pr** | Custom | Agent-driven GitHub PR creation workflow aligned with semantic-release conventions. | [./.claude/skills/pr/SKILL.md](./.claude/skills/pr/SKILL.md) |
| **semantic-release** | Custom | Agent-driven workflow for creating git branches and conventional commits aligned with semantic-release. | [./.claude/skills/semantic-release/SKILL.md](./.claude/skills/semantic-release/SKILL.md) |
| **frontend-design** | Open-source |  | [anthropics/skills](https://github.com/anthropics/skills) |
| **skill-creator** | Open-source |  | [anthropics/skills](https://github.com/anthropics/skills) |
| **api-and-interface-design** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **browser-testing-with-devtools** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **build** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **ci-cd-and-automation** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-review-and-quality** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-simplify** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **context-engineering** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **debugging-and-error-recovery** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **deprecation-and-migration** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **documentation-and-adrs** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **doubt-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **frontend-ui-engineering** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **git-workflow-and-versioning** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **idea-refine** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **incremental-implementation** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **interview-me** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **performance-optimization** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **plan** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **planning-and-task-breakdown** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **review** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **security-and-hardening** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **ship** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **shipping-and-launch** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **source-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **spec** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **spec-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **test** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **test-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **using-agent-skills** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |


### 🔧 Configuration

Claude Code settings and plugins:

- **`.claude/settings.json`** - Plugin configuration (agent-skills@addy-agent-skills enabled)
- **`.claude/settings.local.json`** - Local development overrides
- **`skills-lock.json`** - Pinned versions of open-source skills from anthropics/skills

### Trigger Context & Usage Patterns

#### Workflow Planning & Specification
- **ci-cd-and-automation**: Use this skill to work with ci cd and automation
- **code-simplify**: Use this skill to work with code simplify
- **context-engineering**: Use this skill to work with context engineering
- **deprecation-and-migration**: Use this skill to work with deprecation and migration
- **documentation-and-adrs**: Use this skill to work with documentation and adrs
- **doubt-driven-development**: Use this skill to work with doubt driven development
- **git-workflow-and-versioning**: Use this skill to work with git workflow and versioning
- **idea-refine**: Use this skill to work with idea refine
- **interview-me**: Use this skill to work with interview me
- **plan**: Use this skill to work with plan
- **planning-and-task-breakdown**: Use this skill to work with planning and task breakdown
- **ship**: Use this skill to work with ship
- **shipping-and-launch**: Use this skill to work with shipping and launch
- **skill-creator**: Use this skill to work with skill creator
- **source-driven-development**: Use this skill to work with source driven development
- **spec**: Use this skill to work with spec
- **spec-driven-development**: Use this skill to work with spec driven development
- **using-agent-skills**: Use this skill to work with using agent skills

#### Implementation & Build
- **build**: Use this skill to work with build
- **git-branch**: Create git branches with semantic-release naming conventions for the current...
- **incremental-implementation**: Use this skill to work with incremental implementation
- **pr**: Agent-driven GitHub PR creation workflow aligned with semantic-release...
- **semantic-release**: Agent-driven workflow for creating git branches and conventional commits...

#### Testing & Debugging
- **browser-testing-with-devtools**: Use this skill to work with browser testing with devtools
- **debugging-and-error-recovery**: Use this skill to work with debugging and error recovery
- **test**: Use this skill to work with test
- **test-driven-development**: Use this skill to work with test driven development

#### Code Review & Quality
- **code-review-and-quality**: Use this skill to work with code review and quality
- **github-mcp-setup**: Configure GitHub Model Context Protocol (MCP) server for Claude Code using...
- **performance-optimization**: Use this skill to work with performance optimization
- **review**: Use this skill to work with review
- **security-and-hardening**: Use this skill to work with security and hardening

#### Frontend & UI
- **align-skills-documentation**: Automatically synchronizes README.md and AGENTS.md documentation by discovering...
- **api-and-interface-design**: Use this skill to work with api and interface design
- **frontend-design**: Use this skill to work with frontend design
- **frontend-ui-engineering**: Use this skill to work with frontend ui engineering

## Quick Start: Using This Collection in Your Project

### Installation

Every TORQ repository can use this collection via a **symlink to `.claude`**. This ensures consistent configurations, skills, and conventions across all projects.

#### Step 1: Create the Symlink

From your TORQ repository directory, create a symlink to this collection's `.claude` directory:

```bash
# Absolute path
ln -s /path/to/torq/claude/.claude .claude

# Or relative path (if torq/claude is a sibling)
ln -s ../claude/.claude .claude
```

#### Step 2: Verify the Symlink

Confirm the symlink works:

```bash
ls -l .claude
# Should show: .claude -> ../claude/.claude (or absolute path)
```

#### Step 3: Configure Git (Optional but Recommended)

Add `.claude` to `.gitignore`:

```gitignore
# Claude Code
.claude
```

Then optionally commit the symlink itself (Git handles symlinks correctly):

```bash
git add .claude
git commit -m "Add Claude configuration collection via symlink"
```

#### Step 4: Skills and Plugins Ready to Use

Claude Code will automatically discover and load:
- ✅ All custom skills from `.claude/skills/`
- ✅ All open-source skills from `skills-lock.json`
- ✅ All enabled plugins (agent-skills@addy-agent-skills)
- ✅ Settings from `.claude/settings.json`

No additional setup needed — start using Claude Code as normal!

## 🎯 Addy Osmani Workflow: Primary Development Methodology

This collection implements **Addy Osmani's agent-skills framework** as the core development workflow. This structured approach breaks complex work into clear phases with specialized agents, ensuring quality, testing, and iterative improvement at each stage.

### Core Workflow Phases

| Phase | Agent Skill | Purpose | Command |
|-------|-------------|---------|---------|
| **Idea Refinement** | `/idea-refine` | Refine raw concepts into sharp, actionable requirements | `/idea-refine` |
| **Code Review** | `/review` or `/code-review-and-quality` | Five-axis review (correctness, readability, architecture, security, performance) | `/review` |

### Essential Commands & Shortcuts

**Start with requirements:**
```bash
/spec          # Spec-driven development - write before coding
/interview-me  # Extract real requirements
/idea-refine   # Refine vague ideas into actionable specs
```

**Implement & build:**
```bash
/plan          # Break spec into ordered tasks
/build         # Implement incrementally
/test          # Run TDD workflow (failing tests first)
```

**Quality gates:**
```bash
/review        # Five-axis code review
/ship          # Pre-launch checklist
```

**Supporting tools:**
```bash
/source-driven-development    # Ground decisions in documentation
/doubt-driven-development     # Adversarial review of decisions
/debugging-and-error-recovery # Systematic debugging
/performance-optimization     # Profile and optimize
/security-and-hardening       # Vulnerability hardening
```

### Typical Development Flow

```
1. Start with unclear requirements
   → /interview-me or /idea-refine
   
2. Write specification
   → /spec
   
3. Plan the work
   → /plan (breaks into tasks)
   
4. Build incrementally
   → /build (implement → test → verify → commit)
   
5. Code review
   → /review (five-axis review)
   
6. Launch
   → /ship (pre-launch checklist)
```

### When to Use Each Agent

- **Uncertain requirements?** Start with `/interview-me` or `/idea-refine`
- **Starting new feature?** Use `/spec` to write requirements first
- **Have specs/requirements?** Use `/plan` to break into tasks
- **Implementing a task?** Use `/build` for incremental cycles
- **Bug or test failure?** Use `/test` for TDD or `/debugging-and-error-recovery`
- **Before merge?** Use `/review` for quality gate
- **Going to production?** Use `/ship` for final checklist

**Reference**: [Addy Osmani's agent-skills repository](https://github.com/addyosmani/agent-skills)

No additional setup needed — start using Claude Code as normal!

## Adding Skills to This Collection

### Open-Source Skills (from NPM)

Skills from Anthropic's [anthropics/skills](https://github.com/anthropics/skills) are managed via `skills-lock.json`:

```json
{
  "version": 1,
  "skills": {
    "my-skill": {
      "source": "anthropics/skills",
      "ref": "main",
      "sourceType": "github",
      "skillPath": "skills/my-skill/SKILL.md"
    }
  }
}
```

### Custom Project-Specific Skills

Add custom skills to `.claude/skills/<skill-name>/`:

```
.claude/skills/my-skill/
├── SKILL.md                 # Main skill definition
├── references/              # Documentation files
│   ├── guide.md
│   └── examples.md
├── scripts/                 # Reusable helper scripts
│   └── helper.py
└── assets/                  # Templates, icons, etc.
```

**SKILL.md frontmatter** (required):
```yaml
---
name: my-skill
description: When to use this skill and what it does. Make descriptions clear about trigger contexts.
license: MIT
metadata:
  author: Your Name
---
```

## Repository Structure

```
torq/claude/
├── .claude/
│   ├── skills/              # Custom project-specific skills
│   │   ├── github-mcp-setup/
│   │   └── skill-creator/   # Imported from anthropics/skills
│   ├── settings.json        # Plugin configuration
│   └── settings.local.json  # Local overrides
├── README.md                # This file
├── AGENTS.md                # Agent setup guide
├── package.json             # Project metadata
├── skills-lock.json         # Open-source skills registry
└── .nvmrc                   # Node version specification
```

## Key Skills Overview

### 📝 Frontend Design
Build production-grade UIs with distinctive aesthetics:
```
/frontend-design
```
Creates HTML/React components with cohesive visual direction, custom typography, animations, and attention to design details.

### 🔄 Create Changelog
Generate accurate changelogs from git diffs:
```
/create-changelog
```
Analyzes code changes and creates SemVer-based changelog entries following Keep a Changelog standard.

### 🚀 PR Open
Create pull requests directly from changelog:
```
/pr-open
```
Automates PR creation with branch validation, smart defaults, and changelog-driven formatting.

### 🛠️ GitHub MCP Setup
Configure GitHub automation:
```
/github-mcp-setup
```
Complete GitHub App setup workflow for GitHub MCP integration with fine-grained permissions.

### 🎯 Skill Creator
Build new Claude skills:
```
/skill-creator
```
Full workflow for creating skills: drafting, testing, evaluation, iteration, and description optimization.

## Support & Contributions

**For issues or questions**:
- Check existing skills in `./.claude/skills/*/SKILL.md`
- Review skill documentation in each skill's folder
- For agent-skills, see [https://github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main)

**To add a new skill**:
1. Create a directory in `./.claude/skills/<skill-name>/`
2. Write `SKILL.md` with proper frontmatter
3. Include documentation in `references/` and helper scripts in `scripts/`
4. Test with the `skill-creator` skill

## Version & Metadata

**Repository**: [@torqlab/claude](https://github.com/torqlab/claude)  
**License**: MIT  
**Maintainer**: Mr.B.Lab  
**Node**: 24.x

---

**Last updated**: 2026-06-04
