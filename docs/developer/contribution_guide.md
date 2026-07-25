# Contribution Guide

Thank you for contributing to PHOENIX! Please follow these standards.

## 1. Development Workflow
1. Fork the repository and create a feature branch (`feature/ISSUE-123-short-description`).
2. Implement your changes following the SOLID principles defined in our Architecture Reference.
3. Ensure all new functions include Python type hints.
4. Run the local test suite via `pytest backend/tests/`.
5. Submit a Pull Request targeting the `main` branch.

## 2. CI/CD Requirements
All Pull Requests must pass the automated GitHub Actions pipeline (`ci.yml`) before merging. The pipeline enforces:
- **MyPy**: Static type checking.
- **Bandit**: Python SAST (Static Application Security Testing).
- **TruffleHog**: Scans for leaked secrets in commit history.
- **Trivy**: Scans Docker base images for known CVEs.
- **Pytest**: Minimum 80% code coverage required for the backend API logic.

## 3. Python Style Guide
- Follow **PEP 8**.
- We use `black` for formatting and `isort` for import sorting.
- Always use `Pydantic` models for data validation, never parse raw JSON dictionaries manually.
