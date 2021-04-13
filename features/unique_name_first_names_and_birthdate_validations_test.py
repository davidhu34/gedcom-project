from gedcom.testing import GedcomTestCase
from features.unique_name_first_names_and_birthdate_validations import unique_name_and_birth, unique_first_names_in_families


class UniquenamefirstnamesandbirthdatevalidationsTest(GedcomTestCase):

    def test_unique_name_and_birth(self) -> None:
        ''' US23: Test Unique name and birth date '''

        self.assert_file_validation_fails(
            'incorrect_unique_name_and_birth', unique_name_and_birth,
            ['ANOMALY US23: Individuals(I01 at line 3, I02 at line 10) are not unique by names and birth date: Fatima /Porgho/|1972-02-07'])

        self.assert_file_validation_passes(
            'correct_unique_name_and_birth', unique_name_and_birth)

    def test_unique_first_names_in_families(self) -> None:
        ''' US25: Test Unique first names in families '''

        self.assert_file_validation_fails(
            'incorrect_unique_first_names_in_families', unique_first_names_in_families,
            ['ANOMALY US25: Family(F01 at line24) does not have unique first names (I02 at line 11, I03 at line 18)'])

        self.assert_file_validation_passes(
            'correct_unique_first_names_in_families', unique_first_names_in_families)
