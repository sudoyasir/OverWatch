#!/usr/bin/env bash
# ============================================================================
# OverWatch Universal Installer
# ============================================================================
# One-command install for Linux, macOS, and WSL.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/sudoyasir/overwatch/main/install.sh | bash
#   wget -qO- https://raw.githubusercontent.com/sudoyasir/overwatch/main/install.sh | bash
#
# Options (set as env vars before running):
#   OVERWATCH_INSTALL_DIR  - Where to clone (default: ~/.overwatch)
#   OVERWATCH_NO_VENV      - Set to 1 to skip virtual environment
#   OVERWATCH_EXTRAS       - Extras to install: "all", "api", "alerts" (default: "all")
#
# Author: Yasir N. (@sudoyasir)
# ============================================================================

set -euo pipefail

# --- Configuration ---
REPO_URL="https://github.com/sudoyasir/overwatch.git"
INSTALL_DIR="${OVERWATCH_INSTALL_DIR:-$HOME/.overwatch}"
USE_VENV="${OVERWATCH_NO_VENV:-0}"
EXTRAS="${OVERWATCH_EXTRAS:-all}"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=10

# --- Colors & Formatting ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

info()    { echo -e "${BLUE}[INFO]${NC} $*"; }
success() { echo -e "${GREEN}[OK]${NC} $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
fatal()   { error "$@"; exit 1; }

header() {
    echo ""
    echo -e "${CYAN}${BOLD}============================================${NC}"
    echo -e "${CYAN}${BOLD}  OverWatch Installer${NC}"
    echo -e "${CYAN}${BOLD}  Advanced System Monitoring CLI Tool${NC}"
    echo -e "${CYAN}${BOLD}============================================${NC}"
    echo ""
}

# --- OS Detection ---
detect_os() {
    OS="unknown"
    DISTRO="unknown"
    PKG_MANAGER="unknown"

    case "$(uname -s)" in
        Linux*)
            OS="linux"
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                DISTRO="${ID:-unknown}"
            fi
            # Detect package manager
            if command -v apt-get &>/dev/null; then
                PKG_MANAGER="apt"
            elif command -v dnf &>/dev/null; then
                PKG_MANAGER="dnf"
            elif command -v yum &>/dev/null; then
                PKG_MANAGER="yum"
            elif command -v pacman &>/dev/null; then
                PKG_MANAGER="pacman"
            elif command -v zypper &>/dev/null; then
                PKG_MANAGER="zypper"
            elif command -v apk &>/dev/null; then
                PKG_MANAGER="apk"
            fi
            ;;
        Darwin*)
            OS="macos"
            DISTRO="macos"
            if command -v brew &>/dev/null; then
                PKG_MANAGER="brew"
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            OS="windows"
            DISTRO="windows"
            ;;
    esac

    info "Detected: OS=${OS}, Distro=${DISTRO}, Package Manager=${PKG_MANAGER}"
}

# --- Dependency Checks ---
check_command() {
    command -v "$1" &>/dev/null
}

check_python() {
    local python_cmd=""
    
    # Try python3 first, then python
    for cmd in python3 python; do
        if check_command "$cmd"; then
            local ver
            ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
            local major minor
            major=$(echo "$ver" | cut -d. -f1)
            minor=$(echo "$ver" | cut -d. -f2)
            
            if [ "$major" -ge "$MIN_PYTHON_MAJOR" ] && [ "$minor" -ge "$MIN_PYTHON_MINOR" ]; then
                python_cmd="$cmd"
                success "Found $cmd ($ver)"
                break
            else
                warn "$cmd version $ver found, but >= ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR} required"
            fi
        fi
    done

    if [ -z "$python_cmd" ]; then
        return 1
    fi

    PYTHON_CMD="$python_cmd"
    return 0
}

install_python() {
    info "Attempting to install Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+..."
    
    case "$PKG_MANAGER" in
        apt)
            sudo apt-get update -qq
            sudo apt-get install -y python3 python3-pip python3-venv
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip
            ;;
        yum)
            sudo yum install -y python3 python3-pip
            ;;
        pacman)
            sudo pacman -Sy --noconfirm python python-pip
            ;;
        zypper)
            sudo zypper install -y python3 python3-pip
            ;;
        apk)
            sudo apk add python3 py3-pip
            ;;
        brew)
            brew install python@3.12
            ;;
        *)
            fatal "Cannot auto-install Python. Please install Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ manually:
    - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv
    - Fedora:        sudo dnf install python3 python3-pip
    - Arch:          sudo pacman -S python python-pip
    - macOS:         brew install python@3.12
    - Windows:       https://www.python.org/downloads/"
            ;;
    esac
    
    # Re-check after install
    if ! check_python; then
        fatal "Python installation failed. Please install Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ manually."
    fi
}

install_git() {
    if check_command git; then
        success "Git is installed"
        return 0
    fi

    info "Installing git..."
    case "$PKG_MANAGER" in
        apt)    sudo apt-get update -qq && sudo apt-get install -y git ;;
        dnf)    sudo dnf install -y git ;;
        yum)    sudo yum install -y git ;;
        pacman) sudo pacman -Sy --noconfirm git ;;
        zypper) sudo zypper install -y git ;;
        apk)    sudo apk add git ;;
        brew)   brew install git ;;
        *)      fatal "Please install git manually." ;;
    esac
    success "Git installed"
}

# --- Installation Methods ---
install_via_pip() {
    info "Installing OverWatch via pip..."
    
    if [ "$EXTRAS" = "none" ] || [ "$EXTRAS" = "core" ]; then
        "$PYTHON_CMD" -m pip install --user overwatch-monitor 2>/dev/null || \
        "$PYTHON_CMD" -m pip install overwatch-monitor
    else
        "$PYTHON_CMD" -m pip install --user "overwatch-monitor[${EXTRAS}]" 2>/dev/null || \
        "$PYTHON_CMD" -m pip install "overwatch-monitor[${EXTRAS}]"
    fi
}

install_via_pipx() {
    info "Installing OverWatch via pipx (isolated environment)..."
    
    if ! check_command pipx; then
        info "Installing pipx first..."
        "$PYTHON_CMD" -m pip install --user pipx 2>/dev/null || \
        "$PYTHON_CMD" -m pip install pipx
        "$PYTHON_CMD" -m pipx ensurepath
    fi
    
    pipx install "overwatch-monitor[${EXTRAS}]"
}

install_from_source() {
    info "Installing OverWatch from source..."
    
    # Clone or update
    if [ -d "$INSTALL_DIR" ]; then
        info "Updating existing installation..."
        cd "$INSTALL_DIR"
        git pull --rebase origin main 2>/dev/null || git pull origin main
    else
        info "Cloning OverWatch repository..."
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi

    # Virtual environment
    if [ "$USE_VENV" != "1" ]; then
        VENV_DIR="$INSTALL_DIR/venv"
        if [ ! -d "$VENV_DIR" ]; then
            info "Creating virtual environment..."
            "$PYTHON_CMD" -m venv "$VENV_DIR"
        fi
        
        # Activate
        # shellcheck disable=SC1091
        source "$VENV_DIR/bin/activate"
        success "Virtual environment activated"
    fi

    # Upgrade pip
    "$PYTHON_CMD" -m pip install --upgrade pip setuptools wheel --quiet

    # Install with extras
    if [ "$EXTRAS" = "none" ] || [ "$EXTRAS" = "core" ]; then
        "$PYTHON_CMD" -m pip install -e . --quiet
    else
        "$PYTHON_CMD" -m pip install -e ".[${EXTRAS}]" --quiet
    fi

    success "OverWatch installed from source"
}

# --- PATH Configuration ---
setup_path() {
    local shell_rc=""
    local bin_path=""

    # Determine the binary location
    if [ "$USE_VENV" != "1" ] && [ -d "$INSTALL_DIR/venv" ]; then
        bin_path="$INSTALL_DIR/venv/bin"
    else
        # pip --user installs to ~/.local/bin
        bin_path="$HOME/.local/bin"
    fi

    # Check if already in PATH
    if echo "$PATH" | grep -q "$bin_path"; then
        return 0
    fi

    # Determine shell config file
    local current_shell
    current_shell=$(basename "${SHELL:-/bin/bash}")
    case "$current_shell" in
        zsh)  shell_rc="$HOME/.zshrc" ;;
        bash)
            if [ -f "$HOME/.bash_profile" ]; then
                shell_rc="$HOME/.bash_profile"
            else
                shell_rc="$HOME/.bashrc"
            fi
            ;;
        fish) shell_rc="$HOME/.config/fish/config.fish" ;;
        *)    shell_rc="$HOME/.profile" ;;
    esac

    if [ -n "$shell_rc" ] && [ -f "$shell_rc" ]; then
        if ! grep -q "$bin_path" "$shell_rc" 2>/dev/null; then
            echo "" >> "$shell_rc"
            echo "# OverWatch - System Monitor" >> "$shell_rc"
            if [ "$current_shell" = "fish" ]; then
                echo "set -gx PATH $bin_path \$PATH" >> "$shell_rc"
            else
                echo "export PATH=\"$bin_path:\$PATH\"" >> "$shell_rc"
            fi
            info "Added $bin_path to PATH in $shell_rc"
            warn "Run 'source $shell_rc' or restart your terminal to use 'overwatch' command"
        fi
    fi
}

# --- Verification ---
verify_install() {
    echo ""
    info "Verifying installation..."
    
    # Try direct command
    if check_command overwatch; then
        success "OverWatch is available as 'overwatch' command"
        overwatch version 2>/dev/null || true
        return 0
    fi

    # Try via venv
    if [ -f "$INSTALL_DIR/venv/bin/overwatch" ]; then
        success "OverWatch installed in virtual environment"
        "$INSTALL_DIR/venv/bin/overwatch" version 2>/dev/null || true
        return 0
    fi

    # Try as module
    if "$PYTHON_CMD" -m overwatch version &>/dev/null; then
        success "OverWatch available via: python -m overwatch"
        return 0
    fi

    warn "OverWatch installed but may not be in PATH yet"
    return 0
}

# --- Uninstall ---
uninstall() {
    echo ""
    info "Uninstalling OverWatch..."
    
    # Remove pip installation
    "$PYTHON_CMD" -m pip uninstall -y overwatch-monitor 2>/dev/null || true
    
    # Remove source directory
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
        success "Removed $INSTALL_DIR"
    fi
    
    success "OverWatch uninstalled"
    exit 0
}

# --- Main ---
main() {
    header

    # Handle --uninstall flag
    if [ "${1:-}" = "--uninstall" ] || [ "${1:-}" = "uninstall" ]; then
        detect_os
        check_python || fatal "Python not found"
        uninstall
    fi

    # Step 1: Detect OS
    info "Step 1/5: Detecting system..."
    detect_os

    # Step 2: Check/Install Python
    info "Step 2/5: Checking Python..."
    if ! check_python; then
        warn "Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ not found"
        install_python
    fi

    # Step 3: Check/Install Git
    info "Step 3/5: Checking Git..."
    install_git

    # Step 4: Install OverWatch
    info "Step 4/5: Installing OverWatch..."
    echo ""
    echo -e "  Choose installation method:"
    echo -e "  ${BOLD}1)${NC} pip install (from PyPI) ${GREEN}← Recommended${NC}"
    echo -e "  ${BOLD}2)${NC} pipx install (isolated, great for CLI tools)"
    echo -e "  ${BOLD}3)${NC} Install from source (for development)"
    echo ""
    
    # Default to pip if non-interactive (piped input)
    if [ -t 0 ]; then
        read -rp "  Enter choice [1/2/3] (default: 1): " method
    else
        method="3"  # Default to source when running via curl pipe
        info "Non-interactive mode: installing from source"
    fi

    case "${method:-1}" in
        1) install_via_pip ;;
        2) install_via_pipx ;;
        3) install_from_source ;;
        *) install_via_pip ;;
    esac

    # Step 5: Configure PATH and verify
    info "Step 5/5: Finalizing..."
    setup_path
    verify_install

    # Done!
    echo ""
    echo -e "${GREEN}${BOLD}============================================${NC}"
    echo -e "${GREEN}${BOLD}  OverWatch installed successfully!${NC}"
    echo -e "${GREEN}${BOLD}============================================${NC}"
    echo ""
    echo -e "  ${BOLD}Quick Start:${NC}"
    
    if [ -d "$INSTALL_DIR/venv" ] && [ "$USE_VENV" != "1" ]; then
        echo -e "    source ${INSTALL_DIR}/venv/bin/activate"
    fi
    
    echo -e "    overwatch start       ${CYAN}# Launch dashboard${NC}"
    echo -e "    overwatch api         ${CYAN}# Start API server${NC}"
    echo -e "    overwatch info        ${CYAN}# System information${NC}"
    echo -e "    overwatch --help      ${CYAN}# All commands${NC}"
    echo ""
    echo -e "  ${BOLD}Alternative:${NC}"
    echo -e "    python -m overwatch start"
    echo ""
    echo -e "  ${BOLD}Documentation:${NC} https://github.com/sudoyasir/overwatch"
    echo -e "  ${BOLD}Issues:${NC}         https://github.com/sudoyasir/overwatch/issues"
    echo ""
}

main "$@"
