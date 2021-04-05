
from typing import Tuple, Any
from gedcom import GedcomRepository


def all_gedcom_individuals(repo: GedcomRepository) -> Tuple[Any]:
    ''' print all individuals '''
    return 'Individuals', repo.individuals

def all_gedcom_families(repo: GedcomRepository) -> Tuple[Any]:
    ''' print all families '''
    return 'Families', repo.families