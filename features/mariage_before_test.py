from gedcom.testing import GedcomTestCase
from features.mariage_before import marriage_before_death, marriage_before_divorce


class MarriageBeforeTest(GedcomTestCase):

    def test_marriage_before_death(self) -> None:
        """ test marriage before death """

        self.assert_file_validation_fails(
            'incorrect_death_marriage', marriage_before_death,
            ['ERROR US05 at line 21: Husband (I03) in family(F02) died before marriage',
             'ERROR US05 at line 40: Wife (I05) in family(F02) died before marriage'])

        self.assert_file_validation_passes(
            'correct_death_marriage', marriage_before_death)

    def test_marriage_before_divorce(self) -> None:
        """ test marriage before divorce """

        self.assert_file_validation_fails(
            'incorrect_divorce_marriage', marriage_before_divorce,
            ['ERROR US04 at line 71: Husband (@I11@) in family(@F5@) divorced before marriage',
             'ERROR US04 at line 64: Wife (@I10@) in family(@F5@) divorced before marriage'])

        self.assert_file_validation_passes(
            'correct_divorce_marriage', marriage_before_divorce)
