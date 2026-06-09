# Available Skills

This document lists all available skills organized by type.

## Custom Skills

Project-specific skills maintained in `./.claude/skills/`.

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **document-skills** | Custom | Discovers all available skills and generates a dedicated SKILLS.md file in the project root with a... | [./.claude/skills/document-skills/SKILL.md](./.claude/skills/document-skills/SKILL.md) |
| **git-branch** | Custom | Create git branches with semantic-release naming conventions for the current repository. | [./.claude/skills/git-branch/SKILL.md](./.claude/skills/git-branch/SKILL.md) |
| **github-mcp-setup** | Custom | Configure GitHub Model Context Protocol (MCP) server for Claude Code using GitHub App... | [./.claude/skills/github-mcp-setup/SKILL.md](./.claude/skills/github-mcp-setup/SKILL.md) |
| **pr** | Custom | Agent-driven GitHub PR creation workflow aligned with semantic-release conventions. | [./.claude/skills/pr/SKILL.md](./.claude/skills/pr/SKILL.md) |
| **semantic-release** | Custom | Agent-driven workflow for creating git branches and conventional commits aligned with... | [./.claude/skills/semantic-release/SKILL.md](./.claude/skills/semantic-release/SKILL.md) |

## Open-source Skills

Skills from [anthropics/skills](https://github.com/anthropics/skills) registered in `skills-lock.json`.

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **frontend-design** | Open-source |  | [anthropics/skills](https://github.com/anthropics/skills) |
| **skill-creator** | Open-source |  | [anthropics/skills](https://github.com/anthropics/skills) |

## Agent Skills

Skills from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) plugin.

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **api-and-interface-design** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **browser-testing-with-devtools** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **build** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **ci-cd-and-automation** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **code-review-and-quality** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **code-simplify** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **context-engineering** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **debugging-and-error-recovery** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **deprecation-and-migration** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **documentation-and-adrs** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **doubt-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **frontend-ui-engineering** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **git-workflow-and-versioning** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **idea-refine** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **incremental-implementation** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **interview-me** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **performance-optimization** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **plan** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **planning-and-task-breakdown** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **review** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **security-and-hardening** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **ship** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **shipping-and-launch** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **source-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **spec** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **spec-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **test** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **test-driven-development** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **using-agent-skills** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |

## 🎯 Decision Trees

Guide for selecting the right skill based on your situation.

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