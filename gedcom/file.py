from typing import IO, Iterator
from .exceptions import GedcomLineParsingException, GedcomFileNotFound


class GedcomLine:
    ''' parsed GEDCOM file line '''
    __slots__ = 'line_no', 'data', 'level', 'tag', 'arguments', 'validated'

    def __init__(self, line: str, line_no: int) -> None:
        try:
            level, *tokens = line.split()
            self.level: int = int(level)

            # handles special tag positions
            indi_or_fam: bool = level == '0' and tokens[-1] in ('INDI', 'FAM')
            tag, *arguments = [tokens[1], tokens[0]] if indi_or_fam else tokens

            self.line_no: int = line_no
            self.data: str = line
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

    @property
    def status(self) -> str:
        return "Y" if self.validated else "N"


def get_lines_from_file(file: IO) -> Iterator[GedcomLine]:
    ''' a generator yielding lines from file object '''
    with file:
        # loop through file line sequence
        line_no: int = 0
        for raw_line in file:
            # remove trailing new line
            line: str = raw_line.rstrip('\n')
            line_no += 1
            yield GedcomLine(line, line_no)


def get_lines_from_path(path: str) -> Iterator[GedcomLine]:
    ''' a generator yielding lines of file from path '''
    # read file from path
    try:
        file: IO = open(path)

    # handle file not found
    except FileNotFoundError:
        raise GedcomFileNotFound(f'Cannot open file "{path}"!', path)

    # yield lines form a generator function
    else:
        return get_lines_from_file(file)


def prompt_input_file(prompt_message: str, default_file_path: str = '') -> str:
    ''' prompt for non-empty file path input '''

    while True:
        # prompt input string
        input_file_path: str = input(prompt_message)

        # user input get
        if input_file_path:
            return input_file_path

        # default file path available
        elif default_file_path:
            return default_file_path
