
from typing import Any, List
from datetime import date as Date
from prettytable import PrettyTable
from gedcom import GedcomRepository, prompt_repository_file

NA: str = 'NA'


def optional_string_display(data: Any) -> str:
    ''' return string display of data '''
    if not data:
        # return NA if data is invalid
        return NA

    return f'{data}'


def id_list_display(id_list: List[str]) -> str:
    ''' get ID list display '''
    if not id_list:
        # return NA if list is empty or invalid
        return NA

    # ID's are in quotes
    # join by comma
    content: str = ", ".join([f"'{id}'" for id in id_list])
    # wrapped by brackets
    return f'{{{content}}}'


def print_gedcom_info(repository: GedcomRepository) -> None:
    ''' project 3 pretty tables '''
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
    for individual in repository.individuals:

        death_date: Date = individual.death
        alive: bool = not death_date

        is_male: bool = individual.sex == 'Y'
        spouse_of_families: List[str] = [repository.family[family_id]
                                         for family_id in individual.spouse_of_list]
        spouses: List[str] = [
            family.wife if is_male else family.husband for family in spouse_of_families]
        children: List[str] = [
            child for family in spouse_of_families for child in family.children]

        individual_table.add_row([
            individual.id,
            individual.name,
            individual.sex,
            f'{individual.birth}',
            f'{individual.age}',
            alive,
            optional_string_display(death_date),
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

    for family in repository.families:

        husband_id: str = family.husband
        husband_name: str = repository.individual[husband_id].name
        wife_id: str = family.wife
        wife_name: str = repository.individual[wife_id].name

        children

        family_table.add_row([
            family.id,
            f'{family.marriage}',
            optional_string_display(family.divorce),
            husband_id,
            husband_name,
            wife_id,
            wife_name,
            id_list_display(family.children),
        ])

    print('Families')
    print(family_table)
