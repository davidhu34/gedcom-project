from gedcom import GedcomRepository


def deceased_individual_list(repo):
    '''US29: List all deceased individuals'''
    deceased_individuals = []

    for individual in repo.individuals:

        if individual.death:
            deceased_individuals.append(individual)

    return 'deceased individuals', deceased_individuals


def living_married_list(repo):
    '''US30 : List all living married individuals'''
    living_married = []
    for family in repo.families:

        if family.marriage and not family.divorce:

            for husband in family.husbands:

                if not husband.death:
                    living_married.append(family.husband)

            for wife in family.wifes:
                if not wife.death:
                    living_married.append(family.wife)

    return 'living married', living_married
