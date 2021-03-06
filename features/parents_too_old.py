from typing import List
from gedcom import GedcomRepository
from datetime import date as Date


def year_diff(date1, date2) -> int:
  d1, d2 = (date2, date1) if date1 > date2 else (date1, date2)
  ''' d2 should be larger/later than d1 '''
  d2_mark: Date = Date(d2.year, d1.month, d1.day)

  return d2.year - d1.year - \
      (1 if d2 < d2_mark else 0)


def month_diff(date1, date2) -> int:
  d1, d2 = (date2, date1) if date1 > date2 else (date1, date2)

  years_apart: int = year_diff(d1, d2)
  return years_apart * 12 + d2.month - d1.month


def parents_too_old(repo: GedcomRepository) -> List[str]:
  ''' US12: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children'''
  errors: List[str] = []

  for family in repo.families:
    for child in family.children:

      if not child.birth:
        continue

      for wife in family.wifes:
        if wife.birth and year_diff(wife.birth, child.birth) >= 60:
            errors.append(
                f'ERROR US12: Child({child.id}) is at least 60 years younger than their mother (at line {child.birth_line_no})')

      for husband in family.husbands:
        if husband.birth and year_diff(husband.birth, child.birth) >= 80:
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
            if child is child2 or not child.birth or not child2.birth:
              continue

            else:
              month_d = month_diff(child.birth, child2.birth)
              are_twins = abs((child2.birth - child.birth).days) < 2
              if month_d <= 8 and not are_twins:
                errors.append(
                    f'ERROR US13: Child({child.id}) was born too close in time to another sibling({child2.id}). (at line {child.birth_line_no})')
  return errors
