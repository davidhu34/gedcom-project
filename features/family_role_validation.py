from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def correct_gender_roles(repo: GedcomRepository) -> List[str]:
  ''' US21: correct gender for family roles '''
  invalid_family_roles: List[Tuple[str]] = []

  for family in repo.families:
    husband_id: str = family.husband
    wife_id: str = family.wife

    # check husband is male
    if husband_id and not repo.individual[husband_id].is_male:
      invalid_family_roles.append((family.id, husband_id, 'Husband'))

    # check wife is female
    if wife_id and not repo.individual[wife_id].is_female:
      invalid_family_roles.append((family.id, wife_id, 'Wife'))

  errors: List[str] = []
  for family_id, individual_id, role in invalid_family_roles:
    invalid_sex_line_no: int = repo.individual[individual_id].sex_line_no
    errors.append(
        f'ERROR US21 at line {invalid_sex_line_no}: Family({family_id}) has incorrect gender for {role}({individual_id})')

  return errors


def unique_family_spouses(repo: GedcomRepository) -> List[str]:
  ''' US24: Unique families by spouse '''
  families_by_spouse_combo: Dict[Tuple[str], List[str]] = defaultdict(list)

  for family in repo.families:
    husband_id: str = family.husband
    wife_id: str = family.wife
    marriage_date: Date = family.marriage

    husband_name: str = repo.individual[husband_id].name
    wife_name: str = repo.individual[wife_id].name
    marriage_str: str = f'{marriage_date}'

    # unique by spouse names and marriage date
    key: Tuple[str] = (husband_name, wife_name, marriage_str)

    families_by_spouse_combo[key].append(family.id)

  errors: List[str] = []
  for combo, family_id_list in families_by_spouse_combo.items():
    if len(family_id_list) > 1:
      family_line_info: List[str] = [
          f'{family_id} at line {repo.family[family_id].line_no}'
          for family_id in family_id_list
      ]
      errors.append(
          f'ANOMALY US24: Families({", ".join(family_line_info)}) are not unique by spouse names and marriage date: {"|".join(combo)}')

  return errors
