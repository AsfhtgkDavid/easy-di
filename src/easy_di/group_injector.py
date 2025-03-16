from __future__ import annotations

import functools
from typing import (Any, Callable, ClassVar, Concatenate, Optional, ParamSpec,
                    TypeAlias, TypeVar, Union)
from warnings import warn

from .exceptions import (DependencyFormatError,
                         DependencyGroupNotRegisteredError,
                         DependencyGroupRegisteredError,
                         DependencyNotRegisteredError,
                         DependencyRegisteredError, OverwritingArgumentError)

P = ParamSpec("P")
T = TypeVar("T")
FuncForGroupDeps: TypeAlias = Callable[
    Concatenate[dict[str, Union[dict[str, Any], Any]], P],
    T]


class GroupInjector:
    _registered_dependencies: ClassVar[dict[str, dict[str, Any]]] = {}
    def __init__(self, *dependencies: str) -> None:
        if not all(isinstance(dependency, str) for dependency in dependencies):
            raise TypeError("All dependencies id must be strings")
        self._dependencies = dependencies


    def __call__(self,
                 func: FuncForGroupDeps[P, T],
                 ) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if "deps" in kwargs:
                raise OverwritingArgumentError("deps")
            try:
                deps = {}
                for i in self._dependencies:
                    dependency, group = self._parse_dependency_and_group(i)
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
            group_id: Optional[str] = None) -> None:
        dependency_id, group_id = cls._parse_dependency_and_group(
            dependency_id,
            group_id)
        if group_id not in cls._registered_dependencies:
            raise DependencyGroupNotRegisteredError(group_id)
        if dependency_id in cls._registered_dependencies[group_id]:
            raise DependencyRegisteredError(dependency_id)
        cls._registered_dependencies[group_id][dependency_id] = dependency

    @classmethod
    def unregister_dependency(
            cls,
            dependency_id: str,
            group_id: Optional[str] =None) -> None:
        dependency_id, group_id = cls._parse_dependency_and_group(
            dependency_id,
            group_id)
        if group_id not in cls._registered_dependencies:
            raise DependencyGroupNotRegisteredError(group_id)
        if dependency_id not in cls._registered_dependencies[group_id]:
            raise DependencyNotRegisteredError(dependency_id)
        cls._registered_dependencies[group_id].pop(dependency_id)

    @classmethod
    def register_dependency_group(
            cls,
            group_id: str,
            **dependencies: Any) -> None:
        if not isinstance(group_id, str):
            raise TypeError("Dependency group ID must be a string")
        if group_id in cls._registered_dependencies:
            raise DependencyGroupRegisteredError(group_id)
        if '.' in group_id:
            raise ValueError("Dependency group ID cannot contain dot")
        cls._registered_dependencies[group_id] = {}
        for dependency in dependencies:
            cls.register_dependency(dependency,
                                    dependencies[dependency],
                                    group_id)

    @classmethod
    def unregister_dependency_group(cls, group_id: str) -> None:
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
