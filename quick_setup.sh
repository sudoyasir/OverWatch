#!/bin/bash

# ============================================================================
# OverWatch Quick Setup Script
# ============================================================================
# Sets up OverWatch in under 30 seconds with automatic dependency handling.
#
# Usage:
#   ./quick_setup.sh              Install with all features (default)
#   ./quick_setup.sh core         Install core only (dashboard + CLI)
#   ./quick_setup.sh api          Install with API server
#   ./quick_setup.sh dev          Install for development
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

INSTALL_MODE="${1:-all}"

echo ""
echo -e "${CYAN}${BOLD}=========================================="
echo -e "  OverWatch Quick Setup"
echo -e "==========================================${NC}"
echo ""

# Check Python version
echo -e "${BOLD}[1/4] Checking Python...${NC}"

PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        ver=$("$cmd" -c "import sys; v=sys.version_info; print(f'{v.major}.{v.minor}')" 2>/dev/null || echo "0.0")
        major=$(echo "$ver" | cut -d. -f1)
        minor=$(echo "$ver" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON_CMD="$cmd"
            echo -e "  ${GREEN}✓${NC} Found $cmd ($ver)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "  ${RED}✗ Python 3.10+ required but not found${NC}"
    echo ""
    echo "  Install Python first:"
    echo "    Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "    Fedora:        sudo dnf install python3 python3-pip"
    echo "    macOS:         brew install python@3.12"
    echo "    Windows:       https://www.python.org/downloads/"
    exit 1
fi

# Check we're in the right directory
if [ ! -f "setup.py" ] && [ ! -f "pyproject.toml" ]; then
    echo -e "  ${RED}✗ Please run from the OverWatch project root directory${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${BOLD}[2/4] Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo -e "  ${GREEN}✓${NC} Virtual environment created"
else
    echo -e "  ${GREEN}✓${NC} Virtual environment exists"
fi

# Activate and install
source venv/bin/activate

echo ""
echo -e "${BOLD}[3/4] Installing OverWatch (${INSTALL_MODE})...${NC}"
pip install --upgrade pip setuptools wheel --quiet

case "$INSTALL_MODE" in
    core)
        pip install -e . --quiet
        echo -e "  ${GREEN}✓${NC} Core installed (dashboard + CLI)"
        ;;
    api)
        pip install -e ".[api]" --quiet
        echo -e "  ${GREEN}✓${NC} Installed with API server"
        ;;
    alerts)
        pip install -e ".[alerts]" --quiet
        echo -e "  ${GREEN}✓${NC} Installed with alert notifications"
        ;;
    dev)
        pip install -e ".[all,dev]" --quiet
        echo -e "  ${GREEN}✓${NC} Development environment ready"
        ;;
    all|*)
        pip install -e ".[all]" --quiet
        echo -e "  ${GREEN}✓${NC} All features installed"
        ;;
esac

# Verify
echo ""
echo -e "${BOLD}[4/4] Verifying installation...${NC}"
if overwatch version &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} OverWatch CLI working"
    overwatch version
else
    echo -e "  ${YELLOW}⚠ CLI not in PATH, but module works:${NC}"
    python -m overwatch version
fi

echo ""
echo -e "${GREEN}${BOLD}=========================================="
echo -e "  Setup Complete!"
echo -e "==========================================${NC}"
echo ""
echo -e "  ${BOLD}Activate the environment:${NC}"
echo -e "    source venv/bin/activate"
echo ""
echo -e "  ${BOLD}Commands:${NC}"
echo -e "    overwatch start       ${CYAN}# Launch dashboard${NC}"
echo -e "    overwatch api         ${CYAN}# Start API server${NC}"
echo -e "    overwatch info        ${CYAN}# System information${NC}"
echo -e "    overwatch metrics     ${CYAN}# Current metrics${NC}"
echo -e "    overwatch plugins     ${CYAN}# List plugins${NC}"
echo -e "    overwatch --help      ${CYAN}# All commands${NC}"
echo ""
echo -e "  ${BOLD}Alternative (no activation needed):${NC}"
echo -e "    python -m overwatch start"
echo -e "    ./venv/bin/overwatch start"
echo ""
echo -e "  ${BOLD}Deactivate:${NC}"
echo -e "    deactivate"
echo ""
