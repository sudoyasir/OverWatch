#!/bin/bash

# OverWatch Quick Setup Script
# This script installs OverWatch and runs a quick test

set -e

echo "=========================================="
echo "  OverWatch Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "Error: Please run this script from the OverWatch project root directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing OverWatch..."
pip install --upgrade pip
pip install -e .

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""

# Run test
echo "Running quick test..."
python3 test_overwatch.py

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "To use OverWatch, activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "Then run commands:"
echo "  overwatch start       - Launch dashboard"
echo "  overwatch api         - Start API server"
echo "  overwatch info        - Show system info"
echo "  overwatch plugins     - List plugins"
echo "  overwatch metrics     - Show metrics"
echo "  overwatch --help      - Show all commands"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
echo ""
echo "For more information, see:"
echo "  README.md             - Main documentation"
echo "  INSTALL.md            - Installation guide"
echo "  FILE_INVENTORY.md     - Complete file list"
echo ""
