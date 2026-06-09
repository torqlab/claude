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

## 🎯 Decision Trees

Guide for agents to select the right workflow based on your situation.

### "I need to implement a feature"
- Do you have clear requirements?
  - NO → Use `/interview-me` or `/idea-refine` to clarify, then continue
  - YES → Continue to next question
- Have you written a specification?
  - NO → Use `/spec` to write detailed requirements, then continue
  - YES → Continue to next question
- Have you planned the work?
  - NO → Use `/plan` to break into ordered tasks, then continue
  - YES → Continue to next question
- Ready to build?
  - Use `/build` to implement incrementally
  - As you code, use `/test` for test-driven validation
  - When ready, use `/review` for quality gate
  - Finally, use `/ship` for production launch

### "Something is broken (bug or test failure)"
- Do you understand the root cause?
  - NO → Use `/debugging-and-error-recovery` for systematic analysis
  - YES → Continue to next question
- Is there a failing test?
  - NO → Use `/test` to create a failing test first (TDD approach)
  - YES → Continue to next question
- Ready to fix?
  - Use `/build` to implement the fix
  - Use `/test` to verify the test now passes
  - Use `/review` for quality gate
  - Use `/ship` if deploying

### "Performance is an issue"
- Have you profiled the application?
  - NO → Use `/performance-optimization` to profile and identify bottlenecks
  - YES → Continue to next question
- Ready to optimize?
  - Use `/build` to implement optimizations
  - Use `/test` to verify improvements
  - Use `/review` for quality gate

### "Security concern or compliance requirement"
- Need to harden code?
  - Use `/security-and-hardening` for vulnerability analysis
  - Use `/build` to implement hardening measures
  - Use `/test` to verify security improvements
  - Use `/review` and `/ship` for deployment

### "Refactoring or design work"
- Need API/module design guidance?
  - Use `/api-and-interface-design` for stable interface design
- Need documentation of architectural decisions?
  - Use `/documentation-and-adrs` to record decisions
- Need to review before merging?
  - Use `/code-review-and-quality` for detailed multi-axis review


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


## 🛠️ Custom Skills Integration Guide

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


## 📋 Agent Context Requirements

Prerequisites, inputs, and outputs for each major agent workflow phase.

| Agent | Phase | Prerequisites | Input Context | Output | Success Criteria |
|-------|-------|---|---|--------|------------------|
| `/interview-me` | Requirements | Problem description | Initial idea or requirement | Clarified requirements | Clear understanding of actual needs |
| `/idea-refine` | Requirements | Vague concept | Rough idea or feature request | Actionable requirements | Requirements are specific and measurable |
| `/spec` | Specification | Clear requirements | Requirements document | Detailed specification with acceptance criteria | Spec includes acceptance criteria and edge cases |
| `/plan` | Planning | Specification complete | Detailed spec | Ordered tasks with dependencies | Tasks are ordered, dependencies clear, ready to build |
| `/build` | Implementation | Task list ready | Task description and related spec | Tested, verified, committed code | Code changes committed to feature branch |
| `/test` | Testing | Code or failing test | Code changes or test failure | Passing tests or verified behavior | All tests passing or behavior verified |
| `/review` | Review | Code ready for feedback | Code changes to review | Review feedback or approval | All review feedback addressed |
| `/ship` | Launch | Code reviewed and approved | Approved code and release context | Production deployment checklist | Deployment checklist completed |
| `/debugging-and-error-recovery` | Debugging | Error symptoms or test failure | Error message, logs, or failing test | Root cause identified | Root cause documented and understood |
| `/performance-optimization` | Optimization | Performance baseline | Baseline metrics and code | Optimization strategy and/or implementation | Performance improved per requirements |
| `/security-and-hardening` | Security | Security audit or vulnerability | Code to audit or vulnerability details | Hardening strategy or implementation | Security improvements verified |
| `/frontend-ui-engineering` | Frontend | Design requirements | UI requirements or design specs | Implemented UI components | UI passes acceptance criteria |
| `/api-and-interface-design` | Architecture | API requirements | API requirements or module spec | Stable interface design | API design reviewed and documented |

**Context inheritance**: Later phases build on outputs from earlier phases. Each output becomes input context for the next agent in the workflow.


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
