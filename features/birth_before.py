from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def birth_before_marriage(repo: GedcomRepository) -> List[str]:
  ''' US02: Birth should occur before marriage of an individual '''
  invalid_marriage: List[Tuple[str]] = []

  errors: List[str] = []

  for family in repo.families:
    marriage_date: Date = family.marriage

    if not marriage_date:
      continue

    for husband in family.husbands:
      if husband.birth and marriage_date < husband.birth:
        errors.append(
            f'ERROR US02 at line {husband.sex_line_no}: Husband ({husband.id}) in family({family.id}) married before being born')

    for wife in family.wifes:
      if wife.birth and marriage_date < wife.birth:
        errors.append(
            f'ERROR US02 at line {wife.sex_line_no}: Wife ({wife.id}) in family({family.id}) married before being born')

  return errors


def birth_before_death(repo: GedcomRepository) -> List[str]:
  ''' US03: Birth should occur before death of an individual '''
  invalid_death: List[Tuple[str]] = []

  for individual in repo.individuals:
      birthday: Date = individual.birth
      death_date: Date = individual.death

  # check individual is born before they die
      if death_date and birthday and death_date < birthday:
          invalid_death.append((individual, 'Individual'))

  errors: List[str] = []
  for individual, role in invalid_death:
    errors.append(
        f'ERROR US03 at line {individual.death_line_no}: Individual ({individual.id}) died before being born')

  return errors
