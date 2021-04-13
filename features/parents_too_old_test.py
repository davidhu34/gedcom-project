from gedcom.testing import GedcomTestCase
from features.parents_too_old import parents_too_old, sibling_spacing


class BirthBeforeTest(GedcomTestCase):

    def test_parents_too_old(self) -> None:
        """ test parents too old """

        self.assert_file_validation_fails(
            'incorrect_parent_age', parents_too_old,
            ['ERROR US12 at line 21: Parent in family(F01) is too old'])

        self.assert_file_validation_passes(
            'correct_parent_age', parents_too_old)

    def test_sibling_spacing(self) -> None:
        """ test sibling spacing """

        self.assert_file_validation_fails(
            'incorrect_sibling_spacing', sibling_spacing,
            ['ERROR US03 at line 15: Individual (I02) died before being born'])

        self.assert_file_validation_passes(
            'correct_sibling_spacing', sibling_spacing)
