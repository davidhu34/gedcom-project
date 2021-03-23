from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository

def age_and_age_at_death(repo):
    '''US07'''
    errors = []
    individuals_by_combination: Dict[Tuple[str],
                                   List[GedcomIndividual]] = defaultdict(list)
    for individual in repo.individuals:
    age = individual.age
    age_at_death = individual.death
    for individual_age and individual_age_at_death in [age, age_at_death]
    if  individual_age >= 150  and individual_age_at_death >= 150:
        errors.append(
                f'ERROR US07: Individuals({individual.age} at line { Age.line_no}) have incorrect age (at line {Age.line_no}
                f'ERROR US07: Individuals({individual.death} at line{ age.line_no}) have incorrect age (at line {Age.line_no})

    return errors
    