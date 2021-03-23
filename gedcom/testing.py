from unittest import TestCase
from typing import Callable, Optional, List
from os.path import abspath
from .repository import GedcomRepository, read_repository_file
from .exceptions import GedcomValidationException


class GedcomTestCase(TestCase):
    ''' GEDCOM feature test cases base class '''
    repo = None

    def parse_test_file(self, file_name: str) -> GedcomRepository:
        self.repo = read_repository_file(
            abspath(f'./test_files/{file_name}.ged'))
        return self.repo

    def prepare_validation_test(self, file_name: str, validator: Callable) -> None:
        self.parse_test_file(file_name)
        if not validator:
            raise 'No validator provided for test case'

    def assert_file_validation_passes(self, file_name: str, validator: Callable) -> None:
        self.prepare_validation_test(file_name, validator)
        self.assertFalse(validator(self.repo))

    def assert_file_validation_fails(self, file_name: str, validator: Callable, errors: Optional[List[str]] = []) -> None:
        self.prepare_validation_test(file_name, validator)
        results: Optional[List[str]] = validator(self.repo)
        if errors:
            self.assertEqual(errors, results)
        else:
            self.assertTrue(results and len(validator(self.repo)) > 0)

    def assert_printer_result(self, file_name: str, printer: Callable, results: List[str]) -> None:
        self.parse_test_file(file_name)
        if not printer:
            raise 'No printer provided for test case'
        self.assertEqual(results, printer(self.repo))
        