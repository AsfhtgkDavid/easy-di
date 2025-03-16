# Contributing to Easy-DI 🚀

Thank you for your interest in contributing to Easy-DI! Your help is greatly appreciated. This guide will walk you through the process of contributing to the project.

## Getting Started 🛠️

1. **Fork the Repository** – Click the 'Fork' button at the top right of the repository page.
2. **Clone Your Fork** – Use the following command to clone your forked repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/easy-di.git
   cd easy-di
   ```
3. **Create a New Branch** – Follow the naming convention `feature/your-feature` or `fix/your-fix`:
   ```sh
   git checkout -b feature/your-feature
   ```

## Development Setup ⚙️

Easy-DI supports `poetry` and `uv` for dependency management. Choose one of the following methods:

### Using Poetry
```sh
poetry install
```

To activate the virtual environment:
```sh
poetry shell
```

### Using uv
```sh
uv sync
```

To activate the virtual environment manually:
```sh
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
```

## Code Style & Linting 🎨

Easy-DI follows strict code formatting and linting rules. Before committing your changes, ensure your code is properly formatted:

```sh
ruff check . --fix
isort .
mypy .
```

## Running Tests 🧪

All changes must pass the test suite. Run tests using:

```sh
python -m unittest discover tests
```

To check test coverage:
```sh
coverage run -m unittest discover tests
coverage report -m
```

## Submitting Changes 📩

1. **Commit Your Changes** – Use meaningful commit messages:
   ```sh
   git add .
   git commit -m "Add feature: description"
   ```
2. **Push to Your Fork** –
   ```sh
   git push origin feature/your-feature
   ```
3. **Open a Pull Request** – Go to the original repository and click 'New Pull Request'.

## Contribution Guidelines 📜

- Ensure your code follows PEP8 and type hints where applicable.
- Write unit tests for new features or bug fixes.
- Keep pull requests focused on a single feature or fix.
- Squash commits where appropriate before submitting.
- Be respectful in discussions and reviews.

## Need Help? 🤔

If you have any questions or need guidance, feel free to open an issue in the repository. Happy coding! 🚀

