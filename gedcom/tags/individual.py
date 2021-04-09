from typing import Optional, List, Tuple
from datetime import date as Date
import re
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

        self.name: str = ' '.join(self.line.arguments)

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

        self.sex: str = sex

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

    def _get_name_parts(self) -> Tuple[str]:
        ''' returns individual (first_name, last_name)'''
        name: str = self.name
        slash_indices: List[int] = [
            i for i, c in enumerate(self.name) if c == '/']

        if len(slash_indices) != 2:
            return (name)

        first_name: str = name[0: slash_indices[0]].strip()
        last_name: str = name[slash_indices[0] + 1: slash_indices[1]].strip()
        return (first_name, last_name)

    @property
    def first_name(self) -> Optional[str]:
        ''' get individual first name '''
        return self._get_name_parts()[0]

    @property
    def last_name(self) -> Optional[str]:
        ''' get individual last name '''
        name_parts: Tuple[str] = self._get_name_parts()
        return name_parts[1] if len(name_parts) == 2 else None

    @property
    def name_line_no(self) -> Optional[int]:
        ''' get individual name line number '''
        return self._get_line_no(self._name)

    @property
    def sex(self) -> Optional[str]:
        ''' get individual sex '''
        return self._sex.sex

    @property
    def sex_line_no(self) -> Optional[int]:
        ''' get individual sex line number '''
        return self._get_line_no(self._sex)

    @property
    def is_male(self) -> Optional[str]:
        ''' individual is male '''
        return self.sex == 'M'

    @property
    def is_female(self) -> Optional[str]:
        ''' individual is female '''
        return self.sex == 'F'

    @property
    def birth(self) -> Optional[Date]:
        ''' get individual birth date object '''
        return self._birth.date if self._birth else None

    @property
    def birth_line_no(self) -> Optional[int]:
        ''' get individual birth line number '''
        return self._get_line_no(self._birth)

    @property
    def death(self) -> Optional[Date]:
        ''' get individual death date object '''
        return self._death.date if self._death else None

    @property
    def death_line_no(self) -> Optional[int]:
        ''' get individual death line number '''
        return self._get_line_no(self._death)

    def age_at(self, date: Date = Date.today()) -> int:
        ''' get individual age at death, or else age at input date '''

        end_date: Date = self.death if self.death and self.death < date else date
        birth_date: Date = self.birth
        this_birth_date: Date = Date(
            end_date.year, birth_date.month, birth_date.day)

        return end_date.year - birth_date.year - \
            (1 if end_date < this_birth_date else 0)

    @property
    def age(self) -> int:
        ''' get individul age at the moment (today) '''
        # default: age at today
        return self.age_at()

    def _get_member_of_id(self, member_of: GedcomIndividualMemberOf) -> Optional[str]:
        ''' get the family_id of which this individual is a member of, None if invalid '''
        return member_of.family_id if member_of else None

    @property
    def spouse_of_id_list(self) -> List[str]:
        ''' get list of family_id which this individual is a spouse '''
        return [self._get_member_of_id(_spouse_of) for _spouse_of in self._spouse_of_list]

    @property
    def spouse_of_list(self) -> List[str]:
        ''' get list of families which this individual is a spouse '''
        return [spouse_of for spouse_of in [self._repo.family[spouse_of_id] for spouse_of_id in self.spouse_of_id_list] if spouse_of]

    @property
    def spouse_of_line_no_list(self) -> List[int]:
        ''' get list of line numbers which this individual is a spouse '''
        return [self._get_line_no(_spouse_of) for _spouse_of in self._spouse_of_list]

    @property
    def child_of_id_list(self) -> List[str]:
        ''' get list of family_id which this individual is a child '''
        return [self._get_member_of_id(_child_of) for _child_of in self._child_of_list]

    @property
    def child_of_list(self) -> List[str]:
        ''' get list of families which this individual is a child '''
        return [child_of for child_of in [self._repo.family[child_of_id] for child_of_id in self.child_of_id_list] if child_of]

    @property
    def child_of_line_no_list(self) -> List[int]:
        ''' get list of line numbers which this individual is a spouse '''
        return [self._get_line_no(_child_of) for _child_of in self._child_of_list]

    @property
    def member_of_id_list(self) -> List[str]:
        ''' get list of family_id which this individual is a member '''
        return [_member_of.family_id for _member_of in self._child_of_list + self._spouse_of_list]

    @property
    def member_of_list(self) -> List[str]:
        ''' get list of families which this individual is a member '''
        return [member_of for member_of in [self._repo.family[member_of_id] for member_of_id in self.member_of_id_list] if member_of]

    @property
    def member_of_line_no_list(self) -> List[int]:
        ''' get list of line numbers which this individual is a member '''
        return [self._get_line_no(_member_of) for _member_of in self._child_of_list + self._spouse_of_list]

    def set_default_values(self) -> None:
        self._name = None
        self._sex = None
        self._birth = None
        self._death = None
        self._child_of_list: List[GedcomIndividualChildOf] = []
        self._spouse_of_list: List[GedcomIndividualSpouseOf] = []

    def is_member_of(self, family_id: str) -> bool:
        ''' check if individual is a member of family'''
        return (family_id in self.member_of_id_list)

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

                self._birth = GedcomIndividualBirth(data_lines, self._repo)

            elif tag == 'DEAT':
                if self.has_info(self._death):
                    raise GedcomInvalidData('Duplicate individual death date')

                self._death = GedcomIndividualDeath(data_lines, self._repo)

        elif tag == 'NAME':
            if self.has_info(self._name):
                raise GedcomInvalidData('Duplicate individual name')

            self._name = GedcomIndividualName(data_lines, self._repo)

        elif tag == 'SEX':
            if self.has_info(self._sex):
                raise GedcomInvalidData('Duplicate individual sex')

            self._sex = GedcomIndividualSex(data_lines, self._repo)

        elif tag == 'FAMC':
            child_of = GedcomIndividualChildOf(data_lines, self._repo)

            if self.is_member_of(child_of.family_id):
                child_of.validated = False
                raise GedcomInvalidData(
                    'Duplicate family membership for individual')

            self._child_of_list.append(child_of)

        elif tag == 'FAMS':
            spouse_of = GedcomIndividualSpouseOf(data_lines, self._repo)

            if self.is_member_of(spouse_of.family_id):
                spouse_of.validated = False
                raise GedcomInvalidData(
                    'Duplicate family membership for individual')

            self._spouse_of_list.append(spouse_of)
