from typing import Optional, List
from datetime import datetime
from .base import GedcomData, GedcomSubjectData
from .date import GedcomDateEvent
from ..exceptions import GedcomInvalidData


class GedcomIndividualData(GedcomData):
    ''' GEDCOM data belonging to INDI '''
    belongs_to = 'INDI'
    level = 1


class GedcomIndividualName(GedcomIndividualData):
    ''' GEDCOM 1 NAME {name} '''
    __slots__ = 'name'

    tag = 'NAME'

    def parse_lines(self) -> bool:
        # name cannot be empty
        if not self.line.arguments:
            raise GedcomInvalidData('single argument required')

        self._name: str = ' '.join(self.line.arguments)

        return True


class GedcomIndividualSex(GedcomIndividualData):
    ''' GEDCOM 1 SEX {'M'|'F'} data '''
    __slots__ = 'sex'

    tag = 'SEX'

    def parse_lines(self) -> bool:
        # sex cannot be empty
        if self.line.arguments_count != 1:
            raise GedcomInvalidData('single argument required')

        sex: str = self.line.argument

        # sex can only be M or F
        if sex not in ('M', 'F'):
            raise GedcomInvalidData('M or F required')

        self._sex: str = sex

        return True


class GedcomIndividualMemberOf(GedcomIndividualData):
    ''' GEDCOM individual relation (FAMC/FAMS) data base object '''
    __slots__ = 'family_id'

    def parse_lines(self) -> bool:
        # only a single argument for family ID
        if self.line.arguments_count != 1:
            raise GedcomInvalidData('single argument family ID required')

        self.family_id: str = self.line.argument

        return True


class GedcomIndividualChildOf(GedcomIndividualMemberOf):
    ''' GEDCOM 1 FAMC {family_id} '''
    tag = 'FAMC'


class GedcomIndividualSpouseOf(GedcomIndividualMemberOf):
    ''' GEDCOM 1 FAMS {family_id} '''
    tag = 'FAMS'


class GedcomIndividualBirth(GedcomDateEvent):
    ''' GEDCOM 1 BIRT '''
    belongs_to = 'INDI'
    level = 1
    tag = 'BIRT'


class GedcomIndividualDeath(GedcomDateEvent):
    ''' GEDCOM 1 DEAT '''
    belongs_to = 'INDI'
    level = 1
    tag = 'DEAT'


class GedcomIndividual(GedcomSubjectData):
    ''' GEDCOM 0 {id} INDI '''
    __slots__ = '_name', '_sex', '_birth', '_death', '_child_of_list', '_spouse_of_list'

    tag = 'INDI'
    info_tags = 'NAME', 'SEX', 'FAMC', 'FAMS', 'BIRT', 'DEAT'
    event_tags = 'BIRT', 'DEAT'

    @property
    def name(self) -> Optional[str]:
        ''' get individual name '''
        return self._name.name

    @property
    def sex(self) -> Optional[str]:
        ''' get individual sex '''
        return self._sex.sex

    @property
    def birth(self) -> Optional[datetime]:
        ''' get individual birth datetime object '''
        return self._birth.date

    @property
    def death(self) -> Optional[datetime]:
        ''' get individual death datetime object '''
        return self._death.date

    def get_member_of_id(self, member_of: GedcomIndividualMemberOf) -> Optional[str]:
        ''' get the family_id of which this individual is a member of, None if invalid '''
        return member_of.family_id if member_of else None

    @property
    def spouse_of_list(self) -> List[str]:
        ''' get list of family_id which this individual is a spouse '''
        return [self.get_member_of_id(spouse_of) for spouse_of in self._spouse_of_list]

    @property
    def child_of_list(self) -> List[str]:
        ''' get list of family_id which this individual is a child '''
        return [self.get_member_of_id(child_of) for child_of in self._child_of_list]

    def set_default_values(self) -> None:
        self._name = None
        self._sex = None
        self._birth = None
        self._death = None
        self._child_of_list: List[GedcomIndividualChildOf] = []
        self._spouse_of_list: List[GedcomIndividualSpouseOf] = []

    def is_member(self, family_id: str) -> bool:
        ''' check if individual is a member of family'''
        ofs: List[GedcomIndividualMemberOf] = self._child_of_list + \
            self._spouse_of_list
        return [of for of in ofs if of.family_id == family_id]

    def parse_info_line(self, index: int) -> bool:
        info_line: GedcomLine = self.lines[index]
        tag: str = info_line.tag

        # keep track of lines for the same piece of data
        data_lines: List[GedcomLine] = [info_line]

        if tag in self.event_tags:
            # expect next line to be DATE
            data_lines.append(self.lines[index + 1])

            if tag == 'BIRT':
                if self.has_info(self._birth):
                    raise GedcomInvalidData('Duplicate individual birth date')

                self._birth = GedcomIndividualBirth(data_lines)

            elif tag == 'DEAT':
                if self.has_info(self._death):
                    raise GedcomInvalidData('Duplicate individual death date')

                self._death = GedcomIndividualDeath(data_lines)

        elif tag == 'NAME':
            if self.has_info(self._name):
                raise GedcomInvalidData('Duplicate individual name')

            self._name = GedcomIndividualName(data_lines)

        elif tag == 'SEX':
            if self.has_info(self._sex):
                raise GedcomInvalidData('Duplicate individual sex')

            self._sex = GedcomIndividualSex(data_lines)

        elif tag == 'FAMC':
            child_of = GedcomIndividualChildOf(data_lines)

            if self.is_member(child_of.family_id):
                child_of.validated = False
                raise GedcomInvalidData(
                    'Duplicate family membership for individual')

            self._child_of_list.append(child_of)

        elif tag == 'FAMS':
            spouse_of = GedcomIndividualSpouseOf(data_lines)

            if self.is_member(spouse_of.family_id):
                spouse_of.validated = False
                raise GedcomInvalidData(
                    'Duplicate family membership for individual')

            self._spouse_of_list.append(spouse_of)
