
from gedcom.testing import GedcomTestCase
from features.illegitimate_dates import illegitimate_dates


class IllegitimateDatesTest(GedcomTestCase):

    def test_illegitimate_dates(self) -> None:
        """ test illegitimate_dates """

        self.assert_file_validation_fails(
            'illegitimate_dates', illegitimate_dates,
            [
                'ERROR US42: Illegitimate date (31 JUN 0835) at line (7)',
                'ERROR US42: Illegitimate date (29 FEB 2021) at line (87)'
            ])

        self.assert_file_validation_passes(
            'legitimate_dates', illegitimate_dates)
