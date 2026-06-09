# TORQ Claude Configuration Collection

A shared collection of Claude configurations, skills, hooks, and conventions for the TORQ project. This repository provides a unified set of AI development tools used across multiple TORQ repositories via symlinks.

## Overview

This is a **project-level Claude collection** that serves as a centralized source of truth for Claude development practices. Every TORQ repository can reference this collection via a symlink, ensuring consistent configurations, skills, and conventions across all projects.

**Primary Development Methodology**: This collection uses **Addy Osmani's agent-skills workflow** as the foundation for structured, collaborative development. This proven framework breaks work into clear phases with specialized agents, testing strategies, and quality gates—enabling faster iteration while maintaining code quality and reliability.

**Key purpose**: Enable standardized AI-driven development workflows, code generation, and automation while maintaining quality standards through shared hooks, rules, and custom skills.

## What's Included

- **[SKILLS.md](./SKILLS.md)** — Complete reference for all available skills organized by type (custom, open-source, agent skills) with decision trees for workflow selection
- **Addy Osmani Workflow** — Structured development methodology with specialized agents for each phase
- **Custom Skills** — Project-specific skills for semantic versioning, branch management, PR creation, and documentation
- **Configurations** — Claude Code settings, hooks, and project conventions in `.claude/`
- **Documentation** — Setup guides, workflow patterns, and integration examples

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

### Common Workflows

Typical development patterns using the agent-skills workflow:

#### Workflow 1: Start with Unclear Requirements
1. Use `/idea-refine` or `/interview-me` to clarify scope
2. Write specification with `/spec`
3. Plan with `/plan` to break into tasks
4. Implement with `/build`
5. Test with `/test` (TDD approach)
6. Review with `/review` before merge
7. Launch with `/ship` when ready

#### Workflow 2: Implement a Known Feature
1. Have specifications ready
2. Use `/plan` to organize tasks
3. Use `/build` to implement incrementally
4. Use `/test` for test-driven development
5. Use `/review` for quality gate
6. Use `/ship` before production

#### Workflow 3: Debug or Fix an Issue
1. Use `/debugging-and-error-recovery` for systematic root-cause analysis
2. Use `/test` to create failing test first
3. Fix and verify with `/build`
4. Use `/review` before merge

#### Workflow 4: Optimize Performance
1. Use `/performance-optimization` to profile and identify bottlenecks
2. Implement optimizations with `/build`
3. Test improvements with `/test`
4. Use `/review` before merge

#### Workflow 5: Add Security Hardening
1. Use `/security-and-hardening` for vulnerability analysis
2. Implement fixes with `/build`
3. Test with `/test`
4. Use `/ship` or `/review` before deployment

### Agent Combinations & Context Flow

Common agent workflow sequences and how context flows between them:

| Sequence | Prerequisites | Purpose | Output Context |
|----------|---|---------|--------|
| `/interview-me` → `/spec` | Unclear requirements | Clarify and document requirements | Detailed specification |
| `/spec` → `/plan` → `/build` | Clear specification | Feature development workflow | Planned tasks → Implementation |
| `/plan` → `/build` → `/test` → `/review` | Task list | Complete build cycle | Code changes → Tests → Review feedback |
| `/test` → `/build` → `/review` → `/ship` | Failing test | Bug fix and deployment | Test fix → Reviewed code → Production ready |
| `/debugging-and-error-recovery` → `/test` → `/build` | Error symptoms | Systematic debugging | Root cause → Failing test → Fix |
| `/performance-optimization` → `/build` → `/test` | Performance baseline | Performance improvement | Optimization strategy → Implemented → Verified |
| `/security-and-hardening` → `/build` → `/test` → `/review` | Security audit | Security hardening | Hardening strategy → Implementation → Verification |
| `/api-and-interface-design` → `/build` → `/test` | API requirements | Stable interface design | API design → Implementation → Tests |
| `/code-review-and-quality` → `/ship` | Code ready for review | Final quality gate before ship | Review feedback → Ship checklist |
| `/doubt-driven-development` → `/build` | Non-trivial decision | Adversarial review of design | Questioned assumptions → Confirmed approach |
| `/documentation-and-adrs` → `/build` | Architectural decision | Record decision and implement | ADR → Implementation |

**Context flows left-to-right**: Output from one agent becomes the input context for the next agent in the sequence.

**Reference**: [Addy Osmani's agent-skills repository](https://github.com/addyosmani/agent-skills)

## Adding Skills to This Collection

### Project-Specific Skills

This collection provides custom skills for semantic versioning, branch management, and documentation:

| Skill | Purpose | Usage |
|-------|---------|-------|
| **semantic-release** | Agent-driven workflow for creating git branches and conventional commits aligned with semantic versioning | `/semantic-release` |
| **git-branch** | Create git branches with semantic-release naming conventions for the current repository | `/git-branch` |
| **pr** | Agent-driven GitHub PR creation workflow aligned with semantic-release conventions | `/pr` |
| **github-mcp-setup** | Configure GitHub Model Context Protocol (MCP) server for Claude Code using GitHub App authentication | `/github-mcp-setup` |
| **align-skills-documentation** | Discovers all available skills and generates a dedicated SKILLS.md file in the project root with a comprehensive table organized by skill type | `/align-skills-documentation` |

### Skill Integration with Agent Workflow

How custom project-specific skills integrate with agent-skills:

| Skill | Integration Point | Works With Agents | Sequence |
|-------|-------------------|------------------|----------|
| **semantic-release** | During `/plan` → `/build` | `/plan`, `/build` | `/plan` → `/semantic-release` (create branch) → `/build` |
| **git-branch** | At start of `/build` | `/plan`, `/build` | `/plan` → `/git-branch` (create) → `/build` |
| **pr** | After `/build` when ready for review | `/build`, `/review`, `/ship` | `/build` → `/review` → `/pr` (create) → `/ship` |
| **github-mcp-setup** | Before any `/pr` usage | `/pr` | Setup first, then use `/pr` |
| **align-skills-documentation** | Before releases or during maintenance | Any workflow | Use after adding new skills |

**Integration strategy**:
- **Branch creation**: Use `/semantic-release` or `/git-branch` early in `/build` phase
- **Code review integration**: `/review` provides feedback context for `/pr` creation
- **Release workflow**: Complete `/build` → `/review` → `/pr` → `/ship` sequence
- **Documentation**: Keep `/align-skills-documentation` up to date after skill additions

### Open-Source Skills (from NPM)

Skills from Anthropic's [anthropics/skills](https://github.com/anthropics/skills) are managed via `npx skills` and `skills-lock.json`:

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

**Last updated**: 2026-06-09
