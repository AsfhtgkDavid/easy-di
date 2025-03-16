import random
import unittest

from src import easy_di
from src.easy_di.exceptions import (DependencyFormatError,
                                    DependencyGroupNotRegisteredError,
                                    DependencyGroupRegisteredError,
                                    DependencyNotRegisteredError,
                                    DependencyRegisteredError,
                                    OverwritingArgumentError)

mock_func = lambda deps, x: (x, deps['test.test'])

class GroupInjectorTest(unittest.TestCase):
    def tearDown(self) -> None:
        easy_di.GroupInjector._registered_dependencies = {}
        super().tearDown()

    def test_register_unregister_group_without_deps(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test')
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {'test': {}})
        easy_di.GroupInjector.unregister_dependency_group('test')
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {}
        )

    def test_register_unregister_group_with_deps(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test', test=452)
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {'test': {'test': 452}})
        easy_di.GroupInjector.unregister_dependency_group('test')
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {}
        )

    def test_format_register_unregister_dependency(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test')
        easy_di.GroupInjector.register_dependency('test.test', 452)
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {'test': {'test': 452}})
        easy_di.GroupInjector.unregister_dependency('test.test')
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {'test': {}}
        )

    def test_args_register_unregister_dependency(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test')
        easy_di.GroupInjector.register_dependency(
            'test',
            452,
            'test')
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {'test': {'test': 452}})
        easy_di.GroupInjector.unregister_dependency('test', 'test')
        self.assertDictEqual(
            easy_di.GroupInjector._registered_dependencies,
            {'test': {}}
        )

    def test_register_dependency_without_register_group(self) -> None:
        with self.assertRaises(DependencyGroupNotRegisteredError) as e:
            easy_di.GroupInjector.register_dependency('test.test', 452)
        self.assertEqual(e.exception.group_id, 'test')

    def test_base_inject(self) -> None:
        func = easy_di.GroupInjector('test.test')(mock_func)
        x = random.randint(0, 10)
        dep = random.randint(0, 10)
        easy_di.GroupInjector.register_dependency_group('test', test=dep)
        self.assertTupleEqual((x, dep), func(x))
        easy_di.GroupInjector.unregister_dependency_group('test')

    def test_inject_and_pass_deps(self) -> None:
        func = easy_di.GroupInjector('test')(mock_func)
        x = random.randint(0, 10)
        with self.assertRaises(OverwritingArgumentError):
            func(x, deps=x)  # type: ignore

    def test_decorate_when_dependency_not_registered(self) -> None:
        func = easy_di.GroupInjector('test.test')(mock_func)
        easy_di.GroupInjector.register_dependency_group('test')
        with self.assertRaises(DependencyNotRegisteredError) as e:
            func()  # type: ignore
        self.assertEqual(e.exception.dependency_id, 'test')

    def test_decorate_when_dependency_type_incorrect(self) -> None:
        with self.assertRaises(TypeError):
            easy_di.GroupInjector(75)(mock_func)  # type: ignore

    def test_register_dependency_when_registered(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test', test='test')
        with self.assertRaises(DependencyRegisteredError) as e:
            easy_di.GroupInjector.register_dependency('test.test', 'test')
        self.assertEqual(e.exception.dependency_id, 'test')
        easy_di.GroupInjector.unregister_dependency_group('test')

    def test_register_dependency_incorrect_id(self) -> None:
        with self.assertRaises(TypeError):
            easy_di.GroupInjector.register_dependency(123, 'test')  # type: ignore

    def test_register_dependency_group_incorrect_id(self) -> None:
        with self.assertRaises(TypeError):
            easy_di.GroupInjector.register_dependency_group(123)  # type: ignore

    def test_register_registered_dependency_group(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test')
        with self.assertRaises(DependencyGroupRegisteredError) as e:
            easy_di.GroupInjector.register_dependency_group('test')
        self.assertEqual(e.exception.group_id, 'test')

    def test_register_dependency_group_with_dot(self) -> None:
        with self.assertRaises(ValueError):
            easy_di.GroupInjector.register_dependency_group('test.test')

    def test_register_dependency_with_incorrect_group(self) -> None:
        with self.assertRaises(TypeError):
            easy_di.GroupInjector.register_dependency('test', 'test', 12)  # type: ignore

    def test_register_dependency_without_group(self) -> None:
        with self.assertRaises(DependencyFormatError):
            easy_di.GroupInjector.register_dependency('test', 'test')

    def test_unregister_dependency_when_not_registered(self) -> None:
        easy_di.GroupInjector.register_dependency_group('test')
        with self.assertRaises(DependencyNotRegisteredError) as e:
            easy_di.GroupInjector.unregister_dependency('test.test')
        self.assertEqual(e.exception.dependency_id, 'test')

    def test_unregister_dependency_when_group_not_registered(self) -> None:
        with self.assertRaises(DependencyGroupNotRegisteredError) as e:
            easy_di.GroupInjector.unregister_dependency('test.test')
        self.assertEqual(e.exception.group_id, 'test')

    def test_unregister_dependency_group_when_group_not_registered(self) -> None:
        with self.assertRaises(DependencyGroupNotRegisteredError) as e:
            easy_di.GroupInjector.unregister_dependency_group('test')
        self.assertEqual(e.exception.group_id, 'test')


if __name__ == '__main__':
    unittest.main()
