"""
Allow running OverWatch as a Python module: python -m overwatch

This enables users to run OverWatch without installing it system-wide:
    python -m overwatch start
    python -m overwatch api
    python -m overwatch info
"""

from overwatch.cli.main import main

if __name__ == "__main__":
    main()
