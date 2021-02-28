from typing import Dict, Optional
from datetime import date as Date
from .base import GedcomData, GedcomTagOnlyData
from ..exceptions import GedcomInvalidData


class GedcomDate(GedcomData):
    ''' GEDCOM 2 DATE {date} {month} {year}'''
    __slots__ = 'date'

    level = 2
    tag = 'DATE'
    month_map: Dict[str, int] = {
        'JAN': 1,
        'FEB': 2,
        'MAR': 3,
        'APR': 4,
        'MAY': 5,
        'JUN': 6,
        'JUL': 7,
        'AUG': 8,
        'SEP': 9,
        'OCT': 10,
        'NOV': 11,
        'DEC': 12,
    }

    # def validate_line(self) -> None:
    #     ''' cannot validate DATE line by itself '''
    #     pass

    def parse_lines(self) -> bool:
        d, mmm, yyyy = self.line.arguments

        if not d or not mmm or not yyyy:
            raise GedcomInvalidData(
                f'invalid date arguments {d} {mmm} {yyyy}')

        day: int = int(d)
        month: int = self.month_map[mmm]
        year: int = int(yyyy)

        if not month:
            raise GedcomInvalidData('invalid day month')

        self.date: Date = Date(year, month, day)

        return True


class GedcomDateEvent(GedcomTagOnlyData):
    ''' GEDCOM entry preceding DATE '''
    __slots__ = '_date'

    level = 1
    # def validate_line(self) -> None:
    #     ''' validate lines for DATE event '''
    #     for line in self.lines[0:2]:
    #         line.validated = True

    @property
    def date(self) -> Optional[Date]:
        ''' get date object of event '''
        return self._date.date if self._date else None

    def parse_lines(self) -> bool:
        # no argumets allowed
        if self.line.arguments:
            raise GedcomInvalidData('event no argumets allowed')

        date_line: GedcomLine = self.lines[1]
        date: GedcomDate = GedcomDate([date_line])

        self._date = date if date.validated else None
        return bool(self._date)
