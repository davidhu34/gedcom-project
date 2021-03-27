from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository

def age_and_age_at_death(repo):
    '''US07'''
    errors = []
    individuals_by_combination: Dict[Tuple[str],
                                   List[GedcomIndividual]] = defaultdict(list)
    for individual in repo.individuals:
        individual_age = individual.age
        
    
        if  individual_age >= 150 :
            errors.append(
                f'ERROR US07: Individuals({individual.id}) have incorrect age ({individual.age}) (at line {individual.birth_line_no})')



    return errors
    