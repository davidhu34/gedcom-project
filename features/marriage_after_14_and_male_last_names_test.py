from gedcom.testing import GedcomTestCase
from features.marriage_after_14_and_male_last_names import marriage_after_14, male_last_names

class MarriageAgeAndMaleLastNamesTest(GedcomTestCase):

    def test_marriage_after_14(self) -> None:
        """ test marriage_after_14 """

        self.assert_file_validation_fails('incorrect_marriage_after_14', marriage_after_14, 
        [
            'ERROR US10: Individual(I02) in Family(F01) married (at line 53) when under age 14.', 
            'ERROR US10: Individual(I03) in Family(F01) married (at line 53) when under age 14.'
        ])

        self.assert_file_validation_passes('correct_marriage_after_14', marriage_after_14)
    
    # def test_male_last_names(self) -> None:
    #     """ test male_last_names """

    #     self.assert_printer_result('male_last_names', male_last_names, )
