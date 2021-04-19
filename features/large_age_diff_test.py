from gedcom.testing import GedcomTestCase
from features.large_age_diff import large_age_diff


class LargeAgeDiffTest(GedcomTestCase):

    def test_large_age_diff(self) -> None:
        """ test large_age_diff """

        self.assert_file_validation_fails(
            'large_age_diff', large_age_diff,
            [
                'ANOMALY US34: Family(F01 at line 86) spouse(I03) is more than twice as old as spouse(I02)',
                'ANOMALY US34: Family(F02 at line 95) spouse(I03) is more than twice as old as spouse(I05)'
            ])

        self.assert_file_validation_passes('no_large_age_diff', large_age_diff)
