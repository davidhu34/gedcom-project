from gedcom.testing import GedcomTestCase
from list_recent_births_deaths import list_recent_births

class RecentBirthsDeaths(GedcomTestCase):

    def test_list_recent_births(self) -> None:
        """ test list_recent_births """

        self.assert_printer_result('recent_births', list_recent_births, ['I08'])