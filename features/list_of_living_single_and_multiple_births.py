from typing import List, Tuple, DefaultDict
from collections import defaultdict
from gedcom import GedcomRepository
from datetime import datetime, date as Date
from gedcom.tags import GedcomIndividual


def living_single_list(repo):
    '''US31 : List all living single individuals'''
    living_single = []

    for individual in repo.individuals:

        if not individual.death and individual.age and individual.age > 30 and not individual.spouse_of_list:

            living_single.append(individual)

    return 'living single', living_single


def list_multiple_births(repo: GedcomRepository):
    '''US32: List of multiple births'''
    
    multiple_birth_children = []

    for family in repo.families:
        children: List[GedcomIndividual] = family.children
        birth_day_dict: DefaultDict[str,
            List[GedcomIndividual]] = defaultdict(list)

        for child in children:
            if not child.birth:
                continue
            birth_day_key: str = f'{child.birth}'
            birth_day_dict[birth_day_key].append(child)

        for key, same_birth_children in birth_day_dict.items():
            if len(same_birth_children) > 1:
                    for child in same_birth_children:
                        multiple_birth_children.append(child)

    return  'List multiple birth in families', multiple_birth_children
