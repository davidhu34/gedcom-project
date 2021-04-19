from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository


def unique_name_and_birth(repo):
  ''' US23: Unique name and birth date '''
  errors = []

  individuals_by_combination: Dict[Tuple[str],
                                   List[GedcomIndividual]] = defaultdict(list)

  for individual in repo.individuals:
    name = individual.name
    birth = individual.birth
    if name and birth:
      combination: Tuple[str] = (name, f'{birth}')
      individuals_by_combination[combination].append(individual)

  for combo, individuals in individuals_by_combination.items():
    if len(individuals) > 1:
      individual_line_info: List[str] = [
          f'{individual.id} at line {individual.line_no}'
          for individual in individuals
      ]
      errors.append(
          f'ANOMALY US23: Individuals({", ".join(individual_line_info)}) are not unique by names and birth date: {"|".join(combo)}')

  return errors


def unique_first_names_in_families(repo):
  ''' US25: Unique first names in families '''
  errors = []

  for family in repo.families:
    individuals_by_first_name: Dict[str,
                                    List[GedcomIndividual]] = defaultdict(list)

    for individual in [*family.children, *family.wifes, *family.husbands]:
      if not individual:
        continue
      individuals_by_first_name[individual.first_name].append(individual)

    for first_name, individuals in individuals_by_first_name.items():
      if len(individuals) > 1:
        name_line_info: List[str] = [
            f'{individual.id} at line {individual.name_line_no}'
            for individual in individuals
        ]
        errors.append(
            f'ANOMALY US25: Family({family.id} at line{family.line_no}) does not have unique first names ({", ".join(name_line_info)})')

  return errors
