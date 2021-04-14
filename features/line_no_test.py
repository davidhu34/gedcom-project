from gedcom.testing import GedcomTestCase


class LineNoTest(GedcomTestCase):

    def test_line_no(self) -> None:
        """ test GecomData line number property """
        repo: GedcomRepository = self.parse_test_file('test')
        i01a, i01b, i02, i03, i04, i05, i06, i07, i08, i09 = repo.individuals
        f01a, f01b, f02, f03, f04, f05 = repo.families

        self.assertEqual(i01a.line_no, 3)
        self.assertEqual(i01a.name_line_no, 4)
        self.assertEqual(i01a.sex_line_no, 5)
        self.assertEqual(i01a.birth_line_no, 6)
        self.assertEqual(i01b.death_line_no, None)
        self.assertEqual(i01a.child_of_line_no_list, [8])
        self.assertEqual(i01a.spouse_of_line_no_list, [])

        self.assertEqual(i01b.line_no, 71)
        self.assertEqual(i01b.name_line_no, 72)
        self.assertEqual(i01b.sex_line_no, 73)
        self.assertEqual(i01b.birth_line_no, 74)
        self.assertEqual(i01b.death_line_no, None)
        self.assertEqual(i01b.child_of_line_no_list, [76])
        self.assertEqual(i01b.spouse_of_line_no_list, [])

        self.assertEqual(i02.line_no, 10)
        self.assertEqual(i02.name_line_no, 11)
        self.assertEqual(i02.sex_line_no, 12)
        self.assertEqual(i02.birth_line_no, 13)
        self.assertEqual(i02.death_line_no, 15)
        self.assertEqual(i02.child_of_line_no_list, [])
        self.assertEqual(i02.spouse_of_line_no_list, [17])

        self.assertEqual(i03.line_no, 19)
        self.assertEqual(i03.name_line_no, 20)
        self.assertEqual(i03.sex_line_no, 21)
        self.assertEqual(i03.birth_line_no, 22)
        self.assertEqual(i03.death_line_no, 24)
        self.assertEqual(i03.child_of_line_no_list, [28])
        self.assertEqual(i03.spouse_of_line_no_list, [26, 27])

        self.assertEqual(i04.line_no, 30)
        self.assertEqual(i04.name_line_no, 31)
        self.assertEqual(i04.sex_line_no, 32)
        self.assertEqual(i04.birth_line_no, 33)
        self.assertEqual(i04.death_line_no, None)
        self.assertEqual(i04.child_of_line_no_list, [35])
        self.assertEqual(i04.spouse_of_line_no_list, [])

        self.assertEqual(i05.line_no, 38)
        self.assertEqual(i05.name_line_no, 39)
        self.assertEqual(i05.sex_line_no, 40)
        self.assertEqual(i05.birth_line_no, 41)
        self.assertEqual(i05.death_line_no, 43)
        self.assertEqual(i05.child_of_line_no_list, [])
        self.assertEqual(i05.spouse_of_line_no_list, [45])

        self.assertEqual(i06.line_no, 47)
        self.assertEqual(i06.name_line_no, 48)
        self.assertEqual(i06.sex_line_no, 49)
        self.assertEqual(i06.birth_line_no, 50)
        self.assertEqual(i06.death_line_no, None)
        self.assertEqual(i06.child_of_line_no_list, [52])
        self.assertEqual(i06.spouse_of_line_no_list, [])

        self.assertEqual(i07.line_no, 54)
        self.assertEqual(i07.name_line_no, 55)
        self.assertEqual(i07.sex_line_no, 56)
        self.assertEqual(i07.birth_line_no, 57)
        self.assertEqual(i07.death_line_no, None)
        self.assertEqual(i07.child_of_line_no_list, [])
        self.assertEqual(i07.spouse_of_line_no_list, [59])

        self.assertEqual(i08.line_no, 61)
        self.assertEqual(i08.name_line_no, 62)
        self.assertEqual(i08.sex_line_no, 63)
        self.assertEqual(i08.birth_line_no, 64)
        self.assertEqual(i08.death_line_no, 66)
        self.assertEqual(i08.child_of_line_no_list, [])
        self.assertEqual(i08.spouse_of_line_no_list, [68])

        self.assertEqual(f01a.line_no, 77)
        self.assertEqual(f01a.husband_line_no, 80)
        self.assertEqual(f01a.wife_line_no, 81)
        self.assertEqual(f01a.children_line_no_list, [82, 83, 84])
        self.assertEqual(f01a.marriage_line_no, 78)
        self.assertEqual(f01a.divorce_line_no, None)

        self.assertEqual(f01b.line_no, 120)
        self.assertEqual(f01b.husband_line_no, 123)
        self.assertEqual(f01b.wife_line_no, 124)
        self.assertEqual(f01b.children_line_no_list, [125])
        self.assertEqual(f01b.marriage_line_no, 121)
        self.assertEqual(f01b.divorce_line_no, None)

        self.assertEqual(f02.line_no, 86)
        self.assertEqual(f02.husband_line_no, 91)
        self.assertEqual(f02.wife_line_no, 92)
        self.assertEqual(f02.children_line_no_list, [93])
        self.assertEqual(f02.marriage_line_no, 87)
        self.assertEqual(f02.divorce_line_no, 89)

        self.assertEqual(f03.line_no, 95)
        self.assertEqual(f03.husband_line_no, 101)
        self.assertEqual(f03.wife_line_no, 100)
        self.assertEqual(f03.children_line_no_list, [102])
        self.assertEqual(f03.marriage_line_no, 96)
        self.assertEqual(f03.divorce_line_no, 98)

        self.assertEqual(f04.line_no, 104)
        self.assertEqual(f04.husband_line_no, 107)
        self.assertEqual(f04.wife_line_no, 108)
        self.assertEqual(f04.children_line_no_list, [])
        self.assertEqual(f04.marriage_line_no, 105)
        self.assertEqual(f04.divorce_line_no, None)

        self.assertEqual(f05.line_no, 109)
        self.assertEqual(f05.husband_line_no, 112)
        self.assertEqual(f05.wife_line_no, 113)
        self.assertEqual(f05.children_line_no_list, [])
        self.assertEqual(f05.marriage_line_no, 110)
        self.assertEqual(f05.divorce_line_no, None)
