import random
import unittest

from src import easy_di
from src.easy_di.exceptions import (DependencyNotRegisteredError,
                                    DependencyRegisteredError,
                                    OverwritingArgumentError)

mock_func = lambda deps, x: (x, deps["test"])

class BaseInjectorTest(unittest.TestCase):
    def tearDown(self) -> None:
        easy_di.BaseInjector._registered_dependencies = {}
        super().tearDown()

    def test_base_register_unregister(self) -> None:
        easy_di.BaseInjector.register("test", "test")
        self.assertDictEqual(
            easy_di.BaseInjector._registered_dependencies,
            {"test": "test"})
        easy_di.BaseInjector.unregister("test")
        self.assertDictEqual(
            easy_di.BaseInjector._registered_dependencies,
            {}
        )

    def test_base_inject(self) -> None:
        func = easy_di.BaseInjector("test")(mock_func)
        x = random.randint(0, 10)
        dep = random.randint(0, 10)
        easy_di.BaseInjector.register("test", dep)
        self.assertTupleEqual((x, dep), func(x))

    def test_inject_and_pass_deps(self) -> None:
        func = easy_di.BaseInjector("test")(mock_func)
        x = random.randint(0, 10)
        with self.assertRaises(OverwritingArgumentError):
            func(x, deps=x)  # type: ignore

    def test_decorate_when_dependency_not_registered(self) -> None:
        func = easy_di.BaseInjector("test")(mock_func)
        with self.assertRaises(DependencyNotRegisteredError) as e:
            func(1)
        self.assertEqual(e.exception.dependency_id, "test")

    def test_decorate_when_dependency_type_incorrect(self) -> None:
        with self.assertRaises(TypeError):
            easy_di.BaseInjector(75)(mock_func)  # type: ignore

    def test_register_when_dependency_registered(self) -> None:
        easy_di.BaseInjector.register("test", "test")
        with self.assertRaises(DependencyRegisteredError) as e:
            easy_di.BaseInjector.register("test", "test")
        self.assertEqual(e.exception.dependency_id, "test")

    def test_register_incorrect_dependency_id(self) -> None:
        with self.assertRaises(TypeError):
            easy_di.BaseInjector.register(123, "test")  # type: ignore
        with self.assertRaises(ValueError):
            easy_di.BaseInjector.register("*", "test")

    def test_unregister_when_dependency_not_registered(self) -> None:
        with self.assertRaises(DependencyNotRegisteredError) as e:
            easy_di.BaseInjector.unregister("test")
        self.assertEqual(e.exception.dependency_id, "test")

    def test_unregister_all(self) -> None:
        easy_di.BaseInjector.register("test", "test")
        easy_di.BaseInjector.register("test2", "test2")
        with self.assertWarns(Warning):
            easy_di.BaseInjector.unregister("*")
        self.assertDictEqual(easy_di.BaseInjector._registered_dependencies, {})


if __name__ == "__main__":
    unittest.main()
