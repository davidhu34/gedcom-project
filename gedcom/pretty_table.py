from typing import Any, List, Optional
from datetime import date as Date
from prettytable import PrettyTable
from .tags import GedcomIndividual, GedcomFamily


NA: str = 'NA'


def optional_string_display(data: Any) -> str:
    ''' return string display of data '''
    if not data:
        # return NA if data is invalid
        return NA

    return f'{data}'


def individuals_display(individuals: Optional[List[GedcomIndividual]] = []) -> str:
    ''' get individual list display '''
    # filter out non-existant individuals
    # ID's are in quotes
    id_list: List[str] = [f"'{individual.id}'" for individual in individuals if individual]

    if not id_list:
        # return NA if list is empty or invalid
        return NA

    # join by comma
    content: str = ", ".join(id_list)
    # wrapped by brackets
    return f'{{{content}}}'


def pretty_print_individuals(title: str, individuals: List[GedcomIndividual]) -> None:
    ''' print individuals' data with PrettyTable '''
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
    individual_table: PrettyTable = PrettyTable(
        field_names=individual_fields)

    # add rows from university students
    for individual in individuals:
        death_date: Date = individual.death

        alive: bool = not death_date
        is_male: bool = individual.sex == 'M'

        spouses: List[GedcomIndividual] = [
            family.wife if is_male else family.husband for family in individual.spouse_of_list if family]

        children: List[GedcomIndividual] = [
            child for family in individual.spouse_of_list if family for child in family.children]

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

    print(title)
    print(individual_table)


def pretty_print_families(title: str, families: List[GedcomFamily]) -> None:
    ''' print families' data with PrettyTable '''
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

    for family in families:

        husband: GedcomIndividual = family.husband
        wife: GedcomIndividual = family.wife

        family_table.add_row([
            family.id,
            f'{family.marriage}',
            optional_string_display(family.divorce),
            family.husband_id,
            husband.name if husband else NA,
            family.wife_id,
            wife.name if wife else NA,
            individuals_display(family.children),
        ])

    print(title)
    print(family_table)
