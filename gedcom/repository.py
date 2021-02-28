from typing import List, Iterator
from .tags import *
from .file import GedcomLine, prompt_input_file, get_lines_from_path


class GedcomRepository:
    ''' A Repository for GEDCOM file data '''

    def __init__(self, lines: List[GedcomLine]) -> None:
        ''' construct GedcomRepository '''
        self.parse_and_validate_lines(lines)

    def reset_containers(self) -> None:
        self.notes: List[GedcomNotes] = []
        self.individuals: List[GedcomIndividual] = []
        self.families: List[GedcomFamily] = []
        self.individual_dict: Dict[str, GedcomIndividual] = {}
        self.family_dict: Dict[str, GedcomFamily] = {}

    def parse_and_validate_lines(self, lines: List[GedcomLine]) -> None:
        ''' get data from lines and validate '''
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

        # end of parse_and_validate_lines

    def print_parse_report(self) -> None:
        ''' print parsed line data and validation status '''

        for l in self.lines:
            print(f'--> {l.data}')
            print(
                f'<-- {l.level}|{l.tag}|{l.status}|{" ".join(l.arguments)}')


def prompt_repository_file(
    prompt_message: str = 'Enter GEDCOM file (i.g. "test.ged" or "./test.ged"): ',
    default_file_path: str = 'test.ged'
) -> GedcomRepository:
    ''' prompt for input file to creat GEDCOM repository '''

    path: str = prompt_input_file(prompt_message, default_file_path)
    line_generator: Iterator[GedcomLine] = get_lines_from_path(path)
    lines: List[GedcomLine] = list(line_generator)
    return GedcomRepository(lines)
