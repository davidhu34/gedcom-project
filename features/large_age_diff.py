from typing import List
from gedcom import GedcomRepository


def large_age_diff(repo: GedcomRepository) -> List[str]:
  errors: List[str] = []

  for family in repo.families:
    marriage_date = family.marriage

    if not marriage_date:
      continue

    for husband in family.husbands:
      for wife in family.wifes:
        spouse_older, spouse_younger = (husband, wife) if husband.birth < wife.birth else (wife, husband)
        older_age: int = spouse_older.age_at(marriage_date)
        younger_age: int = spouse_younger.age_at(marriage_date)
        if older_age and younger_age and older_age / 2 > younger_age:
          errors.append(
              f'ANOMALY US34: Family({family.id} at line {family.line_no}) spouse({spouse_older.id}) is more than twice as old as spouse({spouse_younger.id})')

  return errors
