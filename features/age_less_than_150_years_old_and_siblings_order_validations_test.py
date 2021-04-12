from gedcom.testing import GedcomTestCase
from features.age_less_than_150_years_old_and_siblings_order import age_and_age_at_death

class agelessthan150yearsoldandsiblingsorderTest(GedcomTestCase):

    def test_age_and_age_at_death(self) -> None:
        """ test_age_and_age_at_death """

        self.assert_file_validation_fails(
            'age_greater_than_150_years_old', age_and_age_at_death, 
            ['ERROR US07: Individual(I03) is older than 150 years old (521) (at line 20)'])

        self.assert_file_validation_passes(
            'age_less_than_150_years_old', age_and_age_at_death)