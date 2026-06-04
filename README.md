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
| **pr-open** | Custom | Create pull requests on GitHub directly from changelog entries with branch validation and smart defaults | [./.claude/skills/pr-open/SKILL.md](./.claude/skills/pr-open/SKILL.md) |
| **create-changelog** | Custom | Generate accurate changelog entries following Keep a Changelog standard based on git diffs | [./.claude/skills/create-changelog/SKILL.md](./.claude/skills/create-changelog/SKILL.md) |
| **github-mcp-setup** | Custom | Configure GitHub MCP (Model Context Protocol) for GitHub automation with GitHub App authentication | [./.claude/skills/github-mcp-setup/SKILL.md](./.claude/skills/github-mcp-setup/SKILL.md) |
| **frontend-design** | Open-source | Build distinctive, production-grade UI components with cohesive aesthetic direction | [anthropics/skills](https://github.com/anthropics/skills) |
| **skill-creator** | Open-source | Create, test, and iteratively improve new Claude skills with comprehensive evaluation workflows | [anthropics/skills](https://github.com/anthropics/skills) |
| **ship** | Agent Skill | Run pre-launch checklist via parallel fan-out to specialist personas | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-simplify** | Agent Skill | Simplify code for clarity and maintainability without changing behavior | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **review** | Agent Skill | Conduct five-axis code review (correctness, readability, architecture, security, performance) | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **spec** | Agent Skill | Start spec-driven development with structured specifications before coding | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **plan** | Agent Skill | Break work into small verifiable tasks with acceptance criteria and dependencies | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **build** | Agent Skill | Implement tasks incrementally with build, test, verify, and commit cycles | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **test** | Agent Skill | Run TDD workflow with failing tests first for bugs and features | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **idea-refine** | Agent Skill | Refine raw ideas into sharp, actionable concepts through divergent and convergent thinking | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **using-agent-skills** | Agent Skill | Discover and invoke available agent skills from this collection | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **debugging-and-error-recovery** | Agent Skill | Guide systematic root-cause debugging and error recovery workflows | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **interview-me** | Agent Skill | Extract actual user wants vs. assumed requirements through structured interviews | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **frontend-ui-engineering** | Agent Skill | Build production-quality user interfaces with careful attention to design | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **context-engineering** | Agent Skill | Optimize agent context setup for better output quality and relevance | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **deprecation-and-migration** | Agent Skill | Manage deprecation workflows and guide safe migration strategies | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **ci-cd-and-automation** | Agent Skill | Automate CI/CD pipeline setup and orchestration | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **security-and-hardening** | Agent Skill | Harden code against vulnerabilities and OWASP top 10 threats | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-review-and-quality** | Agent Skill | Conduct multi-axis code review for quality and correctness | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **api-and-interface-design** | Agent Skill | Design stable APIs and module boundaries with careful consideration of interfaces | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **spec-driven-development** | Agent Skill | Create detailed specifications before implementing code changes | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **incremental-implementation** | Agent Skill | Deliver changes incrementally with small, verifiable steps | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **shipping-and-launch** | Agent Skill | Prepare applications for production launch with comprehensive checklists | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **planning-and-task-breakdown** | Agent Skill | Break work into ordered tasks with dependencies and acceptance criteria | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **documentation-and-adrs** | Agent Skill | Record architectural decisions and create documentation | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **performance-optimization** | Agent Skill | Optimize application performance through profiling and targeted improvements | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **source-driven-development** | Agent Skill | Ground implementation decisions in official documentation and specifications | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **test-driven-development** | Agent Skill | Drive development with tests as primary design tool | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **git-workflow-and-versioning** | Agent Skill | Structure git workflow practices and semantic versioning | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **doubt-driven-development** | Agent Skill | Subject non-trivial decisions to fresh-context adversarial review | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **code-simplification** | Agent Skill | Simplify code for clarity and maintainability without changing behavior | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |
| **browser-testing-with-devtools** | Agent Skill | Test applications in real browsers via Chrome DevTools MCP | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main) |

### 🔧 Configuration

Claude Code settings and plugins:

- **`.claude/settings.json`** - Plugin configuration (agent-skills@addy-agent-skills enabled)
- **`.claude/settings.local.json`** - Local development overrides
- **`skills-lock.json`** - Pinned versions of open-source skills from anthropics/skills

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
| **Requirements** | `/interview-me` | Extract actual user needs vs. assumed requirements | `/interview-me` |
| **Specification** | `/spec` or `/spec-driven-development` | Write detailed specs before coding begins | `/spec` |
| **Planning** | `/plan` or `/planning-and-task-breakdown` | Break work into ordered tasks with dependencies | `/plan` |
| **Implementation** | `/build` or `/incremental-implementation` | Implement tasks incrementally with validation | `/build` |
| **Testing** | `/test` or `/test-driven-development` | TDD workflow with failing tests first | `/test` |
| **Code Review** | `/review` or `/code-review-and-quality` | Five-axis review (correctness, readability, architecture, security, performance) | `/review` |
| **Launch** | `/ship` or `/shipping-and-launch` | Pre-launch checklist and production readiness | `/ship` |

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
│   │   ├── pr-open/
│   │   ├── create-changelog/
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
