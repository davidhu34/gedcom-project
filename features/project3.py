
from typing import Any, List, Optional
from datetime import date as Date
from prettytable import PrettyTable
from gedcom import GedcomRepository, prompt_repository_file
from gedcom.tags import GedcomIndividual

NA: str = 'NA'


def optional_string_display(data: Any) -> str:
    ''' return string display of data '''
    if not data:
        # return NA if data is invalid
        return NA

    return f'{data}'


def individuals_display(individuals: Optional[List[GedcomIndividual]]) -> str:
    ''' get individual list display '''
    if not individuals:
        # return NA if list is empty or invalid
        return NA

    # ID's are in quotes
    # join by comma
    content: str = ", ".join(
        [f"'{individual.id}'" for individual in individuals])
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

        is_male: bool = individual.sex == 'M'

        spouses: List[GedcomIndividual] = [
            family.wife if is_male else family.husband for family in individual.spouse_of_list]
        children: List[GedcomIndividual] = [
            child for family in individual.spouse_of_list for child in family.children]

        individual_table.add_row([
            individual.id,
            individual.name,
            individual.sex,
            f'{individual.birth}',
            f'{individual.age}',
            alive,
            optional_string_display(death_date),
            individuals_display(children),
            individuals_display(spouses),
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

        husband: GedcomIndividual = family.husband
        wife: GedcomIndividual = family.wife

        family_table.add_row([
            family.id,
            f'{family.marriage}',
            optional_string_display(family.divorce),
            husband.id,
            husband.name,
            wife.id,
            wife.name,
            individuals_display(family.children),
        ])

    print('Families')
    print(family_table)
