from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def siblings_born_at_same_time(repo: GedcomRepository) -> List[str]:
    ''' US14: No more than five siblings should be born at the same time '''
    errors: List[str] = []
    for family in repo.families:
        children=  family.children
        birth_day_dict= defaultdict(list)
        for child in children:
            birth_day_key: str = f'{child.birth}'
            birth_day_dict[birth_day_key].append(child)
        for key, same_birth_children in birth_day_dict.items():
            if len(same_birth_children) > 5:
                errors.append(
                f'ERROR US14 at line {child.birth_line_no}: too many siblings born at once({key}) in family({family.id})')
    return errors


def too_many_siblings(repo: GedcomRepository) -> List[str]:
    ''' US15: There should be fewer than 15 siblings in a family '''
    errors: List[str] = []

    for family in repo.families:
        child_count = 0
        children = family.children  # list of indis
        if len(children) > 14:
            errors.append(
                f'ERROR US15 at line {family.line_no}: too many siblings in family: ({family.id})')

    return errors
