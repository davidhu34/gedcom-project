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

    for husband in family.husbands:
      if husband.death and marriage_date > husband.death:
        errors.append(
            f'ERROR US05 at line {husband.sex_line_no}: Husband ({husband.id}) in family({family.id}) died before marriage')

    for wife in family.wifes:
      if wife.death and marriage_date > wife.death:
        errors.append(
            f'ERROR US05 at line {wife.sex_line_no}: Wife ({wife.id}) in family({family.id}) died before marriage')

  return errors


def marriage_before_divorce(repo: GedcomRepository) -> List[str]:
  ''' US04: Marriage should always occur before divorce'''
  invalid_marriage: List[Tuple[str]] = []

  errors: List[str] = []

  for family in repo.families:
    marriage_date: Date = family.marriage
    divorce_date: Date = family.divorce

    if marriage_date and divorce_date and marriage_date > divorce_date:

      for husband in family.husbands:
        errors.append(
            f'ERROR US04 at line {husband.sex_line_no}: Husband ({husband.id}) in family({family.id}) divorced before marriage')

      for wife in family.wifes:
        errors.append(
            f'ERROR US04 at line {wife.sex_line_no}: Wife ({wife.id}) in family({family.id}) divorced before marriage')

  return errors
