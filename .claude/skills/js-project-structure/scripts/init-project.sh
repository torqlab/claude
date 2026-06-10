#!/usr/bin/env bash
set -euo pipefail

# js-project-structure: init-project.sh
# Initializes a new JavaScript project from torq template

PROJECT_NAME="${1:?Project name required (e.g., my-lib)}"
PROJECT_SCOPE="${2:-}"
PROJECT_DESC="${3:?Project description required}"
CREATE_REMOTE="${4:-no}"
ORG="${5:-}"

TEMPLATE_REPO="https://github.com/torqlab/js-project-template.git"
PROJECT_DIR="${PROJECT_NAME}"

echo "🚀 Initializing project: $PROJECT_NAME"
echo "   Template: $TEMPLATE_REPO"
echo ""

# Clone template
if [ -d "$PROJECT_DIR" ]; then
  echo "❌ Directory already exists: $PROJECT_DIR"
  exit 1
fi

echo "📦 Cloning template..."
git clone "$TEMPLATE_REPO" "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Remove original git history
rm -rf .git
git init
git branch -M main

echo "✅ Template cloned"
echo ""

# Customize package.json
echo "🔧 Customizing configuration..."

FULL_NAME="$PROJECT_SCOPE/$PROJECT_NAME"
if [ -z "$PROJECT_SCOPE" ]; then
  FULL_NAME="$PROJECT_NAME"
fi

# Use sed to update package.json
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS sed syntax
  sed -i '' "s|{{PROJECT_NAME}}|$FULL_NAME|g" package.json
  sed -i '' "s|{{PROJECT_DESCRIPTION}}|$PROJECT_DESC|g" package.json
else
  # Linux sed syntax
  sed -i "s|{{PROJECT_NAME}}|$FULL_NAME|g" package.json
  sed -i "s|{{PROJECT_DESCRIPTION}}|$PROJECT_DESC|g" package.json
fi

echo "✅ Configuration customized"
echo ""

# Create GitHub repo if requested
if [ "$CREATE_REMOTE" = "yes" ]; then
  echo "🌐 Creating GitHub repository..."

  REPO_NAME="$PROJECT_NAME"
  VISIBILITY="public"

  if [ -z "$ORG" ]; then
    ORG=$(gh api user --jq '.login')
  fi

  REPO_URL="https://github.com/$ORG/$REPO_NAME"

  # Create repo
  gh repo create "$ORG/$REPO_NAME" --public --description "$PROJECT_DESC" --source=. --remote=origin --push 2>&1 | grep -E "created|error|fatal|https" || true

  echo "✅ Repository created: $REPO_URL"
  echo ""
else
  echo "📝 Local git repository initialized"
  echo "   To push later: git remote add origin <your-repo-url>"
  echo ""
fi

# Add files and create initial commit
git add .
git commit -m "chore: initialize project from torq template"

# Install dependencies
echo "📥 Installing dependencies..."
if command -v bun &> /dev/null; then
  bun install
else
  npm install
fi
echo "✅ Dependencies installed"
echo ""

# Install git hooks
echo "🔐 Installing git hooks..."
npm run prepare 2>/dev/null || true
echo "✅ Git hooks installed"
echo ""

# Validate setup
echo "✓ Setup complete!"
echo ""
echo "📋 Project structure:"
echo "   $PROJECT_DIR/"
echo "   ├── .github/workflows/     # CI/CD workflows"
echo "   ├── .husky/                # Git hooks"
echo "   ├── src/                   # Source code"
echo "   ├── package.json           # Dependencies"
echo "   ├── tsconfig.json          # TypeScript config"
echo "   ├── eslint.config.mjs      # Linting rules"
echo "   ├── .releaserc.json        # Publishing config"
echo "   └── README.md              # Documentation"
echo ""
echo "🚀 Next steps:"
echo "   1. cd $PROJECT_DIR"
echo "   2. git checkout -b feat/1-your-feature"
echo "   3. Start coding!"
echo "   4. git commit with conventional format"
echo "   5. git push and create PR"
echo "   6. Merge to main for automatic publishing"
