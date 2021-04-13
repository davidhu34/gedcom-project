from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository
from datetime import datetime

def parents_too_old(repo: GedcomRepository) -> List[str]:
  ''' US12: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children'''
  errors: List[str] = []
  
  for family in repo.families:
    wife = family.wife  # an indi
    husband = family.husband  # an indi
    children = family.children  # list of indis
    
    for child in children:
        d1 = datetime.strptime(child, "%Y-%m-%d")
        d2 = datetime.strptime(wife, "%Y-%m-%d")
        d3 = datetime.strptime(husband, "%Y-%m-%d")
        if (abs(d2-d1).days)>21900:
            errors.append(
            f'ERROR US12: Child({child.id}) is at least 60 years younger than their mother (at line {child.birth_line_no})')
        if (abs(d3-d1).days)>29200:
            errors.append(
            f'ERROR US12: Child({child.id}) is at least 80 years younger than their father (at line {child.birth_line_no})')
    
  return errors

def sibling_spacing(repo: GedcomRepository) -> List[str]:
  ''' US13: Birth dates of siblings should be more than 8 months apart or less than 2 days apart
    (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)'''
  errors: List[str] = []
  
  for family in repo.families:
    children = family.children  # list of indis
    for child in children:
        for child2 in children:
            if child is child2:
              continue
            else:
              d1 = datetime.strptime(child, "%Y-%m-%d")
              d2 = datetime.strptime(child2, "%Y-%m-%d")

              if (((abs(d2-d1).days)< 240) and ((abs(d2-d1).days)> 2)):
                errors.append(f'ERROR US13: Child({child.id}) was born too close in time to another sibling. (at line {child.birth_line_no})')
  return errors

