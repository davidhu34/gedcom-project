from gedcom.testing import GedcomTestCase
from features.list_of_all_deceased_and_living_married import deceased_individual_list, living_married_list


class PrintTest(GedcomTestCase):

    def test_deceased_individual_list(self) -> None:
        ''' US29: test print all deceased individuals '''
        self.assert_printer_result(
            'test', deceased_individual_list, ['I02', 'I03', 'I05', 'I08'])

    def test_living_married_list(self) -> None:
        ''' US30: test print all living married '''
        self.assert_printer_result(
            'test', living_married_list, ['I07', 'I07'])