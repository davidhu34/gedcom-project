from typing import Any, Optional, Iterator, IO, List, Dict
from abc import ABCMeta, abstractmethod
from ..file import GedcomLine
from ..exceptions import GedcomDataParsingException, GedcomInvalidData


class GedcomData(metaclass=ABCMeta):
    ''' GEDCOM data base object '''
    # __slots__ = 'lines', '_repo', '_level', 'parents', 'children'

    belongs_to: Optional[str] = None

    @property
    @abstractmethod
    def level(self) -> int:
        return -1

    @property
    @abstractmethod
    def tag(self) -> str:
        return ''

    @abstractmethod
    def parse_lines(self) -> bool:
        ''' return True if gedcom data source is valid '''
        return False

    @property
    def line(self) -> GedcomLine:
        return self.lines[0]

    @property
    def line_no(self) -> int:
        return self.line.line_no

    @property
    def validated(self) -> bool:
        return self.line.validated

    @validated.setter
    def validated(self, v: bool) -> None:
        self.line.validated = v

    def validate_lines(self) -> None:
        ''' validate lines for this GEDCOM data '''
        # default: validate first line only
        self.validated = True

    def set_default_values(self) -> None:
        ''' override to provide default values in __init__ '''
        pass

    def __init__(self, lines: List[GedcomLine], repo: 'GedcomRepository') -> None:
        self._repo: 'GedcomRepository' = repo
        self.lines: List[GedcomLine] = lines

        self.set_default_values()

        try:
            # check if parsed line is of known data type
            line: GedcomLine = lines[0]
            tag_mismatch: bool = line.tag != self.tag
            level_mismatch: bool = self.level != None and line.level != self.level
            if tag_mismatch or level_mismatch:
                raise GedcomDataParsingException(
                    'line and data type not matched')

            # parse line data by type
            done: bool = self.parse_lines()
            if not done:
                raise GedcomDataParsingException('data parsing failed')

        except Exception as e:
            pass

        else:
            # validate lines if no data parsing error
            self.validate_lines()


class GedcomTagOnlyData(GedcomData):
    ''' GEDCOM no argument data base object '''

    def parse_lines(self) -> bool:
        # no argumets allowed
        if self.line.arguments:
            raise GedcomInvalidData(f'{self.tag} no argumets allowed')

        return True


class GedcomSubjectData(GedcomData):
    ''' GEDCOM subject (INDI/FAM) data base object '''
    __slots__ = 'id'

    level = 0

    @abstractmethod
    def parse_info_line(self, index: int) -> bool:
        ''' parse data line of subject '''
        return False

    @property
    @abstractmethod
    def info_tags(self) -> List[str]:
        return []

    @property
    @abstractmethod
    def event_tags(self) -> List[str]:
        return []

    def _get_line_no(self, data: GedcomData) -> Optional[int]:
        ''' get line number of data object, None if no data '''
        return data.line_no if data else None

    def has_info(self, info: GedcomData) -> bool:
        return info and info.validated

    def parse_lines(self) -> bool:
        # tag has to be the last token
        if self.line.data.split()[-1] != self.line.tag:
            raise GedcomInvalidData(f'Incorrect {self.line.tag} format')

        # only a single argument for individual ID
        if self.line.arguments_count != 1:
            raise GedcomInvalidData('single argument individual id required')

        self.id: str = self.line.argument

        # parse data under this subject
        for index in range(1, len(self.lines)):
            info_line: GedcomLine = self.lines[index]
            tag: str = info_line.tag

            # DATE lines should be parsed by a preceding event tag
            if tag == 'DATE':
                continue

            if tag not in self.info_tags:
                continue
                # raise GedcomInvalidData()

            try:
                # parse line containing info of subject
                self.parse_info_line(index)

            except Exception as e:
                pass

        return True
