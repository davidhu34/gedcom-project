from gedcom.testing import GedcomTestCase
from features.family_role_validation import correct_gender_roles, unique_family_spouses


class CorrectGenderRoleTest(GedcomTestCase):

    def test_correct_gender_roles(self) -> None:
        """ test correct_gender_roles """

        self.assert_file_validation_fails(
            'incorrect_gender_roles', correct_gender_roles,
            ['ERROR US21 at line 72: Family(F03) has incorrect gender for Wife(I08)'])

        self.assert_file_validation_passes(
            'correct_gender_roles', correct_gender_roles)

    def test_unique_family_spouses(self) -> None:
        """ test unique_family_spouses """

        self.assert_file_validation_fails(
            'not_unique_family_spouses', unique_family_spouses,
            ['ANOMALY US24: Families(F03 at line 97, F04 at line 105) are not unique by spouse names and marriage date: Grandpa /Yaeger/|Grandma /Yaeger/|0805-05-05'])

        self.assert_file_validation_passes(
            'unique_family_spouses', unique_family_spouses)
