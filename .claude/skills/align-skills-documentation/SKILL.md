---
name: align-skills-documentation
description: |
  Automatically synchronizes README.md skills documentation by discovering all available skills from custom files, open-source registries, and plugins. Use this skill whenever: new skills are added and README needs updating, you need to audit documented vs available skills, documentation has drifted from the actual skill inventory, you need comprehensive trigger patterns for when each skill should be used, you're preparing for a release and need pre-launch verification, or you're encountering missing or malformed SKILL.md files that aren't appearing in docs. This skill discovers skills from three sources (custom .claude/skills/, NPM-based skills-lock.json, and enabled plugins), extracts metadata, detects documentation gaps, and generates accurate trigger patterns organized by workflow phase. It synchronizes README tables while preserving format and adds a "Trigger Context & Usage Patterns" section with clear guidance on when each skill should be invoked. Generates audit reports showing inventory by type, documentation coverage, and any mismatches between code and documentation.
license: MIT
metadata:
  author: Mr.B.Lab
---

# Skills Documentation Alignment Skill

## Overview

This skill maintains synchronization between the project's actual skills and their documentation in README.md. It discovers all available skills from multiple sources (custom skills, NPM-based open-source skills, and enabled plugins), extracts their metadata, and ensures README documentation stays accurate and current.

## What This Skill Does

1. **Discovers all available skills** from:
   - Custom project skills in `.claude/skills/<skill-name>/SKILL.md`
   - NPM-based open-source skills defined in `skills-lock.json` (from anthropics/skills)
   - Enabled plugins in `.claude/settings.json` (agent-skills@addy-agent-skills)

2. **Extracts skill metadata**:
   - Skill name and description from SKILL.md frontmatter
   - Skill type (Custom, Open-source, or Agent Skill)
   - Source information (local path, GitHub repo reference, or plugin)
   - Trigger context (when/why to use this skill)

3. **Updates README.md** with:
   - Synchronized skills table in "📦 Skills" section
   - Accurate purpose and source attribution for each skill
   - Preserved table format: Skill | Type | Purpose | Source
   - New "Trigger Context & Usage Patterns" section with patterns for when skills should be invoked

4. **Generates a summary report** listing:
   - Skills successfully documented
   - Any skills found in code but missing from README
   - Newly added or removed skills
   - Documentation drift indicators

## When to Use

- **After adding new skills**: Run this to auto-update README
- **Before releases**: Verify all skills are properly documented
- **During audits**: Identify undocumented or orphaned skills
- **Maintenance**: Keep documentation in sync as skills evolve
- **Onboarding**: Generate comprehensive skills reference with trigger patterns

## Core Workflow

### Step 1: Skill Discovery

The skill scans the project for all available skills:

```
.claude/skills/               → Custom skills (read SKILL.md from each)
skills-lock.json              → NPM-based open-source skills
.claude/settings.json         → Enabled plugins
```

### Step 2: Metadata Extraction

From each skill's SKILL.md frontmatter, extract:
- `name` — skill identifier
- `description` — full description including when to use
- `license` — optional license info
- `metadata.author` — optional author info
- `compatibility` — optional dependencies/requirements

### Step 3: Categorization

Classify each skill:
- **Custom**: Found in `.claude/skills/<name>/`
- **Open-source**: Listed in `skills-lock.json` (source: anthropics/skills)
- **Agent Skill**: Comes from enabled plugins (source: addyosmani/agent-skills)

### Step 4: README Update

Update the "📦 Skills" section table:
- Columns: Skill | Type | Purpose | Source
- Sort by type (Custom first, then Open-source, then Agent Skills)
- Link to SKILL.md file for custom skills
- Link to source repos for open-source and agent skills

Add new "Trigger Context & Usage Patterns" section:
- Document when each skill should be invoked
- Extract trigger patterns from description
- Group by workflow phase or use case

### Step 5: Report Generation

Generate a summary documenting:
- Total skills discovered
- Skills by type (Custom, Open-source, Agent Skill)
- Any skills missing from README
- Changes from previous documentation
- Summary of added/removed/updated skills

## Implementation Notes

**Preserve existing structure**: The skill respects the current README layout and only updates the skills section.

**Extract descriptions carefully**: Use the skill description field as the "Purpose" in the table. If the description is very long, extract the first 1-2 sentences and provide a link to SKILL.md for full details.

**Handle missing metadata**: If a skill lacks proper SKILL.md structure, flag it in the report and attempt to infer metadata from available sources.

**Trigger context extraction**: Parse description fields to identify patterns like:
- "Use when..." / "Use this skill whenever..."
- "Trigger contexts..." / "When to use..."
- Action verbs indicating when the skill applies

**Source attribution**: Always link to authoritative sources:
- Custom: `./.claude/skills/<name>/SKILL.md`
- Open-source: `https://github.com/anthropics/skills` or specific file path
- Agent Skills: `https://github.com/addyosmani/agent-skills`

## Example Output

### Skills Table (Updated)

| Skill | Type | Purpose | Source |
|-------|------|---------|--------|
| **align-skills-documentation** | Custom | Auto-sync README skills documentation | [./.claude/skills/align-skills-documentation/SKILL.md](...) |
| **pr** | Custom | Create GitHub PRs with semantic-release | [./.claude/skills/pr/SKILL.md](...) |
| ... | ... | ... | ... |

### Trigger Context Section (New)

#### Custom Workflows
- **semantic-release**: Use when creating feature branches and commits for org-wide tickets with proper versioning
- **pr**: Use when you need to create or update a pull request from a semantic-release branch
- **create-changelog**: Use when generating changelog entries from git diffs

#### Documentation & Design
- **frontend-design**: Use when building web components, pages, or applications with attention to design quality
- **align-skills-documentation**: Use when maintaining skills documentation or before releases

... more patterns ...

## Output Format

The skill produces:
1. **Updated README.md** — with synchronized skills table and new trigger context section
2. **Documentation Report** — summary of discovery, changes, and any discrepancies
3. **Console output** — progress indicators and final summary

## Error Handling

If SKILL.md files are malformed or missing:
- Report the issue in the summary
- Skip that skill or attempt recovery from available metadata
- Provide recommendations for fixing undocumented skills

## Integration

This skill works alongside:
- **semantic-release** — for local workflow management
- **pr** — for remote workflow (PR creation)
- **create-changelog** — for changelog generation
- **skill-creator** — for creating and testing new skills
