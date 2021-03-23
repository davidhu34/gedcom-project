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


def id_list_display(id_list: Optional[List[str]] = []) -> str:
    ''' get ID list display '''
    if not id_list:
        # return NA if list is empty or invalid
        return NA

    # join by comma
    # ID's are in quotes
    content: str = ", ".join([f"'{id}'" for id in id_list])
    # wrapped by brackets
    return f'{{{content}}}'


def individuals_display(individuals: Optional[List[GedcomIndividual]] = []) -> str:
    ''' get individual list display '''
    # filter out non-existant individuals
    id_list: List[str] = [f"'{individual.id}'" for individual in individuals if individual]

    return id_list_display(id_list)


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

        spouse_id_list: List[str] = [
            family.wife_id if is_male else family.husband_id for family in individual.spouse_of_list if family]

        children_id_list: List[str] = [
            child_id for family in individual.spouse_of_list if family for child_id in family.children_id_list]

        individual_table.add_row([
            individual.id,
            individual.name,
            individual.sex,
            f'{individual.birth}',
            f'{individual.age}',
            alive,
            optional_string_display(death_date),
            id_list_display(children_id_list),
            id_list_display(spouse_id_list),
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
            id_list_display(family.children_id_list),
        ])

    print(title)
    print(family_table)
