from gedcom.testing import GedcomTestCase
from features.list_recent_births_deaths import list_recent_births, list_recent_deaths

class RecentBirthsDeaths(GedcomTestCase):

    def test_list_recent_births(self) -> None:
        """ test list_recent_births """

        self.assert_printer_result('recent_births', list_recent_births, ['I08'])
    
    def test_list_recent_deaths(self) -> None:
        """ test list_recent_deaths """

        self.assert_printer_result('recent_deaths',  list_recent_deaths, ['I04'])