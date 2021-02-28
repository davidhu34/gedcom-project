
from typing import List
from gedcom import GedcomRepository, prompt_repository_file
from prettytable import PrettyTable
from datetime import date as Date


def id_list_display(id_list: List[str]) -> str:
    content: str = ", ".join([f"'{id}'" for id in id_list])
    return f'{{{content}}}'


def print_gedcom_info() -> None:
    ''' project 3 modifications from project 2 '''
    repo: GedcomRepository = prompt_repository_file()

    individual_fields: List[str] = [
        'ID',
        'Name',
    ]
    individual_table: PrettyTable = PrettyTable(field_names=individual_fields)

    # individuals sorted by ID are available in GedcomRepository property
    for individual in repo.individuals:
        individual_table.add_row([
            individual.id,
            individual.name,
        ])

    print('Individuals')
    print(individual_table)

    family_fields: List[str] = [
        'ID',
        'Husband Name',
        'Wife Name',
    ]
    family_table: PrettyTable = PrettyTable(field_names=family_fields)

    # families sorted by ID are available in GedcomRepository property
    for family in repo.families:

        husband_name: str = repo.individual[family.husband].name
        wife_name: str = repo.individual[family.wife].name

        family_table.add_row([
            family.id,
            repo.individual[family.husband].name,
            repo.individual[family.wife].name,
        ])

    print('Families')
    print(family_table)
