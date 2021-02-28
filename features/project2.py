from gedcom import GedcomRepository, prompt_repository_file


def validate_gedcom_file() -> None:
    ''' project 2 print parsed file and line validations'''
    repo: GedcomRepository = prompt_repository_file()
    repo.print_parse_report()
