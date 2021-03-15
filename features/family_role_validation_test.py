from gedcom.testing import GedcomTestCase
from features.family_role_validation import correct_gender_roles, unique_family_spouses

class CorrectGenderRoleTest(GedcomTestCase):

    def test_correct_gender_roles(self) -> None:
        """ test correct_gender_roles """        
        self.assert_file_validation_fails('incorrect_gender_roles', correct_gender_roles)
        self.assert_file_validation_passes('correct_gender_roles', correct_gender_roles)

    def test_unique_family_spouses(self) -> None:
        """ test unique_family_spouses """        
        self.assert_file_validation_fails('not_unique_family_spouses', unique_family_spouses)
        self.assert_file_validation_passes('unique_family_spouses', unique_family_spouses)
