from gedcom.testing import GedcomTestCase
from features.valid_dates import divorce_before_death, dates_before_current_date

class ValidDatesTest(GedcomTestCase):

    def test_divorce_before_death(self) -> None:
        """ test divorce_before_death """

        self.assert_file_validation_fails('invalid_dates', divorce_before_death, 
        ['ERROR US06: Divorce date (at line 135) for Family(F4) occurs after Husband(I7) death date (at line 69).'])

        self.assert_file_validation_passes('valid_divorce_dates', divorce_before_death)
    
    def test_dates_before_current_date(self) -> None:
        """ test dates_before_current_date """

        self.assert_file_validation_fails('invalid_future_dates', dates_before_current_date, 
        [
            'ERROR US01: Family(F2) marriage date (at line 121) occurs after current date.', 
            'ERROR US01: Family(F5) divorce date (at line 143) occurs after current date.', 
            'ERROR US01: Individual(I1) birth date (at line 8) occurs after current date.', 
            'ERROR US01: Individual(I5) death date (at line 48) occurs after current date.'
        ])

        self.assert_file_validation_passes('valid_dates_before_today', dates_before_current_date)

