from gedcom.testing import GedcomTestCase
from features.id_validations import unique_ids, corresponding_entries


class IdValidationsTest(GedcomTestCase):

    def test_unique_ids(self) -> None:
        """ test unique_ids """

        self.assert_file_validation_fails(
            'not_unique_ids', unique_ids,
            [
                'ERROR US22: Individual ID (I02) is not unique (at line 10, 55)',
                'ERROR US22: Family ID (F01) is not unique (at line 69, 85)'
            ])

        self.assert_file_validation_passes('valid_ids', unique_ids)

    def test_corresponding_entries(self) -> None:
        """ test corresponding_entries """

        self.assert_file_validation_fails(
            'not_corresponding_entries', corresponding_entries,
            [
                'ERROR US26: Individual(I01) is not a spouse of (at line 9) the corresponding family(F02 at line 81)',
                'ERROR US26: Individual(I06) is not a spouse of (at line 53) the corresponding family(F11 not found)',
                'ERROR US26: Individual(I07) is not a child of (at line 62) the corresponding family(F01 at line 72)',
                'ERROR US26: Individual(I08) is not a child of (at line 70) the corresponding family(F12 not found)',
                'ERROR US26: Family(F01) child at line 78 does not correspond to individual(I06 at line 48)',
                'ERROR US26: Family(F04) spouse at line 100 does not correspond to individual(I12 not found)',
                'ERROR US26: Family(F04) spouse at line 99 does not correspond to individual(I01 at line 3)',
                'ERROR US26: Family(F04) child at line 101 does not correspond to individual(I13 not found)'
            ])

        self.assert_file_validation_passes('valid_ids', corresponding_entries)
