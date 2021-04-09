from datetime import date as Date
from gedcom.testing import GedcomTestCase
from gedcom.tags import GedcomIndividual

class AgeTest(GedcomTestCase):
    test_date: Date = Date(836, 3, 29)

    def assertAgeAtEqual(self, individual: GedcomIndividual, age: int) -> None:
      ''' assert age_at of individual is equal to input age '''
      self.assertEqual(individual.age_at(self.test_date), age)

    def test_age_at(self) -> None:
        """ test GedcomIndividual age-at-date property """
        repo: GedcomRepository = self.parse_test_file('test')
        i01a, i01b, i02, i03, i04, i05, i06, i07, i08, i09 = repo.individuals

        self.assertAgeAtEqual(i01a, 0)
        self.assertAgeAtEqual(i01b, 1)
        self.assertAgeAtEqual(i02, 26)
        self.assertAgeAtEqual(i03, 30)
        self.assertAgeAtEqual(i04, 1)
        self.assertAgeAtEqual(i05, -2971)
        self.assertAgeAtEqual(i06, 10)
        self.assertAgeAtEqual(i07, 50)
        self.assertAgeAtEqual(i08, 20)
        self.assertAgeAtEqual(i09, 0)