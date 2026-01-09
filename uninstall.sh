#!/bin/bash

# Terminal Todo App Uninstaller
# Removes the todo alias from shell config

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Uninstalling Terminal Todo App..."
echo

# Check both common shell configs
CONFIGS=("$HOME/.bashrc" "$HOME/.zshrc")
FOUND=false

for CONFIG in "${CONFIGS[@]}"; do
    if [ -f "$CONFIG" ] && grep -q "alias todo=" "$CONFIG" 2>/dev/null; then
        echo "Found todo alias in $CONFIG"
        # Remove the alias line and the comment above it
        sed -i '/# Terminal Todo App/d' "$CONFIG"
        sed -i '/alias todo=/d' "$CONFIG"
        FOUND=true
        echo -e "${GREEN}Removed alias from $CONFIG${NC}"
    fi
done

if [ "$FOUND" = false ]; then
    echo -e "${YELLOW}No todo alias found in shell configuration.${NC}"
    exit 0
fi

echo
echo "Uninstall complete!"
echo "Restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc) to apply changes."
echo
echo -e "${YELLOW}Note: Your tasks in data.json have been preserved.${NC}"
echo "Delete the todo app directory manually if you want to remove everything."
