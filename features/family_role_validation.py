from typing import List, Tuple
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
