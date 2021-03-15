from typing import Callable, Optional, List, Dict, Iterator
from .tags import *
from .file import GedcomLine, prompt_input_file, get_lines_from_path

Validator = Callable[['GedcomRepository'], Optional[List[str]]]
class GedcomRepository:
    ''' A Repository for GEDCOM file data '''
    __slots__ = 'lines', '_notes', '_header', '_trailer', '_individual_dict', '_family_dict', '_individual_keys', '_family_keys',

    def __init__(self, lines: List[GedcomLine]) -> None:
        ''' construct GedcomRepository '''
        self.parse_and_validate_lines(lines)

    @property
    def individual(self) -> Dict[str, GedcomIndividual]:
        ''' get individual id dictionary '''
        return self._individual_dict

    @property
    def family(self) -> Dict[str, GedcomFamily]:
        ''' get family id dictionary '''
        return self._family_dict

    @property
    def individuals(self) -> List[GedcomIndividual]:
        ''' get list of individuals ordered by id '''
        return [self.individual[id] for id in self._individual_keys]

    @property
    def families(self) -> List[GedcomFamily]:
        ''' get list of families ordered by id '''
        return [self.family[id] for id in self._family_keys]

    def reset_containers(self) -> None:
        self._notes: List[GedcomNotes] = []
        self._individual_keys: List[GedcomIndividual] = []
        self._family_keys: List[GedcomFamily] = []
        self._individual_dict: Dict[str, GedcomIndividual] = {}
        self._family_dict: Dict[str, GedcomFamily] = {}

    def parse_and_validate_lines(self, lines: List[GedcomLine]) -> None:
        ''' get data from lines and validate '''

        # cleanse data
        self.lines: List[GedcomLine] = lines
        self.reset_containers()

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
                        self._individual_dict[individual.id] = individual

                    if tag == 'FAM':
                        family = GedcomFamily(data_lines)
                        self._family_dict[family.id] = family

                except:
                    # skip invalid subject(INDI/FaM)
                    # along with following lines without a valid subject
                    pass

            else:
                try:
                    if tag == 'NOTE':
                        _notes.append(GedcomNote(data_lines))

                    elif tag == 'HEAD':
                        _header = GedcomHeader(data_lines)

                    elif tag == 'TRLR':
                        _trailer = GedcomTrailer(data_lines)

                except:
                    # skip invalid top level tags
                    pass

                i += 1

        # sort individuals and family by key
        self._individual_keys = sorted(self._individual_dict.keys())
        self._family_keys = sorted(self._family_dict.keys())
        # end of parse_and_validate_lines

    def print_parse_report(self) -> None:
        ''' print parsed line data and validation status '''

        for l in self.lines:
            print(f'--> {l.data}')
            print(
                f'<-- {l.level}|{l.tag}|{l.status}|{" ".join(l.arguments)}')

    def validate(self, validator: Validator) -> 'GedcomRepository':
        ''' run validator on GEDCOM data '''
        try:
            errors: List[str] = validator(self)
        except Exception as e:
            # catch and print validator internal erros
            print(e)
        else:
            # print each error
            for error in errors:
                print(error)

        # return self for piping
        return self

    def showcase(self, display: Callable[['GedcomRepository'], None]) -> 'GedcomRepository':
        ''' display specified GEDCOM data '''
        try:
            result: bool = display(self)
        except Exception as e:
            # catch unexpected error
            pass

        # return self for piping
        return self


def read_repository_file(path: str) -> GedcomRepository:
    ''' creat GEDCOM repository from input file '''

    line_generator: Iterator[GedcomLine] = get_lines_from_path(path)
    lines: List[GedcomLine] = list(line_generator)
    return GedcomRepository(lines)


def prompt_repository_file(
    prompt_message: str = 'Enter GEDCOM file (i.g. "test.ged" or "./test.ged"): ',
    default_file_path: str = 'test.ged'
) -> GedcomRepository:
    ''' prompt for input file to creat GEDCOM repository '''

    path: str = prompt_input_file(prompt_message, default_file_path)
    return read_repository_file(path)
