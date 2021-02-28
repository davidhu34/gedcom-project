from typing import Any, Optional, Iterator, IO, List, Dict
from datetime import datetime
from abc import ABCMeta, abstractmethod


class FileNotFound(Exception):
    ''' custom file not found exception '''

    def __init__(self, message, path) -> None:
        # construct exception and store erroneous path if given
        super().__init__(message)
        self.path = path


class GedcomException(Exception):
    ''' custom GEDCOM base exception '''

    def __init__(self, message='') -> None:
        # construct exception and store erroneous path if given
        super().__init__(message)


class GedcomLineParsingException(GedcomException):
    pass


class GedcomDataParsingException(GedcomException):
    pass


class GedcomInvalidData(GedcomException):
    pass


class GedcomDateInvalidFormat(GedcomException):
    pass


class GedcomLine:
    ''' parsed GEDCOM file line '''
    __slots__ = 'data', 'level', 'tag', 'arguments', 'validated'

    def __init__(self, line: str) -> None:
        try:
            level, *tokens = line.split()
            self.level: int = int(level)

            # handles special tag positions
            indi_or_fam: bool = level == '0' and tokens[-1] in ('INDI', 'FAM')
            tag, *arguments = [tokens[1], tokens[0]] if indi_or_fam else tokens

            self.data = line
            self.tag: str = tag
            self.arguments: List[str] = arguments
            self.validated: bool = False

        except:
            # error in tokens counts or integer cast
            raise GedcomLineParsingException('line parsing failed')

    @property
    def argument(self) -> str:
        return self.arguments[0]

    @property
    def arguments_count(self) -> int:
        return len(self.arguments)


class GedcomData(metaclass=ABCMeta):
    ''' GEDCOM data base object '''
    # __slots__ = 'lines', '_level', 'parents', 'children'

    belongs_to: Optional[str] = None

    # @property
    # def level(self) -> int:
    #     return self._level;

    # @level.setter
    # def level(self, l: int) -> None:

    #     self._level = l

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

    # def __init__(self, lines: List[GedcomLine], level: Optional[int] = None) -> None:
    def __init__(self, lines: List[GedcomLine]) -> None:
        self.lines: List[GedcomLine] = lines
        # self.parents: List[GedcomData] = []
        # self.childern: List[GedcomData] = []
        # if level != None:
        #     self.level = level

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
            # print('parse_line error', e, self.line.data)
            pass

        else:
            # validate lines if no data parsing error
            self.validate_lines()


class GedcomNote(GedcomData):
    ''' GEDCOM 0 NOTE {note} data '''
    __slots__ = 'note'

    level = 0
    tag = 'NOTE'

    def parse_lines(self) -> bool:
        self.note = ' '.join(self.line.arguments)

        return True


class GedcomTagOnlyData(GedcomData):
    ''' GEDCOM no argument data base object '''

    def parse_lines(self) -> bool:
        # no argumets allowed
        if self.line.arguments:
            raise GedcomInvalidData(f'{self.tag} no argumets allowed')

        return True


class GedcomHeader(GedcomTagOnlyData):
    ''' GEDCOM 0 HEAD '''
    level = 0
    tag = 'HEAD'


class GedcomTrailer(GedcomTagOnlyData):
    ''' GEDCOM 0 TRLR '''
    level = 0
    tag = 'TRLR'


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

        date: int = int(d)
        month: int = self.month_map[mmm]
        year: int = int(yyyy)

        if not month:
            raise GedcomInvalidData('invalid date month')

        self.date: datetime = datetime(year, month, date)

        return True


class GedcomDateEvent(GedcomTagOnlyData):
    ''' GEDCOM entry preceding DATE '''
    __slots__ = 'date'

    level = 1
    # def validate_line(self) -> None:
    #     ''' validate lines for DATE event '''
    #     for line in self.lines[0:2]:
    #         line.validated = True

    def parse_lines(self) -> bool:
        # super().parse_lines()

        # no argumets allowed
        if self.line.arguments:
            raise GedcomInvalidData('event no argumets allowed')

        date_line: GedcomLine = self.lines[1]
        date: GedcomDate = GedcomDate([date_line])

        if date.validated:
            self.date = date
            return True

        else:
            return False


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
                # print('parse info line', e, self.line.data)
                pass

        return True


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
    __slots__ = 'name', 'sex', 'birth', 'death', 'child_of_list', 'spouse_of_list'

    tag = 'INDI'
    info_tags = 'NAME', 'SEX', 'FAMC', 'FAMS', 'BIRT', 'DEAT'
    event_tags = 'BIRT', 'DEAT'

    def set_default_values(self) -> None:
        self.name = None
        self.sex = None
        self.birth = None
        self.death = None
        self.child_of_list: List[GedcomIndividualChildOf] = []
        self.spouse_of_list: List[GedcomIndividualSpouseOf] = []

    def is_member(self, family_id: str) -> bool:
        ''' check if individual is a member of family'''
        ofs: List[GedcomIndividualMemberOf] = self.child_of_list + \
            self.spouse_of_list
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
                if self.has_info(self.birth):
                    raise GedcomInvalidData('Duplicate individual birth date')

                self.birth = GedcomIndividualBirth(data_lines)

            elif tag == 'DEAT':
                if self.has_info(self.death):
                    raise GedcomInvalidData('Duplicate individual death date')

                self.death = GedcomIndividualDeath(data_lines)

        elif tag == 'NAME':
            if self.has_info(self.name):
                raise GedcomInvalidData('Duplicate individual name')

            self.name = GedcomIndividualName(data_lines)

        elif tag == 'SEX':
            if self.has_info(self.sex):
                raise GedcomInvalidData('Duplicate individual sex')

            self.sex = GedcomIndividualSex(data_lines)

        elif tag == 'FAMC':
            child_of = GedcomIndividualChildOf(data_lines)

            if self.is_member(child_of.family_id):
                child_of.validated = False
                raise GedcomInvalidData(
                    'Duplicate family membership for individual')

            self.child_of_list.append(child_of)

        elif tag == 'FAMS':
            spouse_of = GedcomIndividualSpouseOf(data_lines)

            if self.is_member(spouse_of.family_id):
                spouse_of.validated = False
                raise GedcomInvalidData(
                    'Duplicate family membership for individual')

            self.spouse_of_list.append(spouse_of)


class GedcomFamilyData(GedcomData):
    ''' GEDCOM data belonging to FAM '''
    belongs_to = 'FAM'
    level = 1


class GedcomFamilyMember(GedcomFamilyData):
    ''' GEDCOM family member data (HUSB/WIFE/CHIL) base object '''
    __slots__ = 'individual_id'

    def parse_lines(self) -> bool:
        # only a single argument for individual ID
        if self.line.arguments_count != 1:
            raise GedcomInvalidData('single argument individual ID required')

        self.individual_id: str = self.line.argument

        return True


class GedcomFamilyHusband(GedcomFamilyMember):
    ''' GEDCOM 1 HUSB {individual_id} '''
    tag = 'HUSB'


class GedcomFamilyWife(GedcomFamilyMember):
    ''' GEDCOM 1 WIFE {individual_id} '''
    tag = 'WIFE'


class GedcomFamilyChild(GedcomFamilyMember):
    ''' GEDCOM 1 CHIL {individual_id} '''
    tag = 'CHIL'


class GedcomFamilyMarriage(GedcomDateEvent):
    ''' GEDCOM 1 MARR '''
    belongs_to = 'FAM'
    level = 1
    tag = 'MARR'


class GedcomFamilyDivorce(GedcomDateEvent):
    ''' GEDCOM 1 DIV '''
    belongs_to = 'FAM'
    level = 1
    tag = 'DIV'


class GedcomFamily(GedcomSubjectData):
    ''' GEDCOM 0 {id} FAM '''
    __slots__ = 'husband', 'wife', 'marriage', 'divorce', 'children'

    tag = 'FAM'
    info_tags = 'HUSB', 'WIFE', 'CHIL', 'MARR', 'DIV'
    event_tags = 'MARR', 'DIV'

    def set_default_values(self) -> None:
        self.husband = None
        self.wife = None
        self.marriage = None
        self.divorce = None
        self.children: List[GedcomFamilyChild] = []

    def is_member(self, individual_id: str) -> bool:
        ''' check if individual is in this family '''
        return (self.husband and self.husband.individual_id == individual_id
                ) or (self.wife and self.wife.individual_id == individual_id
                      ) or [child for child in self.children if child.individual_id == individual_id]

    def parse_info_line(self, index: int) -> bool:
        info_line: GedcomLine = self.lines[index]
        tag: str = info_line.tag

        data_lines: List[GedcomLine] = [info_line]

        if tag in self.event_tags:
            # expect next line to be DATE
            data_lines.append(self.lines[index + 1])

            if tag == 'MARR':
                if self.has_info(self.marriage):
                    raise GedcomInvalidData('Duplicate family marriage date')

                self.marriage = GedcomFamilyMarriage(data_lines)

            elif tag == 'DIV':
                if self.has_info(self.divorce):
                    raise GedcomInvalidData('Duplicate family divorce date')

                self.divorce = GedcomFamilyDivorce(data_lines)

        elif tag == 'HUSB':
            if self.has_info(self.husband):
                raise GedcomInvalidData('Duplicate family husband')

            husband = GedcomFamilyHusband(data_lines)

            if self.is_member(husband.individual_id):
                child.validated = False
                raise GedcomInvalidData('Duplicate family role for individual')

            self.husband = husband

        elif tag == 'WIFE':
            if self.has_info(self.wife):
                raise GedcomInvalidData('Duplicate family wife')

            wife = GedcomFamilyWife(data_lines)

            if self.is_member(wife.individual_id):
                wife.validated = False
                raise GedcomInvalidData('Duplicate family role for individual')

            self.wife = wife

        elif tag == 'CHIL':
            child = GedcomFamilyChild(data_lines)

            if self.is_member(child.individual_id):
                child.validated = False
                raise GedcomInvalidData('Duplicate family role for individual')

            self.children.append(child)


def get_lines_from_file(file: IO) -> Iterator[str]:
    ''' a generator yielding lines from file object '''
    with file:
        # loop through file line sequence
        for raw_line in file:
            # remove trailing new line
            line: str = raw_line.rstrip('\n')
            # if line ends with a slash
            yield GedcomLine(line)


def get_lines_from_path(path: str) -> Iterator[str]:
    ''' a generator yielding lines of file from path '''
    # read file from path
    try:
        file: IO = open(path)

    # handle file not found
    except FileNotFoundError:
        raise FileNotFound(f'Cannot open file "{path}"!', path)

    # yield lines form a generator function
    else:
        lines: List[GedcomLine] = get_lines_from_file(file)
        return lines


def parse_and_validate(lines: List[GedcomLine]) -> None:
    ''' get data from lines and validate '''
    notes: List[GedcomNotes] = []
    individual_dict: Dict[str, GedcomIndividual] = {}
    family_dict: Dict[str, GedcomFamily] = {}

    i: int = 0
    while i < len(lines):
        line = lines[i]
        level: str = line.level
        tag: str = line.tag

        data_lines: [GedcomLine] = [line]
        if tag in ('INDI', 'FAM'):
            i += 1
            while lines[i].level != 0:
                data_lines.append(lines[i])
                i += 1

            try:
                if tag == 'INDI':
                    individual = GedcomIndividual(data_lines)
                    individual_dict[individual.id] = individual

                if tag == 'FAM':
                    family = GedcomFamily(data_lines)
                    family_dict[family.id] = family

            except:
                # skip invalid subject(INDI/FaM)
                # along with following lines without a valid subject
                pass

        else:
            try:
                if tag == 'NOTE':
                    notes.append(GedcomNote(data_lines))

                elif tag == 'HEAD':
                    header = GedcomHeader(data_lines)

                elif tag == 'TRLR':
                    trailer = GedcomTrailer(data_lines)

            except:
                # skip invalid top level tags
                pass

            i += 1

    for l in lines:
        print(f'--> {l.data}')
        print(
            f'<-- {l.level}|{l.tag}|{"Y" if l.validated else "N"}|{" ".join(l.arguments)}')


def run_project_2() -> None:
    ''' main function for project 2 '''
    input_path = input(
        'Enter GEDCOM file (i.g. "test.ged" or "./test.ged"): ')
    path: str = input_path if input_path else 'test.ged'
    lines: List[GedcomLine] = get_lines_from_path(path)
    parse_and_validate([l for l in lines])


if __name__ == "__main__":
    run_project_2()
