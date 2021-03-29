from gedcom.testing import GedcomTestCase
from features.birth_before import birth_before_death, birth_before_marriage


class BirthBeforeTest(GedcomTestCase):

    def test_birth_before_marriage(self) -> None:
        """ test birth before marriage """

        self.assert_file_validation_fails(
            'incorrect_birth_marriage', birth_before_marriage,
            ['ERROR US02 at line 21: Husband (I03) in family(F01) married before being born',
             'ERROR US02 at line 12: Wife (I02) in family(F01) married before being born'])

        self.assert_file_validation_passes(
            'correct_birth_marriage', birth_before_marriage)

    def test_birth_before_death(self) -> None:
        """ test birth before death """

        self.assert_file_validation_fails(
            'incorrect_birth_death', birth_before_death,
            ['ERROR US03 at line 15: Individual (I02) died before being born'])

        self.assert_file_validation_passes(
            'correct_birth_death', birth_before_death)
