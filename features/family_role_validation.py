from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def correct_gender_roles(repo: GedcomRepository) -> List[str]:
  ''' US21: correct gender for family roles '''
  invalid_family_roles: List[Tuple[str]] = []

  errors: List[str] = []

  for family in repo.families:

    # check husband is male
    if family.husband and not family.husband.is_male:
      errors.append(
          f'ERROR US21 at line {family.husband.sex_line_no}: Family({family.id}) has incorrect gender for Husband({family.husband.id})')

    # check wife is female
    if family.wife and not family.wife.is_female:
      errors.append(
          f'ERROR US21 at line {family.wife.sex_line_no}: Family({family.id}) has incorrect gender for Wife({family.wife.id})')

  return errors


def unique_family_spouses(repo: GedcomRepository) -> List[str]:
  ''' US24: Unique families by spouse '''
  families_by_spouse_combo: Dict[Tuple[str], List[str]] = defaultdict(list)

  for family in repo.families:
    marriage_date: Date = family.marriage

    husband_name: str = family.husband.name
    wife_name: str = family.wife.name
    marriage_str: str = f'{marriage_date}'

    # unique by spouse names and marriage date
    key: Tuple[str] = (husband_name, wife_name, marriage_str)

    families_by_spouse_combo[key].append(family)

  errors: List[str] = []
  for combo, families in families_by_spouse_combo.items():
    if len(families) > 1:
      family_line_info: List[str] = [
          f'{family.id} at line {family.line_no}'
          for family in families
      ]
      errors.append(
          f'ANOMALY US24: Families({", ".join(family_line_info)}) are not unique by spouse names and marriage date: {"|".join(combo)}')

  return errors
