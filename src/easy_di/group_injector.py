"""A dependency injector that supports grouping dependencies into named collections.

Copyright (c) 2025 David Lishchyshen

See the README file for information on usage and redistribution.
"""

from __future__ import annotations

import functools
import sys
from typing import Any, Callable, ClassVar, Dict, Optional, TypeVar, Literal

if sys.version_info >= (3, 10):
    from typing import Concatenate, ParamSpec
else:
    from typing_extensions import ParamSpec, Concatenate

from warnings import warn

from .exceptions import (DependencyFormatError,
                         DependencyGroupNotRegisteredError,
                         DependencyGroupRegisteredError,
                         DependencyNotRegisteredError,
                         DependencyRegisteredError, OverwritingArgumentError)

P = ParamSpec("P")
T = TypeVar("T")
FuncForGroupDeps = Callable[
    Concatenate[Dict[str, Any], P],
    T]


class GroupInjector:
    """A dependency injector that supports grouping dependencies into named collections."""

    _registered_dependencies: ClassVar[Dict[str, Dict[str, Any]]] = {}
    def __init__(self, *dependencies: str, group_deps: bool = False) -> None:
        """Initialize the injector as a decorator with a list of required dependencies.
        Dependency IDs must include group names.

        :param dependencies: Dependency IDs in the format "group_id.dependency_id".
        :param group_deps: If true, group the dependencies into named collections in format {group_id: {dependency_id: dependency}.
        :raises TypeError: If any dependency ID is not a string.
        :raises DependencyFormatError: If a dependency ID is not correctly formatted.
        """
        if not all(isinstance(dependency, str) for dependency in dependencies):
            raise TypeError("All dependencies id must be strings")
        if not all("." in dependency for dependency in dependencies):
            raise DependencyFormatError
        self._dependencies = dependencies
        self._group_deps = not not group_deps


    def __call__(self,
                 func: FuncForGroupDeps[P, T],
                 ) -> Callable[P, T]:
        """Wraps a function to automatically provide the specified dependencies
        from a registered group.
        Injected dependencies are passed as the first argument in a dictionary,
        where keys follow the format "group_id.dependency_id".

        :param func: The function that requires grouped dependency injection.
        :return: The wrapped function with injected dependencies.
        """
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if "deps" in kwargs:
                raise OverwritingArgumentError("deps")
            try:
                deps: dict[str, Any]
                if self._group_deps:
                    groups = self._split_to_unique_groups(self._dependencies)
                    deps = {group: {} for group in groups}
                else:
                    deps = {}
                for i in self._dependencies:
                    dependency, group = self._parse_dependency_and_group(i)
                    if dependency == "*":
                        for dependency_id, dependency in (
                                self._registered_dependencies[group].items()):
                            if self._group_deps:
                                deps[group][dependency_id] = dependency
                            else:
                                deps[group+"."+dependency_id] = dependency
                        continue
                    if self._group_deps:
                        deps[group][dependency] = self._registered_dependencies[group][dependency]
                    else:
                        deps[i] = self._registered_dependencies[group][dependency]
            except KeyError as e:
                raise DependencyNotRegisteredError(e.args[0]) from e
            return func(deps, *args, **kwargs)
        return wrapper


    @classmethod
    def register_dependency(
            cls,
            dependency_id: str,
            dependency: Any,
            group_id: Optional[str] = None,
            *,
            if_group_not_exists: Literal["error", "create"] = "error") -> None:
        """Register a dependency within a specified group.

        :param dependency_id: The unique identifier for the dependency.
        :param dependency: The actual dependency (e.g., object, class, function).
        :param group_id: The group where the dependency should be registered.
        :param if_group_not_exists: What to do when a dependency group is not registered.
        :raises TypeError: If dependency_id or group_id is not a string.
        :raises ValueError: If the dependency ID is '*'.
        :raises DependencyGroupNotRegisteredError: If the specified group is not registered.
        :raises DependencyRegisteredError: If the dependency ID is already registered in the group.
        :raises DependencyFormatError: If the dependency ID is not contain group and group_id is not specified.
        """
        dependency_id, group_id = cls._parse_dependency_and_group(
            dependency_id,
            group_id)
        if dependency_id == "*":
            raise ValueError("Dependency ID cannot be '*'")
        if group_id not in cls._registered_dependencies:
            if if_group_not_exists == "create":
                cls.register_dependency_group(group_id)
            else:
                raise DependencyGroupNotRegisteredError(group_id)
        if dependency_id in cls._registered_dependencies[group_id]:
            raise DependencyRegisteredError(dependency_id)
        cls._registered_dependencies[group_id][dependency_id] = dependency

    @classmethod
    def unregister_dependency(
            cls,
            dependency_id: str,
            group_id: Optional[str] =None) -> None:
        """Unregister a specific dependency from a group.

        :param dependency_id: The unique identifier of the dependency to remove.
        :param group_id: The group from which the dependency should be removed.
        :raises TypeError: If dependency_id or group_id is not a string.
        :raises DependencyGroupNotRegisteredError: If the specified group is not registered.
        :raises DependencyNotRegisteredError: If the dependency is not found in the group.
        :raises DependencyFormatError: If the dependency ID is not contain group and group_id is not specified.
        """
        dependency_id, group_id = cls._parse_dependency_and_group(
            dependency_id,
            group_id)
        if group_id not in cls._registered_dependencies:
            raise DependencyGroupNotRegisteredError(group_id)
        if dependency_id == "*":
            cls._registered_dependencies[group_id].clear()
            warn("Deleted all registered dependencies.")
            return
        if dependency_id not in cls._registered_dependencies[group_id]:
            raise DependencyNotRegisteredError(dependency_id)
        cls._registered_dependencies[group_id].pop(dependency_id)

    @classmethod
    def register_dependency_group(
            cls,
            group_id: str,
            **dependencies: Any) -> None:
        """Register a new dependency group with optional initial dependencies.

        :param group_id: The unique identifier for the group.
        :param dependencies: Key-value pairs representing dependency IDs and their values.
        :raises TypeError: If the group or dependency ID is not a string.
        :raises ValueError: If the group ID contains dot or dependency or group ID is '*'.
        :raises DependencyGroupRegisteredError: If the group ID is already registered.
        """
        if not isinstance(group_id, str):
            raise TypeError("Dependency group ID must be a string")
        if group_id in cls._registered_dependencies:
            raise DependencyGroupRegisteredError(group_id)
        if "." in group_id:
            raise ValueError("Dependency group ID cannot contain dot")
        if group_id == "*":
            raise ValueError("Dependency group ID cannot be '*'")
        cls._registered_dependencies[group_id] = {}
        for dependency in dependencies:
            cls.register_dependency(dependency,
                                    dependencies[dependency],
                                    group_id)

    @classmethod
    def unregister_dependency_group(cls, group_id: str) -> None:
        """Unregister an entire dependency group.

        :param group_id: The unique identifier of the group to remove.
        :raises DependencyGroupNotRegisteredError: If the group ID is not registered.
        """
        if group_id == "*":
            cls._registered_dependencies.clear()
            warn("Deleted all registered dependency groups.")
            return
        if group_id not in cls._registered_dependencies:
            raise DependencyGroupNotRegisteredError(group_id)
        if len(cls._registered_dependencies[group_id]) != 0:
            warn("Deleting not empty dependency group")
        cls._registered_dependencies.pop(group_id)

    @staticmethod
    def _parse_dependency_and_group(
            dependency_id: str,
            group_id: Optional[str] = None) -> tuple[str, str]:
        if not isinstance(dependency_id, str):
            raise TypeError("Dependency ID must be a string")
        if group_id is None:
            splitted = dependency_id.split(".", 1)
            if len(splitted) != 2: # noqa: PLR2004
                raise DependencyFormatError
            group_id, dependency_id = splitted
        elif not isinstance(group_id, str):
            raise TypeError("Dependency group ID must be a string")
        return dependency_id, group_id

    @staticmethod
    def _split_to_unique_groups(
            dependencies: tuple[str,...]) -> tuple[str, ...]:
        return tuple({dependency.split(".", 1)[0] for dependency in dependencies})
