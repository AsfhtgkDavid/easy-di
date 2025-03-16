class OverwritingArgumentError(ValueError):
    def __init__(self, overwritten_argument: str) -> None:
        self.overwritten_argument = overwritten_argument

    def __str__(self) -> str:
        return f"Argument '{self.overwritten_argument}' is already provided\
         and will be overwritten."


class DependencyError(Exception):
    pass


class DependencyNotRegisteredError(DependencyError):
    def __init__(self, dependency_id: str) -> None:
        self.dependency_id = dependency_id

    def __str__(self) -> str:
        return f"Dependency '{self.dependency_id}' is not registered."


class DependencyRegisteredError(DependencyError):
    def __init__(self, dependency_id: str) -> None:
        self.dependency_id = dependency_id

    def __str__(self) -> str:
        return f"Dependency '{self.dependency_id}' is already registered."


class DependencyFormatError(DependencyError):
    def __str__(self) -> str:
        return "Dependency must be set with format {group_id}.{dependency}\
or group_id must be setted"


class DependencyGroupNotRegisteredError(DependencyError):
    def __init__(self, group_id: str) -> None:
        self.group_id = group_id

    def __str__(self) -> str:
        return f"Dependency group '{self.group_id}' is not registered."


class DependencyGroupRegisteredError(DependencyError):
    def __init__(self, group_id: str) -> None:
        self.group_id = group_id

    def __str__(self) -> str:
        return f"Dependency group '{self.group_id}' is already registered."
