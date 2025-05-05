# Easy-DI: Lightweight Dependency Injection for Python 🚀🚀🚀

## Introduction 🎯🔧📌

Easy-DI is a simple yet powerful Python library for dependency injection. It helps you manage dependencies efficiently, promoting modular, reusable, and testable code. With Easy-DI, you can dynamically register and inject dependencies using decorators, making dependency management seamless. ✅✅✅

## Key Features ✨🔥💡

- **Decorator-based dependency injection** for clean and intuitive code
- **Dynamic registration and unregistration** of dependencies
- **Support for various dependency types**: functions, classes, objects, and more
- **Strict enforcement of string-based dependency IDs**
- **Grouped dependency injection** for better organization
- **Supports wildcard injection (`group.*`) to inject all dependencies from a group as separate elements**
- **Supports bulk unregistration using wildcard patterns (e.g., `*`, `group.*`)**
- **Full compatibility with Python's type hints** for type safety

## Installation 💻📦⚙️

Easy-DI has no external dependencies. You can install it using your preferred package manager:

### Using pip 🐍📌✅
```sh
pip install di-easy
```

### Using Poetry 🎼📌✅
```sh
poetry add di-easy
```

### Using uv ⚡📌✅
```sh
uv pip install di-easy
```
or
```sh
uv add di-easy
```

## Usage Guide 📝🚀🔍

### Basic Dependency Injection 🏗️🔄🎯

```python
from easy_di import BaseInjector

# Define a class to be used as a dependency
class Service:
    def process(self, arg):
        return f"Processed: {arg}"

# Register an instance of the class as a dependency
BaseInjector.register("service", Service())  # IDs must be strings

# Define a function with dependency injection
@BaseInjector("service")
def my_function(deps, arg):
    return deps["service"].process(arg)

print(my_function("Hello"))  # Output: "Processed: Hello"
```

> ✅ In `BaseInjector`, dependencies can be registered **before or after** the function is defined, but **must be registered before the function is first called**.

### Grouped Dependency Injection 🎯🔗📌

```python
from easy_di import GroupInjector

# Register a dependency group with multiple dependencies
GroupInjector.register_dependency_group("services", logger=lambda msg: f"Log: {msg}", config={"debug": True})

# Define a function with grouped injection
@GroupInjector("services.logger", "services.config")
def log_message(deps, message):
    return f"{deps['services.logger'](message)} | Debug: {deps['services.config']['debug']}"

print(log_message("An event occurred"))  # Output: "Log: An event occurred | Debug: True"
```

> ✅ In `GroupInjector`, dependencies can also be registered **before or after** the function definition, but **must be registered before its first invocation**. When registering a dependency into a group, ensure that the group is registered **first** (unless you set `if_group_not_exists="create"`).

### Wildcard Group Injection (`group.*`) 🎯✨🔧

You can inject all dependencies from a group using the `group.*` pattern. Each dependency in the group will be added as a separate element in `deps`.

```python
from easy_di import GroupInjector

# Register a dependency group with multiple dependencies
GroupInjector.register_dependency_group("config", host="localhost", port=8080, debug=True)

# Inject all elements of the group as separate entries in `deps`
@GroupInjector("config.*")
def app_settings(deps):
    return f"Host: {deps['config.host']}, Port: {deps['config.port']}, Debug: {deps['config.debug']}"

print(app_settings())  # Output: "Host: localhost, Port: 8080, Debug: True"
```

### Bulk Unregistration with Wildcards ❌🧹🚫

You can unregister multiple dependencies at once using wildcard patterns:

```python
from easy_di import BaseInjector, GroupInjector

BaseInjector.unregister("*")  # Unregister all dependencies in BaseInjector
GroupInjector.unregister_dependency("test.*")  # Unregister all dependencies in group "test"
GroupInjector.unregister_dependency_group("*")  # Unregister all dependency groups and their dependencies
```

## API Reference 📚🔍🛠️

### `BaseInjector` ⚙️🔄📌

#### `BaseInjector(dependency_id: str)`

Decorator that injects a registered dependency into a function.

#### `BaseInjector.register(dependency_id: str, dependency: Any) -> None`

Registers a dependency using a string ID.

#### `BaseInjector.unregister(dependency_id: str) -> None`

Unregisters a dependency by its ID. Supports `"*"` to unregister all.

---

### `GroupInjector` 🔗⚙️📌

#### `GroupInjector(dependency_id: str, *, group_deps: bool = False)`

Decorator that injects dependencies from a registered group.

`group_deps`: If true, group the dependencies into named collections in format `{group_id: {dependency_id: dependency}}`.

#### `GroupInjector.register_dependency_group(group_id: str, **dependencies: Any) -> None`

Registers a dependency group containing multiple dependencies.

#### `GroupInjector.register_dependency(dependency_id: str, dependency: Any, group_id: Optional[str] = None, *, if_group_not_exists: Literal["error", "create"] = "error") -> None`

Registers a dependency inside an existing group.

`if_group_not_exists`: What to do when the group is not registered. Use "error" to raise an exception or "create" to automatically create the group.

#### `GroupInjector.unregister_dependency(dependency_id: str, group_id: Optional[str] = None) -> None`
Unregisters a specific dependency from a group. Supports wildcards (e.g., `"group.*"`).

#### `GroupInjector.unregister_dependency_group(group_id: str) -> None`

Unregisters an entire dependency group. Supports `"*"` to unregister all groups.

## Development & Configuration 🛠️💡🔧

Easy-DI follows PEP8 guidelines and enforces strict type checking with MyPy. The following tools are used in development:

- `coverage` (test coverage analysis)
- `isort` (import sorting)
- `mypy` (static type checking)
- `ruff` (linting and code formatting)

## License 📜✅🔓

Easy-DI is released under the MIT License.

## Contributing 🤝📢📌

Contributions are welcome! Feel free to open issues or submit pull requests.

## Support & Contact 📩💬📌

For questions or support, please open an issue in the repository.
