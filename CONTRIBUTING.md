# OverWatch Development Setup

## Installation

```bash
# Install in development mode
pip install -e .
```

## Running Tests

```bash
pytest tests/
```

## Code Style

We follow PEP 8 guidelines. Use:

```bash
# Format code
black overwatch/

# Check linting
flake8 overwatch/
```

## Building Documentation

```bash
cd docs
make html
```

## Release Process

1. Update version in `setup.py` and `overwatch/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.x.x`
4. Push tag: `git push origin v0.x.x`
5. Build: `python setup.py sdist bdist_wheel`
6. Upload: `twine upload dist/*`
