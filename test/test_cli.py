import unittest

from lib.cli import bright_green
from lib.cli import bright_blue
from lib.cli import bright_yellow
from lib.cli import bright_red
from lib.cli import bold
from lib.cli import validate_path

from unittest.mock import MagicMock, patch

class TestCliColorMethods(unittest.TestCase):
    def test_bright_green(self):
        self.assertEqual(bright_green('test'), '\033[1;32;40mtest\033[0m')

    def test_bright_blue(self):
        self.assertEqual(bright_blue('test'), '\033[1;34;40mtest\033[0m')

    def test_bright_yellow(self):
        self.assertEqual(bright_yellow('test'), '\033[1;33;40mtest\033[0m')

    def test_bright_red(self):
        self.assertEqual(bright_red('test'), '\033[1;31;40mtest\033[0m')

    def test_bold(self):
        self.assertEqual(bold('test'), '\033[1mtest\033[0m')


class TestCliPathValidation(unittest.TestCase):
    @patch('lib.cli.Path')
    def test_returns_true_if_file_exists(self, path_mock):
        path_mock().is_file = MagicMock(return_value = True)
        self.assertTrue(validate_path('path'))

    @patch('lib.cli.Path')
    def test_returns_false_if_file_does_not_exist(self, path_mock):
        path_mock().is_file = MagicMock(return_value = False)
        self.assertFalse(validate_path('path'))

    @patch('lib.cli.Path')
    @patch('lib.cli.print')
    def test_prints_an_error_if_file_does_not_exist(self, print_mock, path_mock):
        path_mock().is_file = MagicMock(return_value = False)
        validate_path('path')
        print_mock.assert_called_with(bright_red("Error: file 'path' not found"))

if __name__ == '__main__':
    unittest.main()
