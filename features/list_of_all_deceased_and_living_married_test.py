from gedcom.testing import GedcomTestCase
from features.list_of_all_deceased_and_living_married import deceased_individual_list, living_married_list


class PrintTest(GedcomTestCase):

    def test_deceased_individual_list(self) -> None:
        ''' US29: test print all deceased individuals '''
        self.assert_printer_result(
            'list_of_deceased', deceased_individual_list, ['I03'])

    def test_living_married_list(self) -> None:
        ''' US30: test print all living married '''
        self.assert_printer_result(
            'list_of_living_married', living_married_list, ['I04', 'I03', 'I05', 'I02'])