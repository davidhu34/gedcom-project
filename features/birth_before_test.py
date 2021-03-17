from gedcom.testing import GedcomTestCase
from features.birth_before import birth_before_death,birth_before_marriage


class correctdeathandmarriagetest(GedcomTestCase):

    def test_birth_before_marriage(self) -> None:
        """ test birth before marriage """

        self.assert_file_validation_fails(
            'incorrect_birth_marriage', birth_before_marriage)

        self.assert_file_validation_passes(
            'correct_birth_marriage', birth_before_marriage)

    def test_birth_before_death(self) -> None:
        """ test birth before death """

        self.assert_file_validation_fails(
            'incorrect_birth_death', birth_before_death)

        self.assert_file_validation_passes(
            'correct_birth_death', birth_before_death)
