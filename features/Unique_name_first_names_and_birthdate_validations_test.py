from gedcom.testing import GedcomTestCase
from features.Unique_name_first_names_and_birthdate_validations import unique_name_and_birth, unique_first_names_in_families


class UniquenamefirstnamesandbirthdatevalidationsTest(GedcomTestCase):

    def test_unique_name_and_birth(self) -> None:
        """ test unique_name_and_birth """

        self.assert_file_validation_fails(
            'incorrect_unique_name_and_birth', unique_name_and_birth,
            ['ANOMALY US23: Individuals(@P1@ at line 3, @P2@ at line 9) are not unique by names and birth date: Fatima /Porgho/|1972-02-07'])

        self.assert_file_validation_passes(
            'correct_unique_name_and_birth', unique_name_and_birth)

    def test_unique_first_names_in_families(self) -> None:
        """ test unique_first_names_in_families """

        self.assert_file_validation_fails(
            'incorrect_unique_first_names_in_families', unique_first_names_in_families,
            ['ANOMALY US25: Family(@F1@ at line21) does not have unique first names (@P2@ at line 13, @P3@ at line 19)'])

        self.assert_file_validation_passes(
            'correct_unique_first_names_in_families', unique_first_names_in_families)
