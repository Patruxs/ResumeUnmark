# Contributing to ResumeUnmark

Thank you for your interest in contributing to ResumeUnmark! 🎉

## Development Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/patrickzs/ResumeUnmark.git
   cd ResumeUnmark
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Project Structure

```
ResumeUnmark/
├── src/                    # Source code
│   ├── core/              # Core watermark removal logic
│   ├── cli/               # Command-line interface
│   └── utils/             # Utility functions
├── docs/                  # Web UI (GitHub Pages)
├── tests/                 # Unit tests
├── scripts/               # Build and automation scripts
└── .github/workflows/     # CI/CD pipelines
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_cleaner.py -v
```

## Code Style

We use:

- **Black** for code formatting (line length: 100)
- **Flake8** for linting
- **MyPy** for type checking

Before committing:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/ --max-line-length=100

# Type check
mypy src/
```

## Building the Executable

```bash
python scripts/build.py
```

The executable will be in the `dist/` folder.

## Contribution Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Test** your changes: `pytest`
5. **Format** your code: `black src/ tests/`
6. **Commit** with descriptive messages: `git commit -m "Add amazing feature"`
7. **Push** to your fork: `git push origin feature/amazing-feature`
8. **Create** a Pull Request

## Pull Request Guidelines

- Keep changes focused and atomic
- Update documentation for user-visible changes
- Add tests for new functionality
- Ensure all tests pass
- Include before/after screenshots for UI changes
- Write clear commit messages

## Areas for Contribution

### High Priority

- Improve watermark detection heuristics
- Add support for more watermark positions
- Performance optimizations
- Better error handling

### Medium Priority

- Web UI enhancements
- Additional output formats
- Configuration file support
- Batch processing improvements

### Low Priority

- GUI desktop application
- Additional languages support
- Theme customization

## Questions?

Open an issue or discussion on GitHub!

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to make a great tool together.
