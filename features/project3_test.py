from gedcom.testing import GedcomTestCase
from features.project3 import all_gedcom_individuals, all_gedcom_families


class Project3PrintTest(GedcomTestCase):

    def test_all_gedcom_individuals(self) -> None:
        """ test print all individuals """
        self.assert_printer_result(
            'test', all_gedcom_individuals, ['I01', 'I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09'])

    def test_marriage_before_divorce(self) -> None:
        """ test print all families """
        self.assert_printer_result(
            'test', all_gedcom_families, ['F01', 'F01', 'F02', 'F03', 'F04', 'F05'])
