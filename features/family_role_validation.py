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

  return [
      f'ERROR US21: Family({family_id}) has incorrect gender for {role}({individual_id})'
      for family_id, individual_id, role
      in invalid_family_roles
  ]


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

  return [
      f'ANOMALY US24: Families({", ".join(family_id_list)}) are not unique by spouse names and marriage date: {"|".join(combo)}'
      for combo, family_id_list in families_by_spouse_combo.items()
      if len(family_id_list) > 1
  ]
