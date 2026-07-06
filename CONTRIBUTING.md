# Contributing to Bank EDA Profiler

First off, thank you for considering contributing to `bank_eda_profiler`! It's people like you that make open-source tools great. 

Whether you want to add a new banking report, optimize a Polars query, fix a bug, or improve documentation, this guide will help you get started.

## 🚀 Getting Started

### 1. Fork and Clone
Fork the repository on GitHub and clone your fork locally:
```bash
git clone https://github.com/your-username/bank_eda_profiler.git
cd bank_eda_profiler
```

### 2. Set Up the Development Environment
We recommend using a virtual environment. Install the package in editable mode with development dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -e .[dev]
```
*(Note: If the `[dev]` tag is not yet configured in `pyproject.toml`, just use `pip install -e .` and manually install `pytest`, `black`, and `flake8`).*

### 3. Run the Tests
Ensure everything is working correctly before making changes:
```bash
pytest tests/
```

## 🛠 How to Contribute

### Adding a New Banking Report
If you want to add a new MIS report (e.g., Credit Card Delinquency Roll-Rates):
1. **Define Requirements**: Add your report's required tables, fields, and fallback logic to `bank_eda_profiler/banking/report_requirements.py`.
2. **Implement Logic**: Create a new python file in `bank_eda_profiler/banking/` (e.g., `delinquency.py`) and write the Polars/DuckDB logic to generate the report dataframe.
3. **Expose It**: Import and add a generation method for your report in `bank_eda_profiler/profiler.py` (e.g., `def generate_delinquency_report(self)`).
4. **Update CLI (Optional)**: If applicable, add it to `bank_eda_profiler/cli.py`.

### Code Style Guidelines
We adhere to standard Python styling to keep the codebase clean and readable:
- Use **Black** for code formatting.
- Use **Flake8** for linting.
- Add type hints to all new function definitions (`from typing import List, Dict, Optional`).
- Write clear, concise docstrings for new modules or complex functions.

### Submitting a Pull Request (PR)
1. Create a new branch for your feature or bugfix (`git checkout -b feature/awesome-new-report`).
2. Make your changes and commit them with descriptive commit messages.
3. Push your branch to your fork (`git push origin feature/awesome-new-report`).
4. Open a Pull Request against the `main` branch of the original repository.
5. In your PR description, clearly explain *what* you changed and *why*. Include screenshots if you changed HTML templates or dashboards!

## 🐛 Reporting Bugs
If you find a bug, please open an issue on GitHub. Include:
- A clear description of the issue.
- The version of `bank_eda_profiler` you are using.
- A minimal reproducible code example (if possible).
- The full error traceback.

## 💡 Suggesting Enhancements
Have an idea for a new feature? We'd love to hear it! Open an issue on GitHub and tag it as an "enhancement". Explain the use case and how it would benefit the financial analytics community.

---

Thank you for contributing!
