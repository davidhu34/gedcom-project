from gedcom.testing import GedcomTestCase
from features.multiple_births import siblings_born_at_same_time,too_many_siblings


class MultpleBirthsTest(GedcomTestCase):

    def test_siblings_born_at_same_time(self) -> None:
        """ test if more than 5 siblings are born at once """

        self.assert_file_validation_fails(
            'incorrect_siblings_born_at_same_time', siblings_born_at_same_time,
            ["ERROR US14 at line 39: too many siblings born at once(0835-02-10) in family(F01)"])

        self.assert_file_validation_passes(
            'correct_siblings_born_at_same_time', siblings_born_at_same_time)

    def test_too_many_siblings(self) -> None:
        """ test if there are more than 15 siblings in the family """

        self.assert_file_validation_fails(
            'incorrect_too_many_siblings', too_many_siblings,
            ['ERROR US15 at line 172: too many siblings in family: (F01)'])

        self.assert_file_validation_passes(
            'correct_too_many_siblings', too_many_siblings)
