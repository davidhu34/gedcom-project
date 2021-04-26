from gedcom.testing import GedcomTestCase
from features.multiple_births import siblings_born_at_same_time,too_many_siblings


class MultpleBirthsTest(GedcomTestCase):

    def test_siblings_born_at_same_time(self) -> None:
        """ test if more than 5 siblings are born at once """

        self.assert_file_validation_fails(
            'incorrect_siblings_born_at_same_time', siblings_born_at_same_time,
            ["ERROR US12: Child(I01) is at least 60 years younger than their mother (at line 6)",
             "ERROR US12: Child(I04) is at least 60 years younger than their mother (at line 33)"])

        self.assert_file_validation_passes(
            'correct_siblings_born_at_same_time', siblings_born_at_same_time)

    def test_too_many_siblings(self) -> None:
        """ test if there are more than 15 siblings in the family """

        self.assert_file_validation_fails(
            'incorrect_too_many_siblings', too_many_siblings,
            ['ERROR US13: Child(I01) was born too close in time to another sibling(I02). (at line 6)',
             "ERROR US13: Child(I02) was born too close in time to another sibling(I01). (at line 13)"])

        self.assert_file_validation_passes(
            'correct_too_many_siblings', too_many_siblings)
