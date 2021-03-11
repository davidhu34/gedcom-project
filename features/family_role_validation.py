from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository
from gedcom.exceptions import GedcomValidationException


def correct_gender_roles(repo: GedcomRepository) -> bool:
  ''' US21: correct gender for family roles '''
  invalid_family_roles: List[Tuple[str]] = []

  for family in repo.families:
    husband_id: str = family.husband
    wife_id: str = family.wife

    # check husband is male
    if husband_id and not repo.individual[husband_id].is_male:
      invalid_family_roles.append((family.id, husband_id))

    # check wife is female
    if wife_id and not repo.individual[wife_id].is_female:
      invalid_family_roles.append((family.id, wife_id))

  if invalid_family_roles:
    # raise error if any
    message: str = "Invalid gender roles (Family -> Individual):"
    for family_id, individual_id in invalid_family_roles:
      message += f'\n{family_id} -> {individual_id}'

    raise GedcomValidationException(message)

  return True


def unique_family_spouses(repo: GedcomRepository) -> bool:
  ''' US21: Unique families by spouse '''
  families_by_spouse_combo: Dict[Tuple[str], List[str]] = defaultdict(list)

  for family in repo.families:
    husband_id: str = family.husband
    wife_id: str = family.wife
    marriage_date: Date = family.marriage

    husband_name: str = repo.individual[husband_id].name
    wife_name: str = repo.individual[husband_id].name
    marriage_str: str = f'{marriage_date}'

    # unique by spouse names and marriage date
    key: Tuple[str] = (husband_name, wife_name, marriage_str)

    families_by_spouse_combo[key].append(family.id)

  duplicate_spouse_info: str = ''
  for combo, family_id_list in families_by_spouse_combo.items():
    # find husband name-wife name-marriage combo with multiple families
    if len(family_id_list) > 1:
      duplicate_spouse_info += f'\n{combo}: {family_id_list}'

  if duplicate_spouse_info:
    # raise if there are duplicates
    raise GedcomValidationException(
        f'Some family spouses are not unique:{duplicate_spouse_info}')

  return True
