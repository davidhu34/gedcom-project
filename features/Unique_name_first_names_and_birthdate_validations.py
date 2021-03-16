from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository

''' US23'''
'''error = 'som thing'''
def unique_name_birth(repo: GedcomRepository) -> List[str]:
    invalid_individuals_name_birth: List[Tuple[str]] = []
    for individuals in repo.individuals:
        individual_id: str = individual_name
        birthdate = individual.birth
    if individual_id and not repo.Individuals[individual_id].is_name:
        invalid_individuals_name_birth.append((individual.id,'Name'))
    if birthdate and not repo.individuals[birthdate].is_birth:
        invalid_individuals_name_birth.append((birthdate,'Birth'))

    errors: List[str] = []
    for family_id, individual_id, role in invalid_individuals_name_birth:
        invalid_name_birth_line: int = repo.individual[individual_id].name_birth_line
        errors.append(
            f'ERROR US23 at line {invalid_name_birth_line}: individual{individual_id}) has incorrect name and birth for {role}({individual_id})')

    return errors


'''US25'''
def unique_first_names_in_families(repo: GedcomRepository) -> List[str]:
    invalid_first_names_in_families: List[Tuple[str]] = []
    for first_names in repo.families:


