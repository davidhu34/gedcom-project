from .base import GedcomData, GedcomTagOnlyData
from ..exceptions import GedcomInvalidData

class GedcomNote(GedcomData):
    ''' GEDCOM 0 NOTE {note} data '''
    __slots__ = 'note'

    level = 0
    tag = 'NOTE'

    def parse_lines(self) -> bool:
        self.note = ' '.join(self.line.arguments)

        return True


class GedcomHeader(GedcomTagOnlyData):
    ''' GEDCOM 0 HEAD '''
    level = 0
    tag = 'HEAD'


class GedcomTrailer(GedcomTagOnlyData):
    ''' GEDCOM 0 TRLR '''
    level = 0
    tag = 'TRLR'

