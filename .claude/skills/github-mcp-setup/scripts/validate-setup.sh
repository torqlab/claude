#!/usr/bin/env bash
# Validate GitHub MCP configuration setup

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Validating GitHub MCP Configuration..."
echo ""

# Check .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env file not found${NC}"
    echo "  Create .env with: GITHUB_APP_ID, GITHUB_APP_PRIVATE_KEY_PATH, GITHUB_INSTALLATION_ID"
    exit 1
fi
echo -e "${GREEN}✓ .env file exists${NC}"

# Check .mcp.json file exists
if [ ! -f .mcp.json ]; then
    echo -e "${RED}✗ .mcp.json file not found${NC}"
    echo "  Create .mcp.json with GitHub MCP server configuration"
    exit 1
fi
echo -e "${GREEN}✓ .mcp.json file exists${NC}"

# Load environment variables from .env
export $(cat .env | grep -v '^#' | xargs)

# Validate GITHUB_APP_ID is set
if [ -z "$GITHUB_APP_ID" ]; then
    echo -e "${RED}✗ GITHUB_APP_ID not set in .env${NC}"
    exit 1
fi
echo -e "${GREEN}✓ GITHUB_APP_ID is set${NC}"

# Validate GITHUB_APP_PRIVATE_KEY_PATH is set
if [ -z "$GITHUB_APP_PRIVATE_KEY_PATH" ]; then
    echo -e "${RED}✗ GITHUB_APP_PRIVATE_KEY_PATH not set in .env${NC}"
    exit 1
fi
echo -e "${GREEN}✓ GITHUB_APP_PRIVATE_KEY_PATH is set${NC}"

# Check private key file exists
if [ ! -f "$GITHUB_APP_PRIVATE_KEY_PATH" ]; then
    echo -e "${RED}✗ Private key file not found at: $GITHUB_APP_PRIVATE_KEY_PATH${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Private key file exists${NC}"

# Check private key file is readable
if [ ! -r "$GITHUB_APP_PRIVATE_KEY_PATH" ]; then
    echo -e "${RED}✗ Private key file is not readable${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Private key file is readable${NC}"

# Validate GITHUB_INSTALLATION_ID is set
if [ -z "$GITHUB_INSTALLATION_ID" ]; then
    echo -e "${RED}✗ GITHUB_INSTALLATION_ID not set in .env${NC}"
    exit 1
fi
echo -e "${GREEN}✓ GITHUB_INSTALLATION_ID is set${NC}"

# Check .gitignore includes private key
if ! grep -q "app-private-key.pem" .gitignore 2>/dev/null; then
    echo -e "${YELLOW}⚠ Private key not in .gitignore${NC}"
    echo "  Add to .gitignore: $GITHUB_APP_PRIVATE_KEY_PATH"
else
    echo -e "${GREEN}✓ Private key in .gitignore${NC}"
fi

echo ""
echo -e "${GREEN}✅ GitHub MCP configuration looks good!${NC}"
echo ""
echo "Next: Restart Claude Code to load the GitHub MCP server"
