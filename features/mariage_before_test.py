from gedcom.testing import GedcomTestCase
from features.mariage_before import marriage_before_death, marriage_before_divorce


class correctdeathandmarriagetest(GedcomTestCase):

    def test_marriage_before_death(self) -> None:
        """ test marriage before death """

        self.assert_file_validation_fails(
            'incorrect_death_marriage', marriage_before_death,
            ['ERROR US05 at line 21: Husband (I03) in family(F01) died before being married',
             'ERROR US05 at line 12: Wife (I02) in family(F01) died before being married'])

        self.assert_file_validation_passes(
            'correct_death_marriage', marriage_before_death)

    def marriage_before_divorce(self) -> None:
        """ test marriage before divorce """

        self.assert_file_validation_fails(
            'incorrect_divorce_marriage', marriage_before_divorce,
            ['ERROR US04 at line 21: Husband (I03) in family(F01) divorced before being married',
             'ERROR US04 at line 12: Wife (I02) in family(F01) divorced before being married'])

        self.assert_file_validation_passes(
            'correct_divorce_marriage', marriage_before_divorce)
