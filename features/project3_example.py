
from typing import List
from gedcom import GedcomRepository, prompt_repository_file
from prettytable import PrettyTable
from datetime import date as Date


def id_list_display(id_list: List[str]) -> str:
    ''' get ID list display '''

    if not id_list:
        # return NA if
        return 'NA'

    # ID's are in quotes
    # join by comma
    content: str = ", ".join([f"'{id}'" for id in id_list])
    # wrapped by brackets
    return f'{{{content}}}'


def print_gedcom_info() -> None:
    ''' project 3 example pretty tables '''
    repo: GedcomRepository = prompt_repository_file()

    individual_fields: List[str] = [
        'ID',
        'Name',
        'Gender',
        'Birthday',
        'Age',
        'Alive',
        'Death',
        'Child',
        'Spouse'
    ]
    individual_table: PrettyTable = PrettyTable(field_names=individual_fields)

    # add rows from university students
    for individual in repo.individuals:

        birth_date: Date = individual.birth
        today: Date = Date.today()
        this_birth_date: Date = Date(
            today.year, birth_date.month, birth_date.day)
        age: int = today.year - birth_date.year - \
            (1 if today < this_birth_date else 0)

        death_date: Date = individual.death
        alive: bool = not death_date

        is_male: bool = individual.sex == 'Y'
        spouse_of_families: List[str] = [repo.family[family_id]
                                         for family_id in individual.spouse_of_list]
        spouses: List[str] = [
            family.wife if is_male else family.husband for family in spouse_of_families]
        children: List[str] = [
            child for family in spouse_of_families for child in family.children]

        individual_table.add_row([
            individual.id,
            individual.name,
            individual.sex,
            f'{birth_date}',
            age,
            alive,
            f'{death_date}' if death_date else 'NA',
            id_list_display(children),
            id_list_display(spouses),
        ])

    print('Individuals')
    print(individual_table)

    family_fields: List[str] = [
        'ID',
        'Married',
        'Divorced',
        'Husband ID',
        'Husband Name',
        'Wife ID',
        'Wife Name',
        'Children',
    ]
    family_table: PrettyTable = PrettyTable(field_names=family_fields)

    for family in repo.families:

        husband_id: str = family.husband
        husband_name: str = repo.individual[husband_id].name
        wife_id: str = family.wife
        wife_name: str = repo.individual[wife_id].name

        children

        family_table.add_row([
            family.id,
            f'{family.marriage}',
            f'{family.divorce}' if family.divorce else 'NA',
            husband_id,
            husband_name,
            wife_id,
            wife_name,
            id_list_display(family.children),
        ])

    print('Families')
    print(family_table)
