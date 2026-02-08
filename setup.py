"""
Setup configuration for OverWatch.

This file is kept for backward compatibility with older pip versions.
The primary configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Core dependencies (minimal install - dashboard only)
CORE_DEPS = [
    "psutil>=5.9.0",
    "rich>=13.0.0",
    "click>=8.0.0",
    "python-dotenv>=1.0.0",
]

# Optional feature groups
API_DEPS = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.23.0",
    "websockets>=11.0.0",
]

ALERT_DEPS = [
    "requests>=2.31.0",
]

DEV_DEPS = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "build>=0.10.0",
    "twine>=4.0.0",
    "ruff>=0.1.0",
]

setup(
    name="overwatch-monitor",
    version="0.1.0",
    author="Yasir N.",
    author_email="y451rmahar@gmail.com",
    description="Advanced system monitoring CLI tool with real-time dashboard, alerts, and REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudoyasir/overwatch",
    project_urls={
        "Bug Reports": "https://github.com/sudoyasir/overwatch/issues",
        "Source": "https://github.com/sudoyasir/overwatch",
        "Documentation": "https://github.com/sudoyasir/overwatch#readme",
        "Changelog": "https://github.com/sudoyasir/overwatch/blob/main/CHANGELOG.md",
        "Author": "https://sudoyasir.space",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Typing :: Typed",
    ],
    python_requires=">=3.10",
    install_requires=CORE_DEPS,
    extras_require={
        "api": API_DEPS,
        "alerts": ALERT_DEPS,
        "all": API_DEPS + ALERT_DEPS,
        "dev": DEV_DEPS,
    },
    entry_points={
        "console_scripts": [
            "overwatch=overwatch.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "overwatch": [
            "alerts/thresholds.json",
        ],
    },
    keywords="monitoring system-monitor cli dashboard metrics cpu memory disk network devops sysadmin",
    zip_safe=False,
)

