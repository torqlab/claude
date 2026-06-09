---
name: align-skills-documentation
description: |
  Discovers all available skills and generates a dedicated SKILLS.md file in the project root with a comprehensive table organized by skill type. Extracts skills from three sources: custom skills in .claude/skills/, open-source skills from skills-lock.json (anthropics/skills), and agent skills from enabled plugins (addyosmani/agent-skills). Generates a clean, consistent markdown table format reusable across projects with columns: Skill | Type | Description | Source. Use this skill to maintain a single source of truth for skills documentation, track what's available in your project, and ensure consistent documentation structure.
license: MIT
metadata:
  author: Mr.B.Lab
---

# Skills Documentation Generation Skill

## Overview

This skill discovers all available skills from multiple sources and generates a dedicated SKILLS.md file in your project root. It maintains a single source of truth for skills inventory, organized by type with consistent markdown formatting.

## What This Skill Does

1. **Discovers all available skills** from:
   - Custom project skills in `.claude/skills/<skill-name>/SKILL.md`
   - Open-source skills defined in `skills-lock.json` (from anthropics/skills)
   - Enabled plugins in `.claude/settings.json` (agent-skills@addy-agent-skills)

2. **Extracts skill metadata**:
   - Skill name and description from SKILL.md frontmatter
   - Skill type (Custom, Open-source, or Agent Skill)
   - Source information with proper attribution links

3. **Generates SKILLS.md** with:
   - Dedicated file in project root: `SKILLS.md`
   - Three sections organized by skill type
   - Consistent markdown table format: `| Skill | Type | Description | Source |`
   - Proper source attribution links
   - Section descriptions explaining each skill type

4. **Deduplicates skills** appearing in multiple sources:
   - Open-source skills (skills-lock.json) take priority
   - Custom copies in .claude/skills/ are excluded if already open-source
   - Clean, non-redundant inventory

5. **Generates a comprehensive report** listing:
   - Total skills discovered by type
   - Lists of skills in each category
   - File generation status

## When to Use

- **After adding new skills**: Run this to update SKILLS.md
- **Before releases**: Verify skill inventory is documented
- **During audits**: Track what skills are available
- **Onboarding**: Generate reference documentation
- **Maintenance**: Keep SKILLS.md in sync as skills evolve

## Core Workflow

### Step 1: Skill Discovery

The skill scans the project for all available skills:

```
.claude/skills/               → Custom skills (read SKILL.md from each)
skills-lock.json              → NPM-based open-source skills
.claude/settings.json         → Enabled plugins (agent skills)
```

### Step 2: Metadata Extraction

From each skill's SKILL.md frontmatter, extract:
- `name` — skill identifier
- `description` — full description
- `license` — optional license info

### Step 3: Categorization & Deduplication

Classify each skill:
- **Custom**: Found in `.claude/skills/<name>/` (unless also in skills-lock.json)
- **Open-source**: Listed in `skills-lock.json` (source: anthropics/skills)
- **Agent Skill**: From enabled plugins (source: addyosmani/agent-skills)

### Step 4: SKILLS.md Generation

Generate the file with three organized sections:

```markdown
# Available Skills

## Custom Skills
| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **skill-name** | Custom | Description | [link](path) |

## Open-source Skills
| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **skill-name** | Open-source | Description | [link](url) |

## Agent Skills
| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **skill-name** | Agent Skill | Description | [link](url) |
```

### Step 5: Report Generation

Generate a summary documenting:
- Total skills discovered
- Skills by type breakdown
- Lists of skills in each category
- File generation status

## Output Format

The skill produces:
1. **SKILLS.md** — Single source of truth for skills inventory, organized by type
2. **JSON Report** — Structured discovery report with all details
3. **Console output** — Progress indicators and summary statistics

## Markdown Table Format (Standard)

To ensure consistency across projects, this skill uses a fixed table format:

**Header**: `| Skill | Type | Description | Source |`
**Separator**: `|-------|------|-------------|--------|`

This format is:
- Easy to parse and maintain
- Consistent across all projects
- Clean and readable in markdown viewers
- Supports all skill types

## Source Attribution

Always link to authoritative sources:
- **Custom**: `./.claude/skills/<name>/SKILL.md` (local link)
- **Open-source**: `https://github.com/anthropics/skills` (GitHub repo)
- **Agent Skills**: `https://github.com/addyosmani/agent-skills` (GitHub repo)

## Example Output

```markdown
# Available Skills

This document lists all available skills organized by type.

## Custom Skills

Project-specific skills maintained in `./.claude/skills/`.

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **pr** | Custom | Create GitHub PRs with semantic-release | [./.claude/skills/pr/SKILL.md](...) |
| **semantic-release** | Custom | Create branches and conventional commits | [./.claude/skills/semantic-release/SKILL.md](...) |

## Open-source Skills

Skills from [anthropics/skills](https://github.com/anthropics/skills) registered in `skills-lock.json`.

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **frontend-design** | Open-source |  | [anthropics/skills](https://github.com/anthropics/skills) |

## Agent Skills

Skills from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) plugin.

| Skill | Type | Description | Source |
|-------|------|-------------|--------|
| **spec** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **plan** | Agent Skill |  | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
```

## Error Handling

If SKILL.md files are malformed or missing:
- Report the issue in console warnings
- Skip that skill or attempt recovery from available metadata
- Continue processing other skills

## Integration

This skill works alongside:
- **skill-creator** — for creating and testing new skills
- **semantic-release** — for managing versioning
- **pr** — for managing pull requests

