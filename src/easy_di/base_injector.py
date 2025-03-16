import functools
from typing import Any, Callable, ClassVar, Concatenate, ParamSpec, TypeVar

from .exceptions import (DependencyNotRegisteredError,
                         DependencyRegisteredError, OverwritingArgumentError)

P = ParamSpec("P")
T = TypeVar("T")


class BaseInjector:
    _registered_dependencies: ClassVar[dict[str, Any]] = {}
    def __init__(self, *dependencies: str) -> None:
        if not all(isinstance(dependency, str) for dependency in dependencies):
            raise TypeError("All dependencies id must be strings")
        self._dependencies = dependencies

    def __call__(
            self,
            func: Callable[Concatenate[dict[str, Any], P], T],
    ) -> Callable[P, T]:
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
        if not isinstance(dependency_id, str):
            raise TypeError("Dependency ID must be a string")
        if dependency_id in cls._registered_dependencies:
            raise DependencyRegisteredError(dependency_id)
        cls._registered_dependencies[dependency_id] = dependency


    @classmethod
    def unregister(cls, dependency_id: str) -> None:
        if dependency_id not in cls._registered_dependencies:
            raise DependencyNotRegisteredError(dependency_id)
        cls._registered_dependencies.pop(dependency_id)
