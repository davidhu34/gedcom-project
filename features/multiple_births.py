from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def siblings_born_at_same_time(repo: GedcomRepository) -> List[str]:
  ''' US14: No more than five siblings should be born at the same time '''
  errors: List[str] = []

  for family in repo.families:
    
    children = family.children  # list of indis
    for child in children:
        born_at_same_time=1
        for child2 in children:
            if child is child2:
              continue
            if child.birth ==child2.birth:
                born_at_same_time+=1
            if born_at_same_time>5:
                errors.append(
                f'ERROR US14 at line {child.birth_line_no}: too many siblings born at once in family({family.id})')
                return
  return errors


def too_many_siblings(repo: GedcomRepository) -> List[str]:
    ''' US15: There should be fewer than 15 siblings in a family '''
    errors: List[str] = []
 
    for family in repo.families:
        child_count =0
        children = family.children  # list of indis
        for child in children:
            child_count+=1
        if child_count>14:
            errors.append(f'ERROR US14 at line {child.birth_line_no}: too many siblings in family: ({family.id})')

    return errors