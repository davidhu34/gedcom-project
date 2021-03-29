from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def marriage_before_death(repo: GedcomRepository) -> List[str]:
  ''' US05: Marriage should always occur before death'''
  invalid_marriage: List[Tuple[str]] = []

  errors: List[str] = []
  
  for family in repo.families:
    marriage_date: Date = family.marriage
  
    if not marriage_date:
      continue

    if family.husband and family.husband.death and marriage_date > family.husband.death:
      errors.append(
          f'ERROR US05 at line {family.husband.sex_line_no}: Husband ({family.husband.id}) in family({family.id}) died before marriage')

    if family.wife and family.wife.death and marriage_date > family.wife.death:
      errors.append(
          f'ERROR US05 at line {family.wife.sex_line_no}: Wife ({family.wife.id}) in family({family.id}) died before marriage')

  return errors


def marriage_before_divorce(repo: GedcomRepository) -> List[str]:
  ''' US04: Marriage should always occur before divorce'''
  invalid_marriage: List[Tuple[str]] = []

  errors: List[str] = []
  
  for family in repo.families:
    marriage_date: Date = family.marriage
    divorce_date: Date = family.divorce
    if not marriage_date or not divorce_date:
      continue

    if family.husband and marriage_date > divorce_date:
      errors.append(
          f'ERROR US04 at line {family.husband.sex_line_no}: Husband ({family.husband.id}) in family({family.id}) divorced before marriage')

    if family.wife and marriage_date > divorce_date:
      errors.append(
          f'ERROR US04 at line {family.wife.sex_line_no}: Wife ({family.wife.id}) in family({family.id}) divorced before marriage')

  return errors