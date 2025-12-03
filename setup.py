"""
Setup configuration for OverWatch.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="overwatch",
    version="0.1.0",
    author="Yasir N.",
    author_email="y451rmahar@gmail.com",
    description="Advanced system monitoring CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudoyasir/overwatch",
    project_urls={
        "Bug Reports": "https://github.com/sudoyasir/overwatch/issues",
        "Source": "https://github.com/sudoyasir/overwatch",
        "Portfolio": "https://sudoyasir.space",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "psutil>=5.9.0",
        "rich>=13.0.0",
        "click>=8.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "requests>=2.31.0",
        "websockets>=11.0.0",
    ],
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
    keywords="monitoring system-monitor cli dashboard metrics",
    project_urls={
        "Bug Reports": "https://github.com/sudoyasir/overwatch/issues",
        "Source": "https://github.com/sudoyasir/overwatch",
    },
)
