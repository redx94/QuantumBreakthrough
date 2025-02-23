# Contributing to Quantum Breakthrough

We welcome contributions from quantum physicists, AI developers, and all interested collaborators.

## Code Style Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Testing

- Write unit tests for all new functionality
- Use pytest for testing
- Ensure all tests pass before submitting PR
- Maintain minimum 80% code coverage

## Pull Request Process

1. Create a feature branch from `develop`
2. Update documentation as needed
3. Add tests for new functionality
4. Submit PR with clear description of changes

## Development Setup

```bash
# Setup development environment
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 src tests
