#!/bin/bash

# Terminal Todo App Installer
# Detects shell and adds the todo alias

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALIAS_LINE="alias todo=\"python3 $SCRIPT_DIR/main.py\""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Installing Terminal Todo App..."
echo

# Check Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Determine shell config file
detect_shell_config() {
    if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "$(which zsh)" ]; then
        echo "$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ] || [ "$SHELL" = "$(which bash)" ]; then
        echo "$HOME/.bashrc"
    else
        # Fallback: check which config files exist
        if [ -f "$HOME/.zshrc" ]; then
            echo "$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            echo "$HOME/.bashrc"
        else
            echo ""
        fi
    fi
}

SHELL_CONFIG=$(detect_shell_config)

if [ -z "$SHELL_CONFIG" ]; then
    echo -e "${RED}Error: Could not detect shell configuration file.${NC}"
    echo "Please manually add this line to your shell config:"
    echo "  $ALIAS_LINE"
    exit 1
fi

echo "Detected shell config: $SHELL_CONFIG"

# Check if alias already exists
if grep -q "alias todo=" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${YELLOW}Warning: A 'todo' alias already exists in $SHELL_CONFIG${NC}"
    read -p "Do you want to replace it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    # Remove existing alias
    sed -i '/alias todo=/d' "$SHELL_CONFIG"
fi

# Add alias to shell config
echo "" >> "$SHELL_CONFIG"
echo "# Terminal Todo App" >> "$SHELL_CONFIG"
echo "$ALIAS_LINE" >> "$SHELL_CONFIG"

echo -e "${GREEN}Successfully installed!${NC}"
echo
echo "To start using todo, either:"
echo "  1. Run: source $SHELL_CONFIG"
echo "  2. Or restart your terminal"
echo
echo "Then try: todo help"
