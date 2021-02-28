from gedcom import GedcomRepository, prompt_repository_file


def validate_gedcom_file() -> None:
    ''' main function for project 2 '''
    repo: GedcomRepository = prompt_repository_file()
    repo.print_parse_report()
