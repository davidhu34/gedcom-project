from gedcom.testing import GedcomTestCase
from features.list_of_living_single_and_multiple_births import living_single_list, list_multiple_births


class PrintTest(GedcomTestCase):

    def test_living_single_list(self) -> None:
        '''US31 : List all living single individuals'''
        self.assert_printer_result(
            'list_of_living_single', living_single_list, ['I03'])

    def test_list_multiple_births(self) -> None:
        '''US32: List of multiple births'''
        self.assert_printer_result(
            'list_of_multiple_births', list_multiple_births, ['I01', 'I02'])