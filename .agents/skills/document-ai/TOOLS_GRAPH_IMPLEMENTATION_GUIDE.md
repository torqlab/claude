# Agent Tools Graph Implementation Guide

This document outlines the implementation strategy for the Agent Tools Graph feature with document dependency discovery and reference validation.

## Architecture Overview

```
select_platform()             → "kiro" | "claude"
discover_hooks(platform)      → Hook[]
discover_agents(platform)     → Agent[]
discover_skills()             → Skill[]
extract_doc_references(hooks, agents, skills) → DocRef[]
validate_hard_references(hooks, agents, skills) → HardValidationResult
validate_soft_references(doc_refs) → SoftValidationResult
report_and_confirm(validation) → UserDecision
build_graph(hooks, agents, skills, docs, validation) → Graph
generate_mermaid(graph)       → MermaidSyntax
generate_ai_md(skills, graph) → MarkdownFile
```

## Component Breakdown

### 1. Platform Detection & User Input

```
Ask user: "Which platform should I document? (Kiro or Claude)"
Return: "kiro" or "claude"
```

### 2. Hook Discovery

#### Kiro Platform
```
For each file in .kiro/hooks/*.kiro.hook:
  Parse JSON (skip malformed with warning)
  Extract:
    - name, shortName
    - trigger_type: when.type
    - action_type: then.type
    - prompt: then.prompt (if askAgent)
    - command: then.command (if runCommand)
    
  If action_type == "askAgent":
    Extract agent references:
      Regex: invokeSubAgent\(\s*name:\s*["']([^"']+)["']
      
    Extract skill activation references:
      Regex: USE THE\s+(\S+)\s+SKILL
      
    Extract document references:
      → See "Reference Extraction Algorithm" section
```

### 3. Agent Discovery

```
For each file in .kiro/agents/*.agent.json:
  Parse JSON (skip malformed with warning)
  Extract:
    - name, displayName, description, model
    - skills: array of skill names
    - systemPrompt: full prompt text
    - autoActivateSkills
    
  Extract document references from systemPrompt:
    → See "Reference Extraction Algorithm" section
```

### 4. Skills Discovery

```
Classification priority:
1. skills-lock.json keys → Open-source
2. .kiro/skills/ or .claude/skills/ NOT in lock → Custom
3. .claude/settings.json enabledPlugins → Agent Skill

For custom skills:
  Read SKILL.md body
  Extract document references from body text
```

### 5. Reference Extraction Algorithm

This is the core new logic. Given a block of text from an AI entity, extract file references.

```
function extract_doc_references(text, entity_name, entity_type):
  references = []
  
  # --- PHASE 1: Structured reference sections ---
  # These are highest confidence. Look for labeled blocks.
  
  section_headers = [
    "KEY REFERENCE FILES",
    "REFERENCE LINKS",
    "Reference Files",
    "REFERENCE:",
  ]
  
  For each section_header found in text:
    Extract all lines in that section until next header or blank line
    For each line, extract file paths (patterns below)
    Annotate as "structured_section" confidence
  
  # --- PHASE 2: Instructional verb patterns ---
  # File paths following action verbs that indicate runtime dependency
  
  instructional_patterns = [
    (r"Authoritative source:\s*(.+\.(?:ts|md|json))", "source of truth"),
    (r"File:\s*(.+\.(?:ts|md|json|js|tsx|jsx))", "input data"),
    (r"Location:\s*(.+\.(?:ts|md|json|js|tsx|jsx))", "input data"),
    (r"Read:?\s+(.+\.(?:ts|md|json))", "input data"),
    (r"Check:?\s+(.+\.(?:ts|md|json))", "validation rules"),
    (r"Verify against:?\s+(.+\.(?:ts|md|json))", "validation rules"),
    (r"Standards:\s*(.+\.md)", "standards enforcement"),
    (r"Requirements:\s*(.+\.md)", "requirements source"),
    (r"Architecture:\s*(.+\.md)", "architecture reference"),
    (r"Skill guide:\s*(.+\.md)", "skill instructions"),
    (r"Implementation:\s*(.+\.md)", "implementation guide"),
  ]
  
  For each pattern, regex_search the text:
    For each match: add to references with extracted usage
  
  # --- PHASE 3: Bare file path patterns ---
  # Match paths that look like project file references
  
  path_regex = r'(?:^|\s|["\'])(/[a-zA-Z][\w./\-]*\.(?:ts|tsx|js|jsx|md|json))'
  Also match: ./path, .kiro/path, .claude/path, src/path
  Also match: bare root files like AGENTS.md, README.md when in enforcement context
  
  For each matched path:
    # --- FILTERING: Exclude non-references ---
    SKIP if path is inside a fenced code block (``` ... ```) that is clearly an EXAMPLE
    SKIP if path contains [ ] or < > (template)
    SKIP if preceded by "Save to:", "Output:", "Write to:"
    SKIP if part of a shell command line (starts with npm, git, npx, etc.)
    SKIP if it's a URL
    
    # --- CONTEXT ANALYSIS: Determine usage ---
    Look at surrounding text (±100 chars) to determine usage:
    - Near "standards", "rules", "enforce", "verify" → "standards enforcement"
    - Near "validate", "requirements", "constraints" → "requirements source"
    - Near "types", "interface", "TypeScript", "source of truth" → "source of truth"
    - Near "spec", "design", "architecture" → "architecture reference"
    - Near "skill", "guide", "workflow" → "skill instructions"
    - Near "schema", "Zod", "validation" → "schema/validation"
    - Default → "dependency"
    
    Add to references with entity info and usage
  
  # --- PHASE 4: Special document patterns ---
  # Detect AGENTS.md, README.md etc. referenced by name in enforcement context
  
  If text contains "AGENTS.md" in context of "verify against", "per", "standards":
    Add AGENTS.md with usage "standards enforcement"
  
  # --- DEDUPLICATION ---
  Deduplicate by (entity_name, file_path) pair
  
  return references
```

### 6. Path Normalization

```
function normalize_path(raw_path, project_root):
  # All paths are project-root-relative in the graph
  
  path = raw_path.strip()
  
  # Remove leading / (project-root-relative, NOT filesystem root)
  if path.startswith('/'):
    path = path[1:]
  
  # Remove leading ./
  if path.startswith('./'):
    path = path[2:]
  
  # Keep .kiro/ and .claude/ as-is
  # Keep src/ as-is
  
  # For bare filenames like AGENTS.md, keep as root-relative
  
  return path  # project-root-relative, no leading slash
```

### 7. Reference Validation

```
function validate_hard_references(hooks, agents, all_skill_names, all_agent_names):
  """
  Hard references MUST exist. Failure = stop generation.
  """
  errors = []
  
  # Check agent skills[] arrays
  For each agent:
    For each skill_name in agent.skills:
      if skill_name not in all_skill_names:
        errors.append({
          entity: agent.name,
          entity_type: "agent",
          ref_type: "skill",
          referenced: skill_name,
          message: f"Agent '{agent.name}' references skill '{skill_name}' which does not exist"
        })
  
  # Check hook invokeSubAgent patterns
  For each hook:
    For each agent_ref in hook.agent_references:
      if agent_ref not in all_agent_names:
        errors.append({
          entity: hook.name,
          entity_type: "hook",
          ref_type: "agent", 
          referenced: agent_ref,
          message: f"Hook '{hook.name}' references agent '{agent_ref}' which does not exist"
        })
  
  if errors:
    # STOP! Report all errors. Do NOT generate AI.md.
    report = "❌ HARD REFERENCE VALIDATION FAILED\n\n"
    report += "The following references point to entities that don't exist:\n\n"
    for err in errors:
      report += f"  - {err.message}\n"
    report += "\nFix these broken references before running document-ai."
    ERROR(report)
  
  return OK


function validate_soft_references(doc_refs, project_root):
  """
  Soft references SHOULD exist. Missing = warn, ask, mark.
  """
  broken = []
  valid = []
  
  For each ref in doc_refs:
    absolute_path = join(project_root, ref.normalized_path)
    if file_exists(absolute_path):
      valid.append(ref)
    else:
      broken.append(ref)
  
  return SoftValidationResult(valid=valid, broken=broken)


function report_and_confirm(soft_result):
  """
  If broken soft references found, notify caller and ask.
  """
  if not soft_result.broken:
    return "continue"
  
  message = f"⚠️ Found {len(soft_result.broken)} broken file reference(s):\n\n"
  
  for ref in soft_result.broken:
    message += f"  - {ref.entity_type} \"{ref.entity_name}\" → "
    message += f"\"{ref.normalized_path}\" (used for: {ref.usage})\n"
  
  message += "\nShould I continue with these marked as warnings in the output,"
  message += " or stop so you can fix them first?"
  
  decision = ask_user(message)
  # decision is "continue" or "stop"
  
  if decision == "stop":
    HALT("Generation stopped. Fix broken references and re-run.")
  
  return "continue_with_warnings"
```

### 8. Graph Construction

```
class Node:
  id: string        # e.g., "hook_review-code", "doc_AGENTS_md"
  name: string      # Display name
  type: string      # "hook" | "agent" | "skill" | "document"
  description: string
  metadata: dict    # trigger_type, model, full_path, validation_status, etc.

class Edge:
  source_id: string
  target_id: string
  label: string     # "calls", "triggers", "uses", "activates", "references: [usage]"

class Graph:
  nodes: dict       # id -> Node
  edges: list       # [Edge]


function build_graph(hooks, agents, skills, doc_refs, soft_validation):
  graph = Graph()
  
  # --- Add hook nodes ---
  For each hook:
    id = sanitize_id("hook", hook.shortName or hook.name)
    graph.nodes[id] = Node(id, hook.name, "hook", hook.description,
      {trigger_type: hook.trigger_type, action_type: hook.action_type})
  
  # --- Add agent nodes ---
  For each agent:
    id = sanitize_id("agent", agent.name)
    graph.nodes[id] = Node(id, agent.displayName or agent.name, "agent",
      agent.description, {model: agent.model})
  
  # --- Add skill nodes (only those referenced by agents) ---
  referenced_skills = set()
  For each agent:
    For each skill_name in agent.skills:
      referenced_skills.add(skill_name)
  
  For each skill_name in referenced_skills:
    id = sanitize_id("skill", skill_name)
    skill_info = find_skill_info(skill_name, all_skills)
    graph.nodes[id] = Node(id, skill_name, "skill",
      skill_info.description, {skill_type: skill_info.type})
  
  # --- Add document nodes (deduplicated by path) ---
  unique_doc_paths = deduplicate_by_path(doc_refs)
  For each path in unique_doc_paths:
    id = sanitize_id("doc", path)
    is_broken = path in [r.normalized_path for r in soft_validation.broken]
    short_name = basename(path)
    description = derive_doc_description(path, doc_refs)
    graph.nodes[id] = Node(id, short_name, "document",
      description, {
        full_path: path,
        validation_status: "broken" if is_broken else "valid"
      })
  
  # --- Add edges: Hook → Agent ---
  For each hook:
    For each agent_ref in hook.agent_references:
      source = sanitize_id("hook", hook.shortName or hook.name)
      target = sanitize_id("agent", agent_ref)
      label = "triggers" if "Task" in hook.trigger_type else "calls"
      graph.edges.append(Edge(source, target, label))
  
  # --- Add edges: Agent → Skill ---
  For each agent:
    For each skill_name in agent.skills:
      source = sanitize_id("agent", agent.name)
      target = sanitize_id("skill", skill_name)
      graph.edges.append(Edge(source, target, "uses"))
  
  # --- Add edges: Entity → Document ---
  For each doc_ref in doc_refs:
    source = get_entity_id(doc_ref.entity_name, doc_ref.entity_type)
    target = sanitize_id("doc", doc_ref.normalized_path)
    label = f"references: {doc_ref.usage}"
    graph.edges.append(Edge(source, target, label))
  
  return graph


function sanitize_id(prefix, name):
  """Create a valid Mermaid node ID from prefix + name"""
  # Replace non-alphanumeric with underscore, avoid starting with digit
  safe = re.sub(r'[^a-zA-Z0-9]', '_', name)
  return f"{prefix}_{safe}"


function derive_doc_description(path, all_refs_for_path):
  """Short description for a document node based on filename and usage context"""
  filename = basename(path)
  
  # Well-known files
  well_known = {
    "AGENTS.md": "Project development standards",
    "README.md": "Project documentation",
    "AI.md": "AI tools documentation",
    "requirements.md": "Feature requirements",
    "design.md": "Architecture & design",
    "tasks.md": "Implementation tasks",
  }
  if filename in well_known:
    return well_known[filename]
  
  # Infer from path
  if "types.ts" in path: return "Type definitions"
  if "schema" in path: return "Validation schema"
  if "constants" in path: return "Configuration constants"
  if "SKILL.md" in path: return "Skill instructions"
  if "/specs/" in path: return "Specification document"
  
  # Fall back to aggregated usage from references
  usages = set(r.usage for r in all_refs_for_path)
  if usages:
    return ", ".join(sorted(usages))
  
  return "Project file"
```

### 9. Mermaid Generation

```
function generate_mermaid(graph):
  lines = ["graph TD"]
  
  # Separate nodes by type
  hooks = [n for n in graph.nodes.values() if n.type == "hook"]
  agents = [n for n in graph.nodes.values() if n.type == "agent"]
  skills = [n for n in graph.nodes.values() if n.type == "skill"]
  docs_valid = [n for n in graph.nodes.values() 
    if n.type == "document" and n.metadata.get("validation_status") == "valid"]
  docs_broken = [n for n in graph.nodes.values()
    if n.type == "document" and n.metadata.get("validation_status") == "broken"]
  
  # --- Hooks sub-graph ---
  if hooks:
    lines.append('    subgraph Hooks["🪝 Hooks (Trigger Automation)"]')
    for node in sorted(hooks, key=lambda n: n.name):
      label = format_hook_label(node)
      lines.append(f'        {node.id}["{label}"]')
    lines.append('    end')
  
  # --- Agents sub-graph ---
  if agents:
    lines.append('    subgraph Agents["🤖 Agents (Execute Tasks)"]')
    for node in sorted(agents, key=lambda n: n.name):
      label = format_agent_label(node)
      lines.append(f'        {node.id}["{label}"]')
    lines.append('    end')
  
  # --- Skills sub-graph ---
  if skills:
    lines.append('    subgraph Skills["💡 Skills (Capabilities)"]')
    for node in sorted(skills, key=lambda n: n.name):
      label = format_skill_label(node)
      lines.append(f'        {node.id}["{label}"]')
    lines.append('    end')
  
  # --- Documents sub-graph (valid) ---
  if docs_valid:
    lines.append('    subgraph Documents["📄 Referenced Documents"]')
    for node in sorted(docs_valid, key=lambda n: n.name):
      label = format_doc_label(node)
      lines.append(f'        {node.id}["{label}"]')
    lines.append('    end')
  
  # --- Broken references sub-graph ---
  if docs_broken:
    lines.append('    subgraph BrokenRefs["⚠️ Broken References"]')
    for node in docs_broken:
      label = f"<b>⚠️ {node.name}</b><br/>{node.metadata['full_path']}<br/>FILE NOT FOUND"
      lines.append(f'        {node.id}["{label}"]')
    lines.append('    end')
  
  # --- Add edges ---
  for edge in graph.edges:
    source = edge.source_id
    target = edge.target_id
    label = edge.label
    
    # Check if target is a broken document
    target_node = graph.nodes.get(target)
    if target_node and target_node.type == "document" \
       and target_node.metadata.get("validation_status") == "broken":
      lines.append(f'    {source} -.->|"{label} ⚠️"| {target}')
    else:
      lines.append(f'    {source} -->|"{label}"| {target}')
  
  # --- Styling ---
  lines.append('')
  lines.append('    %% Styling')
  for node in hooks:
    lines.append(f'    style {node.id} fill:#bbdefb,stroke:#1976d2,stroke-width:2px,color:#000')
  for node in agents:
    lines.append(f'    style {node.id} fill:#c8e6c9,stroke:#388e3c,stroke-width:2px,color:#000')
  for node in skills:
    lines.append(f'    style {node.id} fill:#ffe0b2,stroke:#f57c00,stroke-width:2px,color:#000')
  for node in docs_valid:
    lines.append(f'    style {node.id} fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px,color:#000')
  for node in docs_broken:
    lines.append(f'    style {node.id} fill:#fff9c4,stroke:#f9a825,stroke-width:3px,stroke-dasharray:5 5,color:#000')
  
  return '\n'.join(lines)


function format_hook_label(node):
  trigger_map = {
    "userTriggered": "Manual",
    "postTaskExecution": "Task Completed",
    "fileEdited": "File Changed",
    "fileCreated": "File Created",
    "promptSubmit": "Prompt Submit",
  }
  trigger = trigger_map.get(node.metadata.get("trigger_type", ""), "Unknown")
  desc = truncate(node.description, 45)
  return f"<b>{node.name}</b><br/>Trigger: {trigger}<br/>{desc}"

function format_agent_label(node):
  model = node.metadata.get("model", "")
  desc = truncate(node.description, 45)
  parts = [f"<b>{node.name}</b>", desc]
  if model:
    parts.append(f"Model: {model}")
  return "<br/>".join(parts)

function format_skill_label(node):
  skill_type = node.metadata.get("skill_type", "").replace("-", " ").title()
  desc = truncate(node.description, 45)
  return f"<b>{node.name}</b><br/>Type: {skill_type}<br/>{desc}"

function format_doc_label(node):
  path = node.metadata.get("full_path", "")
  desc = truncate(node.description, 35)
  return f"<b>{node.name}</b><br/>{path}<br/>{desc}"
```

### 10. AI.md Generation

```
function generate_ai_md(skills_inventory, graph, doc_refs, validation):
  sections = []
  
  # Header
  sections.append("# Available AI Tools\n")
  sections.append("[intro text]\n")
  
  # Skills tables (existing logic, unchanged)
  sections.append(generate_custom_skills_section(skills_inventory))
  sections.append(generate_opensource_skills_section(skills_inventory))
  sections.append(generate_agent_skills_section(skills_inventory))
  
  # Decision Trees (existing logic)
  sections.append(generate_decision_trees(skills_inventory))
  
  # Agent Tools Graph (NEW: includes documents)
  sections.append("## 🔗 Agent Tools Graph\n")
  sections.append(generate_graph_legend())  # includes Document type
  sections.append(f"```mermaid\n{generate_mermaid(graph)}\n```\n")
  
  # Document Dependencies table (NEW)
  sections.append("### Document Dependencies\n")
  sections.append(generate_doc_dependencies_table(doc_refs))
  
  # Active Workflows
  sections.append(generate_workflows_section(graph))
  
  # Broken References (if any)
  if validation.broken:
    sections.append("### ⚠️ Broken References\n")
    sections.append(generate_broken_refs_table(validation.broken))
  
  # Summary
  sections.append(generate_summary(skills_inventory, graph, validation))
  
  return "\n".join(sections)


function generate_doc_dependencies_table(doc_refs):
  """Generate markdown table showing which entities reference which documents"""
  # Group by document path
  by_path = group_by(doc_refs, key=lambda r: r.normalized_path)
  
  table = "| Document | Referenced By | Usage |\n"
  table += "| --- | --- | --- |\n"
  
  for path in sorted(by_path.keys()):
    refs = by_path[path]
    doc_name = basename(path)
    entities = ", ".join(sorted(set(r.entity_name for r in refs)))
    usages = ", ".join(sorted(set(r.usage for r in refs)))
    table += f"| {doc_name} | {entities} | {usages} |\n"
  
  return table
```

### 11. Error Handling

```
function safe_load_json(filepath):
  """Load JSON with error handling — skip malformed files"""
  try:
    return parse_json(read_file(filepath))
  except JSONParseError as e:
    console.warn(f"⚠️ Malformed JSON in {filepath}: {e} — skipping")
    return None
  except FileNotFoundError:
    console.warn(f"⚠️ File not found: {filepath} — skipping")
    return None
```

## Implementation Checklist

### Core Discovery
- [ ] Platform detection (ask Kiro or Claude)
- [ ] Hook discovery for selected platform
- [ ] Agent discovery for selected platform
- [ ] Skills discovery (existing logic, unchanged)

### Document Reference Discovery (NEW)
- [ ] Reference extraction from hook prompts
- [ ] Reference extraction from agent systemPrompts
- [ ] Reference extraction from custom skill SKILL.md bodies
- [ ] Path normalization (project-root-relative)
- [ ] Usage annotation derivation from context
- [ ] Filtering of non-references (examples, templates, commands)
- [ ] Deduplication by file path

### Reference Validation (NEW)
- [ ] Hard validation: skill existence (agent skills arrays)
- [ ] Hard validation: agent existence (hook invokeSubAgent patterns)
- [ ] Soft validation: file existence on disk
- [ ] Broken reference reporting to caller
- [ ] User confirmation flow (continue with warnings vs stop)

### Graph Construction
- [ ] Four node types: hook, agent, skill, document
- [ ] Edge creation with usage annotations
- [ ] Broken reference marking (validation_status field)
- [ ] Node ID sanitization for Mermaid compatibility
- [ ] Isolated node inclusion

### Mermaid Generation
- [ ] Four sub-graphs (hooks, agents, skills, documents + broken)
- [ ] Five color schemes (blue, green, orange, purple, yellow-dashed)
- [ ] Rich node labels
- [ ] Annotated edge labels
- [ ] Dashed edges for broken references
- [ ] Valid Mermaid syntax

### AI.md Output
- [ ] Skills inventory sections
- [ ] Decision trees
- [ ] Agent Tools Graph with legend (4 node types)
- [ ] Document Dependencies table
- [ ] Active Workflows
- [ ] Broken References section (conditional)
- [ ] Summary with document and broken ref counts

## Testing Strategy

1. **Reference extraction**: Test against real hook/agent content — verify correct paths extracted, examples excluded
2. **Validation**: Create a test case with one broken path → verify soft validation triggers
3. **Hard validation**: Reference a non-existent skill in an agent → verify error stops generation
4. **Graph construction**: Verify document nodes appear and edges have usage annotations
5. **Mermaid output**: Validate syntax renders in a Mermaid viewer
6. **Deduplication**: Same file referenced by 3 entities → 1 node, 3 edges
7. **Edge cases**: Empty hooks dir, malformed JSON, huge prompts
