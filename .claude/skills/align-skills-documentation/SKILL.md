---
name: align-skills-documentation
description: |
  Automatically synchronizes README.md and AGENTS.md documentation by discovering all available skills from custom files, open-source registries, and plugins. Use this skill whenever: new skills are added and documentation needs updating, you need to audit documented vs available skills, documentation has drifted from the actual skill inventory, you need comprehensive trigger patterns for when each skill should be used, you're preparing for a release and need pre-launch verification, agents need decision trees to understand when to combine skills, you need to document custom skill integration points within agent workflows, agents need explicit context about prerequisites and state flow between skills, or you're encountering missing or malformed SKILL.md files that aren't appearing in docs. This skill discovers skills from three sources (custom .claude/skills/, NPM-based skills-lock.json, and enabled plugins), extracts metadata, detects documentation gaps, generates accurate trigger patterns organized by workflow phase, and creates agent-friendly decision logic. It synchronizes README tables while preserving format, adds trigger context sections, generates AGENTS.md decision trees and agent combination matrices, documents custom skill integration points, and produces audit reports showing inventory by type, documentation coverage, and skill integration status.
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
   - Agent skills from AGENTS.md existing tables

2. **Extracts skill metadata**:
   - Skill name and description from SKILL.md frontmatter
   - Skill type (Custom, Open-source, or Agent Skill)
   - Source information (local path, GitHub repo reference, or plugin)
   - Trigger context (when/why to use this skill)
   - Workflow phase association (from agent-skills organization)
   - Integration points with other skills

3. **Updates README.md** with:
   - Synchronized skills table in "📦 Skills" section
   - Accurate purpose and source attribution for each skill
   - Preserved table format: Skill | Type | Purpose | Source
   - "Trigger Context & Usage Patterns" section with patterns for when skills should be invoked

4. **Updates AGENTS.md** with agent-friendly documentation:
   - Decision trees showing if-then flows for skill selection
   - Agent combinations matrix documenting workflow sequences
   - Custom skill integration guide mapping connection points
   - Agent context requirements showing prerequisites and state flow
   - Skill categorization by workflow phase

5. **Generates a comprehensive report** listing:
   - Skills successfully documented
   - Any skills found in code but missing from documentation
   - Newly added or removed skills
   - Custom skill integration points and workflow connections
   - Documentation drift indicators
   - Agent-friendly decision logic coverage

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

### Step 6: AGENTS.md Generation (New)

Generate agent-friendly documentation sections in AGENTS.md:

**6a. Decision Trees**
- Parse existing agent descriptions and "When to Use" patterns
- Create if-then cascading flows for agent selection
- Example: "I need to implement a feature" → /interview-me or /spec → /plan → /build
- Help agents choose between workflows based on problem characteristics

**6b. Agent Combinations & Context Flow**
- Map agent sequences showing workflow progressions
- Document what context/state flows between agents
- Create matrix showing: Sequence | Prerequisites | Purpose | Output Context
- Example: /spec → /plan → /build means spec output becomes plan input

**6c. Custom Skills Integration Guide**
- Identify integration points where custom skills fit into agent workflows
- Map custom skills to specific agents and phases
- Create table: Skill | Integration Point | Works With Agents | Sequence
- Example: /pr after /build completes → /build → /review → /pr

**6d. Agent Context Requirements**
- Document prerequisites and state for each agent
- Show what input agents expect and what output they produce
- Map dependencies: which agents must run before others
- Example: /plan requires /spec output; /build requires /plan output

## Implementation Notes

**Preserve existing structure**: The skill respects the current README and AGENTS.md layouts and only updates relevant sections.

**Extract descriptions carefully**: Use the skill description field as the "Purpose" in tables. If the description is very long, extract the first 1-2 sentences and provide a link to SKILL.md for full details.

**Handle missing metadata**: If a skill lacks proper SKILL.md structure, flag it in the report and attempt to infer metadata from available sources.

**Trigger context extraction**: Parse description fields to identify patterns like:
- "Use when..." / "Use this skill whenever..."
- "Trigger contexts..." / "When to use..."
- Action verbs indicating when the skill applies

**Agent-friendly decision logic**: Extract from trigger patterns:
- Conditions that determine agent selection (if-then cascades)
- State prerequisites (what must be true before using an agent)
- Integration points (where custom skills connect)
- Workflow variations (conservative, rapid, performance-critical)

**Source attribution**: Always link to authoritative sources:
- Custom: `./.claude/skills/<name>/SKILL.md`
- Open-source: `https://github.com/anthropics/skills` or specific file path
- Agent Skills: `https://github.com/addyosmani/agent-skills`

## Agent-Friendly Documentation Format

### Decision Trees (AGENTS.md section)

```markdown
## 🎯 Decision Trees

### "I need to implement a feature"
- Do you have clear requirements?
  - NO → Use /interview-me or /idea-refine, then continue
  - YES → Continue
- Have you written a spec?
  - NO → Use /spec, then continue
  - YES → Continue
- Have you planned the work?
  - NO → Use /plan, then continue
  - YES → Use /build for implementation

### "Something is broken"
- Do you know the root cause?
  - NO → Use /debugging-and-error-recovery
  - YES → Use /test (TDD approach) → Fix with /build
```

### Agent Combinations Matrix (AGENTS.md section)

```markdown
## 🔗 Agent Combinations & Context Flow

| Sequence | Prerequisites | Purpose | Output Context |
|----------|---|---------|--------|
| /spec → /plan → /build | Clear requirements | Feature development | Task list → Implementation |
| /test → /build → /review | Failing test | Bug fix | Test passes → Code reviewed |
| /debugging-and-error-recovery → /test → /build | Error symptoms | Systematic debugging | Root cause → Failing test → Fix |
```

### Custom Skills Integration (AGENTS.md section)

```markdown
## 🛠️ Custom Skills Integration Guide

| Skill | Integration Point | Works With Agents | Sequence |
|-------|-------------------|------------------|----------|
| /pr | After /build completes & ready for review | /build, /review | /build → /review → /pr |
| /create-changelog | After /build before /ship | /build, /ship | /build → /create-changelog → /ship |
| /semantic-release | During planning for branch creation | /plan, /build | /plan → /semantic-release → /build |
| /frontend-design | During /frontend-ui-engineering | /spec, /frontend-ui-engineering | /spec → /frontend-design → /frontend-ui-engineering |
```

### Agent Context Requirements (AGENTS.md section)

```markdown
## 📋 Agent Context Requirements

| Agent | Phase | Prerequisites | Input | Output | Success Criteria |
|-------|-------|---|-------|--------|------------------|
| /spec | Specification | Clear requirements | Clarified requirements | Detailed spec with acceptance criteria | Spec has clear acceptance criteria |
| /plan | Planning | Spec complete | Specification | Ordered tasks with dependencies | Tasks are ordered and dependencies clear |
| /build | Build | Task list ready | Task from plan | Tested, verified, committed code | Code changes committed to feature branch |
| /test | Testing | Code exists | Code changes or failing test | Passing tests, verified behavior | All tests passing |
| /review | Review | Code ready | Code changes to review | Review feedback or approval | All review feedback addressed |
```

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
1. **Updated README.md** — with synchronized skills table and trigger context section
2. **Updated AGENTS.md** — with decision trees, agent combinations matrix, custom skill integration guide, and agent context requirements
3. **Documentation Report** — summary of discovery, changes, discrepancies, and custom skill integration points
4. **Console output** — progress indicators and final summary

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
