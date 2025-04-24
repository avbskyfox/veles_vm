from misc import *
from unittest import TestCase


class Test(TestCase):
    def test_get_classes_from_folder(self):
        modules = import_classes_from_folder('test_module_folder')
        class_names = ['TestClass1', 'TestClass2']
        for module in modules:
            if not module.__name__ in class_names:
                self.fail(f'Test {module.__name__} class not fond in imported class')
