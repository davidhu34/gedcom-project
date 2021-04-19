from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository
from gedcom.pretty_table import pretty_print_individuals


def age_and_age_at_death(repo):
    '''US07'''
    errors = []
    individuals_by_combination: Dict[Tuple[str],
                                     List[GedcomIndividual]] = defaultdict(list)
    for individual in repo.individuals:
        individual_age = individual.age

        if individual_age and individual_age >= 150:
            errors.append(
                f'ERROR US07: Individual({individual.id}) is older than 150 years old ({individual.age}) (at line {individual.birth_line_no})')

    return errors


def order_siblings_by_age(repo):
    '''US28'''
    for family in repo.families:
        siblings = family.children
        if siblings:
            sorted_siblings = sorted(siblings, key=lambda sibling: sibling.age * -1 if sibling.age else 0)
            pretty_print_individuals(
                f'Family({family.id} at line {family.line_no}) siblings ordered by age:', sorted_siblings)
