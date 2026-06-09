# TORQ Claude Configuration Collection

A shared collection of Claude configurations, skills, hooks, and conventions for the TORQ project. This repository provides a unified set of AI development tools used across multiple TORQ repositories via symlinks.

## Overview

This is a **project-level Claude collection** that serves as a centralized source of truth for Claude development practices. Every TORQ repository can reference this collection via a symlink, ensuring consistent configurations, skills, and conventions across all projects.

**Key purpose**: Enable standardized AI-driven development workflows, code generation, and automation while maintaining quality standards through shared hooks, rules, and custom skills.

## What's Included

- **Skills**: Comprehensive skill inventory organized by type (custom, open-source, agent skills)
- **Workflows**: Structured development patterns for requirements, implementation, testing, and deployment
- **Configurations**: Claude Code settings, hooks, and project conventions
- **Documentation**: SKILLS.md for complete skills reference, README.md for setup and usage

## Quick Links

- **[README.md](./README.md)** — Complete setup guide, workflow patterns, and skill integration
- **[SKILLS.md](./SKILLS.md)** — All available skills organized by type with decision trees
- **[SKILL.md files](./skills/)** — Detailed documentation for each custom skill
- **[.claude/settings.json](./.claude/settings.json)** — Plugin configuration
- **[.claude/rules/](./.claude/rules/)** — Project conventions and coding standards

## Repository Structure

```
torq/claude/
├── .claude/
│   ├── skills/              # Custom project-specific skills
│   ├── settings.json        # Plugin configuration
│   └── settings.local.json  # Local overrides
├── README.md                # Setup, workflows, and skill integration
├── SKILLS.md                # Complete skills reference with decision trees
├── package.json             # Project metadata
├── skills-lock.json         # Open-source skills registry
└── .nvmrc                   # Node version specification
```

## Support & Resources

For complete documentation on setup, workflows, and skill integration, see [README.md](./README.md).

For detailed skill documentation, see [SKILLS.md](./SKILLS.md).

For agent-skills reference, see [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main).

---

**Repository**: [@torqlab/claude](https://github.com/torqlab/claude)  
**License**: MIT  
**Maintainer**: Mr.B.Lab  
**Node**: 24.x
