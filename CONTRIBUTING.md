# Contributing to OverWatch

Thank you for considering contributing to OverWatch!

## Project Maintainer

**Yasir N.**
- GitHub: [@sudoyasir](https://github.com/sudoyasir)
- Email: y451rmahar@gmail.com
- Portfolio: [sudoyasir.space](https://sudoyasir.space)

---

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
