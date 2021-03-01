
from typing import List
from datetime import date as Date
from prettytable import PrettyTable
from gedcom import GedcomRepository, prompt_repository_file


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
        'Husband ID',
        'Husband Name',
        'Wife ID',
        'Wife Name',
    ]
    family_table: PrettyTable = PrettyTable(field_names=family_fields)

    # families sorted by ID are available in GedcomRepository property
    for family in repo.families:

        husband_name: str = repo.individual[family.husband].name
        wife_name: str = repo.individual[family.wife].name

        family_table.add_row([
            family.id,
            family.husband,
            repo.individual[family.husband].name,
            family.wife,
            repo.individual[family.wife].name,
        ])

    print('Families')
    print(family_table)
