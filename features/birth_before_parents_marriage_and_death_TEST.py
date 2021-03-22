from gedcom.testing import GedcomTestCase
from features.birth_before_parents_marriage_and_death import birth_before_parents_marriage, birth_before_parents_death

class BirthBeforeParentsMarriageDeathTest(GedcomTestCase):

    def test_birth_before_parents_marriage(self) -> None:
        """ test birth_before_parents_marriage """

        self.assert_file_validation_fails('incorrect_birth_before_parents_marriage', birth_before_parents_marriage, 
        [
            "ANOMALY US08: Birth date (at line 4) for Individual(I01) in Family(F01) occurs before parent's marriage date (at line 53).", 
            "ANOMALY US08: Birth date (at line 16) for Individual(I03) in Family(F02) occurs before parent's marriage date (at line 60).", 
            "ANOMALY US08: Birth date (at line 37) for Individual(I06) in Family(F02) occurs before parent's marriage date (at line 60)."
        ])

        self.assert_file_validation_passes('correct_birth_before_parents_marriage', birth_before_parents_marriage)

    def test_birth_before_parents_death(self) -> None:
        """ test birth_before_parents_death """

        self.assert_file_validation_fails('incorrect_birth_before_parents_death', birth_before_parents_death, 
        [
            "ERROR US09: Birth date (at line 4) for Individual(I01) in Family(F01) occurs after Father's(I02) death date (at line 12).", 
            "ERROR US09: Birth date (at line 18) for Individual(I03) in Family(F02) occurs after Mother's(I05) death date (at line 33)."
        ])

        self.assert_file_validation_passes('correct_birth_before_parents_death', birth_before_parents_death)