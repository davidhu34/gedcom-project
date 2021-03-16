from typing import Optional, List
from datetime import date as Date
from .base import GedcomData, GedcomSubjectData
from .date import GedcomDateEvent
from ..exceptions import GedcomInvalidData


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
    __slots__ = '_husband', '_wife', '_marriage', '_divorce', '_children'

    tag = 'FAM'
    info_tags = 'HUSB', 'WIFE', 'CHIL', 'MARR', 'DIV'
    event_tags = 'MARR', 'DIV'

    def _get_member_id(self, member: GedcomFamilyMember) -> Optional[str]:
        ''' get member individual_id, None if member is not valid '''
        return member.individual_id if member else None

    @property
    def husband_id(self) -> Optional[str]:
        ''' get husband individual_id '''
        return self._get_member_id(self._husband)

    @property
    def husband(self) -> Optional[str]:
        ''' get husband '''
        return self._repo.individual[self.husband_id]

    @property
    def husband_line_no(self) -> Optional[str]:
        ''' get husband line number '''
        return self._husband.line_no

    @property
    def wife_id(self) -> Optional[str]:
        ''' get husband individual_id '''
        return self._get_member_id(self._wife)

    @property
    def wife(self) -> Optional[str]:
        ''' get wife '''
        return self._repo.individual[self.wife_id]

    @property
    def wife_line_no(self) -> Optional[str]:
        ''' get wife line number '''
        return self._wife.line_no

    @property
    def children_id_list(self) -> List[str]:
        ''' get list of children individual_id '''
        return [self._get_member_id(_child) for _child in self._children]

    @property
    def children(self) -> List[str]:
        ''' get list of children '''
        return [self._repo.individual[child_id] for child_id in self.children_id_list]

    @property
    def children_line_no_list(self) -> List[str]:
        ''' get list of children line numbers '''
        return [_child.line_no for _child in self._children]

    @property
    def marriage(self) -> Optional[Date]:
        ''' get Date object of marriage '''
        return self._marriage.date if self._marriage else None

    @property
    def marriage_line_no(self) -> Optional[str]:
        ''' get marriage line number '''
        return self._marriage.line_no

    @property
    def divorce(self) -> Optional[Date]:
        ''' get Date object of divorce '''
        return self._divorce.date if self._divorce else None

    @property
    def divorce_line_no(self) -> Optional[str]:
        ''' get divorce line number '''
        return self._divorce.line_no

    def set_default_values(self) -> None:
        self._husband = None
        self._wife = None
        self._marriage = None
        self._divorce = None
        self._children: List[GedcomFamilyChild] = []

    def has_member(self, individual_id: str) -> bool:
        ''' check if individual is in this family '''
        return (self._husband and self._husband.individual_id == individual_id
                ) or (self._wife and self._wife.individual_id == individual_id
                      ) or [child for child in self._children if child.individual_id == individual_id]

    def parse_info_line(self, index: int) -> bool:
        info_line: GedcomLine = self.lines[index]
        tag: str = info_line.tag

        data_lines: List[GedcomLine] = [info_line]

        if tag in self.event_tags:
            # expect next line to be DATE
            data_lines.append(self.lines[index + 1])

            if tag == 'MARR':
                if self.has_info(self._marriage):
                    raise GedcomInvalidData('Duplicate family marriage date')

                self._marriage = GedcomFamilyMarriage(data_lines, self._repo)

            elif tag == 'DIV':
                if self.has_info(self._divorce):
                    raise GedcomInvalidData('Duplicate family divorce date')

                self._divorce = GedcomFamilyDivorce(data_lines, self._repo)

        elif tag == 'HUSB':
            if self.has_info(self._husband):
                raise GedcomInvalidData('Duplicate family husband')

            husband = GedcomFamilyHusband(data_lines, self._repo)

            if self.has_member(husband.individual_id):
                child.validated = False
                raise GedcomInvalidData('Duplicate family role for individual')

            self._husband = husband

        elif tag == 'WIFE':
            if self.has_info(self._wife):
                raise GedcomInvalidData('Duplicate family wife')

            wife = GedcomFamilyWife(data_lines, self._repo)

            if self.has_member(wife.individual_id):
                wife.validated = False
                raise GedcomInvalidData('Duplicate family role for individual')

            self._wife = wife

        elif tag == 'CHIL':
            child = GedcomFamilyChild(data_lines, self._repo)

            if self.has_member(child.individual_id):
                child.validated = False
                raise GedcomInvalidData('Duplicate family role for individual')

            self._children.append(child)
