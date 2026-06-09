# AGENTS.md — Agent Skills & Development Workflow Guide

**Reference**: See [README.md](./README.md) for complete overview, installation instructions, and skills table.

This guide documents the **Addy Osmani agent-skills workflow** — the primary development methodology for this TORQ Claude configuration collection. All agents and skills work together to support structured, collaborative development from requirements through launch.

## 🔍 About This Collection

**TORQ Claude** is a shared collection of Claude configurations, skills, and conventions. Per [README.md](./README.md):

> **Primary Development Methodology**: This collection uses **Addy Osmani's agent-skills workflow** as the foundation for structured, collaborative development. This proven framework breaks work into clear phases with specialized agents, testing strategies, and quality gates—enabling faster iteration while maintaining code quality and reliability.

**Maintainer**: Mr.B.Lab  
**Repository**: @torqlab/claude  
**License**: MIT

## Quick Reference

- **README.md** (source of truth) — Overview, installation, complete skills table
- **This document** — Workflow phases, when to use each agent
- **Skills**: See README.md §Skills table for full list
- **Installation**: See README.md §Quick Start for symlink setup
- **Conventions**: `./.claude/rules/` directory

## 🎯 Addy Osmani Workflow: Primary Development Methodology

The **Addy Osmani agent-skills workflow** is the core development approach. See [README.md §Addy Osmani Workflow](./README.md#-addy-osmani-workflow-primary-development-methodology) for:
- **Core Workflow Phases** table (requirements → specification → planning → implementation → testing → review → launch)
- **Essential Commands & Shortcuts** (organized by purpose)
- **Typical Development Flow** (step-by-step process)
- **When to Use Each Agent** (decision guidance)

## 🔧 Workflow Guidance

The **Addy Osmani agent-skills workflow** is the core development approach. See [README.md §Addy Osmani Workflow](./README.md#-addy-osmani-workflow-primary-development-methodology) for:
- **Core Workflow Phases** table
- **Essential Commands & Shortcuts** (organized by purpose)
- **Typical Development Flow** (step-by-step process)
- **When to Use Each Agent** (decision guidance)

For a complete list of all available agent skills, see [SKILLS.md §Agent Skills](./SKILLS.md#agent-skills).

## 📦 Project-Specific Skills

In addition to agent-skills, this collection provides custom and open-source skills. See [README.md §Key Skills Overview](./README.md#-key-skills-overview) for details.

### Custom Skills (Project-Specific)

| Skill | Purpose | Usage |
|-------|---------|-------|
| **align-skills-documentation** | Auto-sync README.md and AGENTS.md with available skills inventory | `/align-skills-documentation` |
| **semantic-release** | Create git branches with semantic-release naming conventions | `/semantic-release` |
| **git-branch** | Create branches aligned with semantic-release conventions | `/git-branch` |
| **pr** | Create GitHub pull requests aligned with semantic-release workflow | `/pr` |
| **github-mcp-setup** | Configure GitHub MCP server with GitHub App authentication | `/github-mcp-setup` |

### Open-Source Skills (anthropics/skills)

| Skill | Purpose | Usage |
|-------|---------|-------|
| **frontend-design** | Build distinctive, production-grade UI components | `/frontend-design` |
| **skill-creator** | Create, test, and iteratively improve new Claude skills | `/skill-creator` |

For complete skill details including features and workflows, see README.md.

### Integration Guide

Where custom project-specific skills fit into the agent workflow, and how they integrate with agent skills.

| Skill | Purpose | Integration Point | Works With Agents | Sequence |
|-------|---------|-------------------|------------------|----------|
| **semantic-release** | Create feature branches with semantic versioning | During `/plan` → `/build` | `/plan`, `/build` | `/plan` → `/semantic-release` (create branch) → `/build` |
| **git-branch** | Create semantic-release naming convention branches | At start of `/build` | `/plan`, `/build` | `/plan` → `/git-branch` (create) → `/build` |
| **pr** | Create GitHub pull requests aligned with semantic-release | After `/build` when ready for review | `/build`, `/review`, `/ship` | `/build` → `/review` → `/pr` (create) → `/ship` |
| **github-mcp-setup** | Configure GitHub MCP server for automated workflows | Before any `/pr` usage | `/pr` | Setup first, then use `/pr` |
| **align-skills-documentation** | Synchronize documentation with available skills | Before releases or during maintenance | Any workflow | Use after adding new skills |

**Integration strategy**:
- **Branch creation**: Use `/semantic-release` or `/git-branch` early in `/build` phase
- **Code review integration**: `/review` provides feedback context for `/pr` creation
- **Release workflow**: Complete `/build` → `/review` → `/pr` → `/ship` sequence
- **Documentation**: Keep `/align-skills-documentation` up to date after skill additions

## 📋 Common Workflows

Typical development patterns using the agent-skills workflow:

### Workflow 1: Start with Unclear Requirements
1. Use `/idea-refine` or `/interview-me` to clarify scope
2. Write specification with `/spec`
3. Plan with `/plan` to break into tasks
4. Implement with `/build`
5. Test with `/test` (TDD approach)
6. Review with `/review` before merge
7. Launch with `/ship` when ready

### Workflow 2: Implement a Known Feature
1. Have specifications ready
2. Use `/plan` to organize tasks
3. Use `/build` to implement incrementally
4. Use `/test` for test-driven development
5. Use `/review` for quality gate
6. Use `/ship` before production

### Workflow 3: Debug or Fix an Issue
1. Use `/debugging-and-error-recovery` for systematic root-cause analysis
2. Use `/test` to create failing test first
3. Fix and verify with `/build`
4. Use `/review` before merge

### Workflow 4: Optimize Performance
1. Use `/performance-optimization` to profile and identify bottlenecks
2. Implement optimizations with `/build`
3. Test improvements with `/test`
4. Use `/review` before merge

### Workflow 5: Add Security Hardening
1. Use `/security-and-hardening` for vulnerability analysis
2. Implement fixes with `/build`
3. Test with `/test`
4. Use `/ship` or `/review` before deployment

## 🔌 Installation & Setup

For complete installation instructions, see [README.md §Quick Start](./README.md#quick-start-using-this-collection-in-your-project).

**Quick setup** (from any TORQ repository):

```bash
# Create symlink
ln -s ../claude/.claude .claude

# Verify
ls -l .claude
```

All skills and agents are automatically discovered after creating the symlink.

## 📚 Reference & Resources

- **README.md** (source of truth) — Overview, installation, complete skills and workflow documentation
- **`.claude/skills/`** — Custom project-specific skills
- **`.claude/settings.json`** — Plugin configuration
- **`.claude/rules/`** — Project conventions and coding standards
- **`skills-lock.json`** — Open-source skills registry from anthropics/skills
- **Agent Skills Source**: [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main)

## 🎯 Decision Trees

Decision trees for selecting the right skill or workflow have been moved to [SKILLS.md §Decision Trees](./SKILLS.md#-decision-trees). This ensures a single source of truth for skill guidance.


## 🔗 Agent Combinations & Context Flow

Common agent workflow sequences and the context that flows between them.

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


## Getting Help

1. **See README.md** for installation, overview, and complete skill details
2. **Check individual SKILL.md files** for detailed skill documentation in `./.claude/skills/*/`
3. **Review project conventions** in `./.claude/rules/`
4. **Explore agent skills** with `/using-agent-skills` command

---

**Last updated**: 2026-06-04  
**Collection**: @torqlab/claude  
**Maintainer**: Mr.B.Lab  
**License**: MIT  
**Source**: [README.md](./README.md) is the authoritative reference for this collection
