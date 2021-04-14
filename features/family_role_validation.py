from typing import List, Tuple, DefaultDict
from collections import defaultdict
from gedcom import GedcomRepository


def correct_gender_roles(repo: GedcomRepository) -> List[str]:
  ''' US21: correct gender for family roles '''
  invalid_family_roles: List[Tuple[str]] = []

  errors: List[str] = []

  for family in repo.families:

    for husband in family.husbands:
      # check husband is male
      if husband and not husband.is_male:
        errors.append(
            f'ERROR US21: Family({family.id}) has incorrect gender (at line {husband.sex_line_no}) for Husband({husband.id}) at line {family.husband_line_no}')

    for wife in family.wifes:
      # check wife is female
      if wife and not wife.is_female:
        errors.append(
            f'ERROR US21: Family({family.id}) has incorrect gender (at line {wife.sex_line_no}) for Wife({wife.id}) at line {family.wife_line_no}')

  return errors


def unique_family_spouses(repo: GedcomRepository) -> List[str]:
  ''' US24: Unique families by spouse '''
  families_by_spouse_combo: DefaultDict[Tuple[str], List[str]] = defaultdict(list)

  for family in repo.families:
    # ignore families with incomplete info
    if not family.husbands or not family.wifes or not family.marriage:
      continue

    for husband in family.husbands:
      for wife in family.wifes:
        husband_name: str = husband.name
        wife_name: str = wife.name
        marriage_str: str = f'{family.marriage}'

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
