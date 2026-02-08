# ============================================================================
# OverWatch Makefile - Convenience targets for development and installation
# ============================================================================
# Usage:
#   make install          Install OverWatch (core only)
#   make install-all      Install with all features
#   make dev              Install for development
#   make run              Launch the dashboard
#   make api              Start the API server
#   make test             Run tests
#   make clean            Clean build artifacts
#   make build            Build distribution packages
#   make publish-test     Publish to TestPyPI
#   make publish          Publish to PyPI
#   make docker           Build Docker image
#   make help             Show this help
# ============================================================================

.DEFAULT_GOAL := help
SHELL := /bin/bash
PYTHON ?= python3
VENV_DIR := venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

.PHONY: help venv install install-all install-api install-alerts dev \
        run api test lint clean build publish-test publish docker \
        uninstall info check

# --- Help ---
help: ## Show available targets
	@echo ""
	@echo "  OverWatch - Advanced System Monitoring CLI"
	@echo "  ==========================================="
	@echo ""
	@echo "  Installation:"
	@grep -E '^(install|dev|uninstall)[a-zA-Z_-]*:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*##"}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  Running:"
	@grep -E '^(run|api|info)[a-zA-Z_-]*:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*##"}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  Development:"
	@grep -E '^(test|lint|clean|build|publish|docker|check)[a-zA-Z_-]*:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*##"}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# --- Virtual Environment ---
venv: ## Create virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
		$(PIP) install --upgrade pip setuptools wheel --quiet; \
		echo "Virtual environment created at $(VENV_DIR)/"; \
	else \
		echo "Virtual environment already exists"; \
	fi

# --- Installation ---
install: venv ## Install OverWatch (core: dashboard + CLI)
	@echo "Installing OverWatch (core)..."
	@$(PIP) install -e . --quiet
	@echo ""
	@echo "Done! Activate with: source $(VENV_DIR)/bin/activate"
	@echo "Then run: overwatch start"

install-all: venv ## Install OverWatch with all features (API + alerts)
	@echo "Installing OverWatch (all features)..."
	@$(PIP) install -e ".[all]" --quiet
	@echo ""
	@echo "Done! Activate with: source $(VENV_DIR)/bin/activate"
	@echo "Then run: overwatch start"

install-api: venv ## Install with API server support
	@echo "Installing OverWatch (with API)..."
	@$(PIP) install -e ".[api]" --quiet
	@echo "Done!"

install-alerts: venv ## Install with alert notifications
	@echo "Installing OverWatch (with alerts)..."
	@$(PIP) install -e ".[alerts]" --quiet
	@echo "Done!"

dev: venv ## Install for development (includes testing & linting tools)
	@echo "Installing OverWatch (development mode)..."
	@$(PIP) install -e ".[all,dev]" --quiet
	@echo ""
	@echo "Development environment ready!"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

uninstall: ## Remove OverWatch installation
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Removing virtual environment..."; \
		rm -rf $(VENV_DIR); \
	fi
	@$(PYTHON) -m pip uninstall -y overwatch-monitor 2>/dev/null || true
	@echo "OverWatch uninstalled"

# --- Running ---
run: ## Launch the terminal dashboard
	@$(VENV_BIN)/overwatch start

api: ## Start the API server
	@$(VENV_BIN)/overwatch api

info: ## Show system information
	@$(VENV_BIN)/overwatch info

# --- Development ---
test: ## Run tests
	@$(VENV_BIN)/python -m pytest -v 2>/dev/null || $(VENV_BIN)/python test_overwatch.py

lint: ## Run linter (ruff)
	@$(VENV_BIN)/ruff check overwatch/ --fix
	@$(VENV_BIN)/ruff format overwatch/

check: ## Verify installation is working
	@echo "Checking OverWatch installation..."
	@$(VENV_BIN)/overwatch version
	@echo ""
	@$(VENV_BIN)/python -c "import overwatch; print(f'Package version: {overwatch.__version__}')"
	@$(VENV_BIN)/python -c "import psutil; print(f'psutil: {psutil.__version__}')"
	@$(VENV_BIN)/python -c "import rich; print(f'rich: {rich.__version__}')" 2>/dev/null || true
	@$(VENV_BIN)/python -c "import click; print(f'click: {click.__version__}')"
	@echo ""
	@echo "All checks passed!"

clean: ## Clean build artifacts and caches
	@echo "Cleaning..."
	@rm -rf dist/ build/ *.egg-info overwatch_monitor.egg-info/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache/ .ruff_cache/ htmlcov/ .coverage
	@echo "Clean!"

# --- Building & Publishing ---
build: clean venv ## Build distribution packages
	@echo "Building OverWatch..."
	@$(PIP) install build --quiet
	@$(PYTHON_VENV) -m build
	@echo ""
	@echo "Built packages:"
	@ls -lh dist/

publish-test: build ## Publish to TestPyPI
	@$(PIP) install twine --quiet
	@$(VENV_BIN)/twine check dist/*
	@$(VENV_BIN)/twine upload --repository testpypi dist/*
	@echo ""
	@echo "Test with: pip install --index-url https://test.pypi.org/simple/ overwatch-monitor"

publish: build ## Publish to PyPI (production)
	@$(PIP) install twine --quiet
	@$(VENV_BIN)/twine check dist/*
	@echo ""
	@read -p "Publish to PyPI? This cannot be undone. (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		$(VENV_BIN)/twine upload dist/*; \
		echo "Published! Users can install with: pip install overwatch-monitor"; \
	else \
		echo "Cancelled."; \
	fi

# --- Docker ---
docker: ## Build Docker image
	@docker build -t overwatch:latest -t sudoyasir/overwatch:latest .
	@echo ""
	@echo "Run with: docker run -it overwatch:latest"
