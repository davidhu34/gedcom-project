from typing import List, Tuple
from collections import defaultdict
from gedcom import GedcomRepository
from gedcom.pretty_table import pretty_print_individuals


def deceased_individual_list (repo):
    '''US29'''
    deceased_individuals = []

    for individual in repo.individuals:

        if individual.death :
            deceased_individuals.append(individual)
            
   
    return 'deceased_individuals' deceased_individuals


def living_married_list (repo):
    living_married = []
    '''US30'''
    for family in repo.families:

        if family.marriage and not family.divorce:

            if family.husband and not family.husband.death:
                living_married.append(husband)

            if family.wife and not family.wife.death:
                living_married.append(wife)

    return 'living married', living_married

            
       

    


            
        
