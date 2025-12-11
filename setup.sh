#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}[*] Setting up Pulse Scanner...${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python 3 is not installed. Please install Python 3 to continue.${NC}"
    exit 1
fi

# Get the absolute path of the project directory
INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RUN_FILE="$INSTALL_DIR/run.py"

# Make run.py executable
echo -e "${GREEN}[*] Making run.py executable...${NC}"
chmod +x "$RUN_FILE"

# Install dependencies if requirements.txt exists and is not empty
if [ -s "$INSTALL_DIR/requirements.txt" ]; then
    echo -e "${GREEN}[*] Installing dependencies...${NC}"
    pip3 install -r "$INSTALL_DIR/requirements.txt"
fi

# Create symbolic link in /usr/local/bin
SYMLINK_PATH="/usr/local/bin/pulse"

echo -e "${GREEN}[*] Creating global 'pulse' command...${NC}"
echo -e "${GREEN}[*] This may require your password for sudo access.${NC}"

# Remove existing link/file if it exists
if [ -L "$SYMLINK_PATH" ] || [ -f "$SYMLINK_PATH" ]; then
    sudo rm "$SYMLINK_PATH"
fi

# Create new symlink
if sudo ln -s "$RUN_FILE" "$SYMLINK_PATH"; then
    echo -e "${GREEN}[+] Successfully installed!${NC}"
    echo -e "${GREEN}[+] You can now run Pulse from anywhere using command:${NC}"
    echo -e "    pulse --help"
else
    echo -e "${RED}[!] Failed to create symbolic link. Please check your permissions.${NC}"
    exit 1
fi
