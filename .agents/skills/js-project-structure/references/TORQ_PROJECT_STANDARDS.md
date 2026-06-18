# Torq Project Standards

This document defines the standardization approach for all TypeScript/Node.js projects within the torq ecosystem.

## Philosophy

All torq projects follow a **single-source-of-truth template** approach:
- One canonical template repository (torqlab/js-project-template)
- All new projects clone and customize from this template
- Consistent tooling, git workflow, and publishing pipeline
- Low overhead for new projects, high consistency across org

## Core Standards

### 1. Version Control & Git Workflow

**Branch Naming**: `<type>/<ticket_id>-<description>`
- Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`
- Ticket ID: numeric (links to GitHub issues/Jira)
- Example: `feat/42-add-user-auth`, `fix/99-resolve-race-condition`

**Commit Format** (Conventional Commits):
```
<type>(<scope>, #<ticket_id>): <subject>

<body (optional)>

Addresses #<ticket_id>
```
- Type & Scope: Required
- Scope examples: `api`, `types`, `auth`, `db`, `ui`
- Subject: Imperative mood, lowercase, max 50 chars, no period

**Validation**: Enforced via Git hooks
- commit-msg hook: Validates format via commitlint
- pre-push hook: Validates branch name, runs linting, tests

### 2. Versioning & Publishing

**Semantic Versioning**: Automatic via semantic-release
- `feat` commits → MINOR bump (1.0.0 → 1.1.0)
- `fix` & `perf` commits → PATCH bump (1.0.0 → 1.0.1)
- `feat!` → MAJOR bump (1.0.0 → 2.0.0, breaking change)
- `chore`, `docs`, `test` → No version bump

**Publishing**: Automatic when merged to main
- Runs on GitHub Actions
- Uses OIDC Trusted Publishing (keyless, secure)
- Publishes to npm automatically
- Creates GitHub releases & tags

### 3. Code Quality

**TypeScript**: Strict mode
- `strict: true` in tsconfig.json
- Dual-format output: ESM + CommonJS
- Type declarations (.d.ts) included

**ESLint**: Code rules via eslint-config-prettier
- Immutability: Only `const`, no `let`/`var`
- Max line length: 100 characters
- JSDoc required for all functions
- Node.js built-ins use `node:` prefix

**Prettier**: Code formatting
- Print width: 100 characters
- Single quotes for strings
- Trailing commas in objects/arrays
- 2-space indentation
- Semicolons required

**Integration**: No conflicts via eslint-config-prettier
- ESLint handles logic rules (errors)
- Prettier handles formatting (style)
- ESLint rules that conflict with Prettier are disabled

### 4. Testing

**Test Runner**: Bun (built-in, zero-config)
- Located in `src/**/*.test.ts`
- Run with `bun test`
- Integrated in pre-push hook

**Coverage**: Not enforced, but encouraged
- No minimum threshold required
- Developers responsible for adequate coverage

### 5. Build & Distribution

**Build Outputs**:
- ESM: `dist/index.mjs` (modern JavaScript, tree-shakeable)
- CommonJS: `dist/index.cjs` (legacy compatibility)
- Types: `dist/index.d.ts` (TypeScript declarations)

**Build Scripts**:
```bash
bun run build        # Full build (types + ESM + CJS)
bun run build:types  # Just .d.ts files
bun run build:esm    # Just .mjs modules
bun run build:cjs    # Just .cjs modules
```

**Package Distribution**:
- Main entry: `dist/index.cjs` (CommonJS default)
- Module entry: `dist/index.mjs` (Modern tooling prefers ESM)
- Types entry: `dist/index.d.ts` (TypeScript)
- Exports configured in package.json for both formats

### 6. Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Project metadata, scripts, dependencies |
| `tsconfig.json` | TypeScript strict mode, ES2022 target |
| `eslint.config.mjs` | Code quality rules (flat config) |
| `.prettierrc` | Code formatting rules |
| `commitlint.config.js` | Commit message validation |
| `.releaserc.json` | Semantic-release configuration |
| `.mcp.json` | GitHub MCP server config |
| `.env.example` | Environment setup template |

### 7. Git Hooks

**Husky** manages two hooks:

**commit-msg** (before commit saved)
- Validates commit message format
- Enforced by commitlint
- Fails if message doesn't follow conventional format

**pre-push** (before push to remote)
- Linting check: `bun run lint`
- Format check: `bun run format:check`
- Test check: `bun test`
- Branch validation: `npx validate-branch-name`
- Fails if any check fails (push blocked)

### 8. CI/CD Workflows

**verify.yml**: Runs on pull request
- Install dependencies
- Run linting
- Run formatting check
- Run tests
- Run build
- Parallel jobs for speed

**publish.yml**: Runs on merge to main
- Install dependencies
- Run full verify pipeline
- Run semantic-release
- Publishes to npm (OIDC trusted)
- Creates GitHub release

### 9. Development Commands

```bash
bun install              # Install dependencies
bun run build            # Build project
bun run lint             # Run ESLint
bun run format           # Auto-format with Prettier
bun run format:check     # Check formatting without changes
bun test                 # Run all tests
npm run prepare          # Install git hooks
bun run clean            # Remove dist/ directory
```

### 10. Node.js Version

**Required**: Node.js 24+
- Enforced via `.nvmrc` (managed by nvm)
- TypeScript target: ES2022
- Modern JavaScript features expected

## Monorepo Pattern

For monorepos (multiple projects under torq/):

1. **Shared configuration** via symlink:
   ```bash
   ln -s ../../.claude .claude
   ```

2. **Per-project customization**:
   - Each project has own package.json (name, description)
   - Each project has own CI/CD workflow
   - Each project publishes independently to npm

3. **Benefits**:
   - One update point for shared standards
   - Independent versioning per project
   - Consistent development experience

## Standards Evolution

Standards can evolve, but changes should:
1. Be documented with rationale
2. Be applied to new projects first
3. Provide migration path for existing projects
4. Maintain backward compatibility where possible

Template repository serves as the canonical version. Changes are:
- Tagged with releases in the template repo
- Applied to new projects immediately
- Backported to existing projects via pull requests

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Semantic Release Documentation](https://semantic-release.gitbook.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [ESLint Documentation](https://eslint.org/)
- [Prettier Documentation](https://prettier.io/)
- [Bun Runtime](https://bun.sh/)
