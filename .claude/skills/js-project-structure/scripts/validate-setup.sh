#!/usr/bin/env bash
set -euo pipefail

# js-project-structure: validate-setup.sh
# Validates that a project is properly configured

PROJECT_DIR="${1:-.}"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Directory not found: $PROJECT_DIR"
  exit 1
fi

cd "$PROJECT_DIR"

echo "🔍 Validating project setup..."
echo ""

ERRORS=0

# Check required files
echo "📋 Checking configuration files..."
for file in package.json tsconfig.json eslint.config.mjs .prettierrc commitlint.config.js .releaserc.json .env.example .gitignore .mcp.json; do
  if [ -f "$file" ]; then
    echo "  ✅ $file"
  else
    echo "  ❌ Missing: $file"
    ((ERRORS++))
  fi
done
echo ""

# Check directories
echo "📁 Checking directories..."
for dir in .github .husky; do
  if [ -d "$dir" ]; then
    echo "  ✅ $dir/"
  else
    echo "  ❌ Missing: $dir/"
    ((ERRORS++))
  fi
done
echo ""

# Check git setup
echo "🔐 Checking git configuration..."
if [ -d ".git" ]; then
  echo "  ✅ Git repository initialized"
  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
  echo "     Current branch: $branch"
else
  echo "  ⚠️  Git repository not initialized"
fi
echo ""

# Check husky hooks
echo "🪝 Checking git hooks..."
if [ -f ".husky/commit-msg" ]; then
  echo "  ✅ commit-msg hook"
else
  echo "  ❌ Missing: .husky/commit-msg"
  ((ERRORS++))
fi

if [ -f ".husky/pre-push" ]; then
  echo "  ✅ pre-push hook"
else
  echo "  ❌ Missing: .husky/pre-push"
  ((ERRORS++))
fi
echo ""

# Check node_modules
echo "📦 Checking dependencies..."
if [ -d "node_modules" ]; then
  echo "  ✅ Dependencies installed"
else
  echo "  ⚠️  Dependencies not installed (run: bun install)"
fi
echo ""

# Check TypeScript
echo "🔷 Checking TypeScript..."
if command -v tsc &> /dev/null; then
  echo "  ✅ TypeScript installed"
else
  echo "  ⚠️  TypeScript not in PATH (run: bun install)"
fi
echo ""

# Check ESLint
echo "🔍 Checking ESLint..."
if command -v eslint &> /dev/null || [ -f "node_modules/.bin/eslint" ]; then
  echo "  ✅ ESLint installed"
else
  echo "  ⚠️  ESLint not installed (run: bun install)"
fi
echo ""

# Check Prettier
echo "✨ Checking Prettier..."
if command -v prettier &> /dev/null || [ -f "node_modules/.bin/prettier" ]; then
  echo "  ✅ Prettier installed"
else
  echo "  ⚠️  Prettier not installed (run: bun install)"
fi
echo ""

if [ $ERRORS -eq 0 ]; then
  echo "✅ All checks passed! Project is ready to use."
  echo ""
  echo "Next steps:"
  echo "  1. bun install          # Install dependencies"
  echo "  2. npm run prepare       # Install git hooks"
  echo "  3. git checkout -b feat/1-your-feature"
  echo "  4. Start coding!"
  exit 0
else
  echo "❌ Found $ERRORS issue(s). Run setup again or check SKILL.md for troubleshooting."
  exit 1
fi
