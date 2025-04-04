"""A simple dependency injector.

Copyright (c) 2025 David Lishchyshen

See the README file for information on usage and redistribution.
"""
from __future__ import annotations

import functools
import sys
from typing import Any, Callable, ClassVar, Dict, TypeVar
from warnings import warn

if sys.version_info >= (3, 10):
    from typing import Concatenate, ParamSpec
else:
    from typing_extensions import ParamSpec, Concatenate

from .exceptions import (DependencyNotRegisteredError,
                         DependencyRegisteredError, OverwritingArgumentError)

P = ParamSpec("P")
T = TypeVar("T")


class BaseInjector:
    """A simple dependency injector.

    Allows registering and injecting dependencies
    dynamically into functions using decorators.
    """

    _registered_dependencies: ClassVar[Dict[str, Any]] = {}
    def __init__(self, *dependencies: str) -> None:
        """Initialize the injector with a list of dependency IDs.

        :param dependencies: Dependency IDs that should be injected.
        :raises TypeError: If any dependency ID is not a string.
        """
        if not all(isinstance(dependency, str) for dependency in dependencies):
            raise TypeError("All dependencies id must be strings")
        self._dependencies = dependencies

    def __call__(
            self,
            func: Callable[Concatenate[Dict[str, Any], P], T],
    ) -> Callable[P, T]:
        """Injects the specified dependency.

        Wraps a function to automatically provide the specified dependencies
        as an argument when it is called. Injected dependencies are passed as
        the first argument in a dictionary.

        :param func: The function that requires dependency injection.
        :return: A new function with injected dependencies.
        """
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if "deps" in kwargs:
                raise OverwritingArgumentError("deps")
            try:
                registered_dependencies = (self
                                           ._registered_dependencies)
                deps = {
                    i: registered_dependencies[i] for i in self._dependencies
                }
            except KeyError as e:
                raise DependencyNotRegisteredError(e.args[0]) from e
            return func(deps, *args, **kwargs)
        return wrapper

    @classmethod
    def register(cls, dependency_id: str, dependency: Any) -> None:
        """Register a dependency with a unique string ID.

        :param dependency_id: The unique identifier for the dependency.
        :param dependency: The actual dependency (e.g., object, class, function).
        :raises TypeError: If the dependency ID is not a string.
        :raises ValueError: If the dependency ID is '*'.
        :raises DependencyRegisteredError: If the dependency ID is already registered.
        """
        if dependency_id == "*":
            raise ValueError("Dependency ID cannot be '*'")
        if not isinstance(dependency_id, str):
            raise TypeError("Dependency ID must be a string")
        if dependency_id in cls._registered_dependencies:
            raise DependencyRegisteredError(dependency_id)
        cls._registered_dependencies[dependency_id] = dependency


    @classmethod
    def unregister(cls, dependency_id: str) -> None:
        """Unregister a dependency by its unique ID.

        :param dependency_id: The unique identifier of the dependency to remove.
        :raises DependencyNotRegisteredError: If the dependency ID is not registered.
        """
        if dependency_id == "*":
            cls._registered_dependencies.clear()
            warn("Deleted all registered dependencies.")
            return
        if dependency_id not in cls._registered_dependencies:
            raise DependencyNotRegisteredError(dependency_id)
        cls._registered_dependencies.pop(dependency_id)
