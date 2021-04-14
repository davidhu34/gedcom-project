from gedcom.testing import GedcomTestCase
from features.parents_too_old import parents_too_old, sibling_spacing


class ParentsAgeTest(GedcomTestCase):

    def test_parents_too_old(self) -> None:
        """ test if parents are within 60 and 80 years of child """

        self.assert_file_validation_fails(
            'incorrect_parent_age', parents_too_old,
            ['ERROR US12 at line 21: Parent in family(F01) is too old'])

        self.assert_file_validation_passes(
            'correct_parent_age', parents_too_old)

    def test_sibling_spacing(self) -> None:
        """ test if siblings are too close in age but not twins """

        self.assert_file_validation_fails(
            'incorrect_sibling_spacing', sibling_spacing,
            ['ERROR US13: Child(I01) was born too close in time to another sibling(I02). (at line 6)',
            "ERROR US13: Child(I02) was born too close in time to another sibling(I01). (at line 13)"])

        self.assert_file_validation_passes(
            'correct_sibling_spacing', sibling_spacing)
