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

## 🔧 Available Agents in This Collection

All agents are part of the **@addy-agent-skills plugin** suite. For complete workflow details, see [README.md §Addy Osmani Workflow](./README.md#-addy-osmani-workflow-primary-development-methodology).

### Workflow Agents (Core Development Flow)

| Agent | Purpose | When to Use |
|-------|---------|-----------|
| `/idea-refine` | Refine raw concepts into sharp, actionable requirements | Starting with vague ideas or unclear scope |
| `/interview-me` | Extract actual user needs vs. assumed requirements | Before starting development, to clarify requirements |
| `/spec` | Write detailed specifications before implementation | When requirements are clear; write before coding |
| `/plan` | Break work into ordered tasks with dependencies | After spec is complete; need ordered task list |
| `/build` | Implement tasks incrementally with validation | Executing planned tasks; implement → test → verify → commit |
| `/test` | TDD workflow with failing tests first | Testing existing code or developing new features |
| `/review` | Five-axis code review (correctness, readability, architecture, security, performance) | Before merging; quality gate |
| `/ship` | Pre-launch checklist and production readiness | Before shipping to production |

### Domain-Specific Agents

| Agent | Purpose | When to Use |
|-------|---------|-----------|
| `/frontend-ui-engineering` | Build production-quality user interfaces | Designing and implementing frontend features |
| `/api-and-interface-design` | Design stable APIs and module boundaries | Planning API or module architecture |
| `/performance-optimization` | Profile and optimize application performance | Performance issues or optimization requirements |
| `/security-and-hardening` | Harden code against vulnerabilities and OWASP threats | Security-sensitive code; before production |
| `/ci-cd-and-automation` | Automate CI/CD pipeline setup and orchestration | Setting up or improving CI/CD workflows |
| `/documentation-and-adrs` | Record architectural decisions and create documentation | Documenting decisions; creating architecture docs |

### Practice & Specialized Agents

| Agent | Purpose | When to Use |
|-------|---------|-----------|
| `/incremental-implementation` | Ship changes in small, verifiable steps | Implementing features; ensure incremental delivery |
| `/test-driven-development` | TDD patterns and practices | Structuring development around tests |
| `/code-review-and-quality` | Multi-axis code review patterns | Before merge; detailed quality review |
| `/source-driven-development` | Ground decisions in official documentation | When decisions need documentation backing |
| `/doubt-driven-development` | Adversarial review before decisions | Questioning non-trivial decisions |
| `/git-workflow-and-versioning` | Git practices and semantic versioning | Managing git workflow and version management |
| `/debugging-and-error-recovery` | Systematic root-cause analysis | Debugging failures; error recovery |
| `/context-engineering` | Optimize agent context and prompts | Improving output quality and relevance |
| `/deprecation-and-migration` | Plan and execute migrations | Deprecating features or managing migrations |
| `/browser-testing-with-devtools` | Real browser testing via Chrome DevTools MCP | Testing in actual browser environments |
| `/using-agent-skills` | Discover and invoke available agent skills | Learning what agent skills are available |
| `/code-simplify` | Simplify code for clarity | Refactoring code for readability |
| `/code-simplification` | Simplify code for clarity and maintainability | Maintenance and refactoring tasks |
| `/spec-driven-development` | Create detailed specifications before coding | Spec-first development approach |
| `/shipping-and-launch` | Prepare applications for production launch | Pre-launch preparation |
| `/planning-and-task-breakdown` | Break work into ordered tasks with dependencies | Task organization and dependency management |

## 📦 Custom Project-Specific Skills

In addition to agent-skills, this collection provides custom skills. See [README.md §Key Skills Overview](./README.md#-key-skills-overview) for details:

| Skill | Purpose | Usage |
|-------|---------|-------|
| **pr-open** | Create pull requests on GitHub from changelog entries with branch validation | `/pr-open` |
| **create-changelog** | Generate changelog entries following Keep a Changelog standard | `/create-changelog` |
| **github-mcp-setup** | Configure GitHub MCP with GitHub App authentication | `/github-mcp-setup` |
| **frontend-design** | Build distinctive, production-grade UI components | `/frontend-design` |
| **skill-creator** | Create, test, and iteratively improve new Claude skills | `/skill-creator` |

For complete skill details including features and workflows, see README.md.

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
