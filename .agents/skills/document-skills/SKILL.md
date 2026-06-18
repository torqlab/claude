---
name: document-skills
description: |
  Discovers all available skills and generates a dedicated SKILLS.md file in the project root with a comprehensive table organized by skill type. Extracts skills from three sources: custom skills in .kiro/skills/ and .claude/skills/, open-source skills from skills-lock.json with GitHub links, and agent skills from enabled plugins. Generates a clean, consistent markdown table format reusable across projects with columns: Skill | Type | Description | Source. Use this skill to maintain a single source of truth for skills documentation, track what's available in your project, and ensure consistent documentation structure.
license: MIT
metadata:
  author: Mr.B.Lab
---

# Skills Documentation Generation Skill

## ⚠️ CRITICAL: GENERIC AND PROJECT-AGNOSTIC DESIGN

**This skill MUST NEVER contain project-specific information or hardcoded references.**

✅ **ALLOWED**:
- Generic file paths like `.kiro/skills/`, `.claude/skills/`, `skills-lock.json`, `.claude/settings.json`
- Generic decision tree templates based on discovered skills
- Generic workflow descriptions
- Dynamic generation based on discovered skill names

❌ **FORBIDDEN**:
- Hardcoded skill names (e.g., "spec", "plan", "build" — discover from project first!)
- Project-specific tool references (e.g., "Vite", "React", "Three.js", "npm")
- Hardcoded project names or domains
- Assumptions about which skills exist
- Any content that doesn't work for projects with different skill sets

**Why?** This skill must work identically for ANY project (3D configurators, APIs, CLIs, desktop apps, etc.). All content must be generated dynamically based on discovered skills, never from hardcoded lists.

## Overview

This skill discovers all available skills from multiple sources and generates a dedicated SKILLS.md file in your project root. It maintains a single source of truth for skills inventory, organized by type with consistent markdown formatting.

## What This Skill Does

1. **Discovers all available skills** from:
   - Custom project skills in `.kiro/skills/<skill-name>/SKILL.md` and `.claude/skills/<skill-name>/SKILL.md`
   - Open-source skills defined in `skills-lock.json` with GitHub repository source links
   - Enabled plugins like agent-skills from addyosmani/agent-skills

2. **Extracts skill metadata**:
   - Skill name and description from SKILL.md frontmatter
   - Skill type (Custom, Open-source, or Agent Skill)
   - Source information with proper attribution links

3. **Generates SKILLS.md** with:
   - Dedicated file in project root: `SKILLS.md`
   - Three sections organized by skill type
   - Consistent markdown table format: `| Skill | Type | Description | Source |`
   - Proper source attribution links
   - **Dynamic decision trees** based on discovered skills (NOT hardcoded)
   - Always regenerated from scratch (no stale data)

4. **Generates decision trees** dynamically:
   - Analyzes discovered skills to identify available types
   - Creates workflows for common scenarios (implementation, debugging, quality, performance, security)
   - Only mentions skills that ACTUALLY exist in the project
   - Always up-to-date when skills are added/removed

5. **Deduplicates skills** appearing in multiple sources:
   - Open-source skills (skills-lock.json) take priority
   - Custom copies in .claude/skills/ are excluded if already open-source
   - Clean, non-redundant inventory

6. **Generates a comprehensive report** listing:
   - Total skills discovered by type
   - Lists of skills in each category
   - File generation status

## When to Use

- **After adding new skills**: Run this to update SKILLS.md with new skills
- **After removing skills**: Run this to clean up references (old skills are removed, new ones added)
- **Before releases**: Verify skill inventory is documented and current
- **During audits**: Track what skills are available in your project
- **Onboarding**: Generate reference documentation for new team members
- **Maintenance**: Keep SKILLS.md in sync as skills evolve

**Note**: SKILLS.md is always **completely regenerated from scratch** to ensure it reflects the current state of skills in your project. No stale or orphaned skill references will remain.

## Core Workflow

### Step 1: Skill Discovery

The skill scans the project for all available skills:

```
.kiro/skills/                 → Custom skills (read SKILL.md from each)
.claude/skills/               → Custom skills (read SKILL.md from each)
skills-lock.json              → Open-source skills with source repository info
.claude/settings.json         → Enabled plugins (agent skills)
```

**Categorization Logic**:
- Any skill found in `.kiro/skills/` or `.claude/skills/` that is NOT in `skills-lock.json` → **Custom**
- Any skill found in `skills-lock.json` → **Open-source** (source repository extracted and linked)
- Any skill from enabled plugins → **Agent Skill**

### Step 2: Metadata Extraction

From each skill's SKILL.md frontmatter, extract:
- `name` — skill identifier
- `description` — full description
- `license` — optional license info

### Step 3: Categorization & Deduplication

Classify each skill based on skills-lock.json:
- **Custom**: Found in `.kiro/skills/` or `.claude/skills/` but NOT in `skills-lock.json`
- **Open-source**: Listed in `skills-lock.json` (GitHub source repository extracted and linked for each)
- **Agent Skill**: From enabled plugins

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
- **Custom**: `./.kiro/skills/<name>/SKILL.md` or `./.claude/skills/<name>/SKILL.md` (local link)
- **Open-source**: Dynamic GitHub link extracted from `skills-lock.json` source field (e.g., `https://github.com/anthropics/skills`, `https://github.com/EnzeD/r3f-skills`, etc.)
- **Skills from Claude Plugins**: Dynamic GitHub link extracted from the Claude plugin information (e.g., `https://github.com/addyosmani/agent-skills` for the `addyosmani/agent-skills` Claude plugin)

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

## 🎯 Decision Trees

Guide for selecting the right skill based on your situation.

### "I need to implement a feature"
- Do you have clear requirements?
  - NO → Use `/interview-me` or `/idea-refine` to clarify, then continue
  - YES → Continue to next question
- ... (continues with full decision tree)
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

