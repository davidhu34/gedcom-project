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

    if family.husband and marriage_date<family.husband.birth:
      errors.append(
          f'ERROR US02 at line {family.husband.sex_line_no}: Husband ({family.husband.id}) in family({family.id}) married before being born')

    if family.wife and marriage_date<family.wife.birth:
      errors.append(
          f'ERROR US02 at line {family.wife.sex_line_no}: Wife ({family.wife.id}) in family({family.id}) married before being born')

  return errors


def birth_before_death(repo: GedcomRepository) -> List[str]:
  ''' US03: Birth should occur before death of an individual '''
  invalid_death: List[Tuple[str]] = []
  

  for individual in repo.individuals:
      birthday: Date = individual.birth
      death_date: Date = individual.death
      
  
  # check individual is born before they die
      if death_date and birthday and death_date< birthday: 
          invalid_death.append(( individual, 'Individual'))

  errors: List[str] = []
  for individual, role in invalid_death:
    errors.append(
        f'ERROR US03 at line {individual.death_line_no}: Individual ({individual.id}) died before being born')

  return errors