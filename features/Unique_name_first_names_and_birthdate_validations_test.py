from gedcom.testing import GedcomTestCase
from features.Unique_name_first_names_and_birthdate_validations import unique_name_and_birth, unique_names_in_families


class UniquenamefirstnamesandbirthdatevalidationsTest(GedcomTestCase):

    def test_unique_name_and_birth(self) -> None:
        """ test unique_name_and_birth """

        self.assert_file_validation_fails(
            'incorrect_unique_name_and_birth', unique_name_and_birth)

        self.assert_file_validation_passes(
            'correct_unique_name_and_birth', unique_name_and_birth)

    def test_unique_names_in_families(self) -> None:
        """ test unique_first_names_in_families """

        self.assert_file_validation_fails(
            'incorrect_unique_names_in_families', unique_names_in_families)

        self.assert_file_validation_passes(
            'correct_unique_names_in_families', unique_names_in_families)
