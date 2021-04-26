from gedcom import GedcomRepository
from datetime import timedelta, date as Date

def list_recent_births(repo: GedcomRepository):
    """US35 List all people in a GEDCOM file who were born in the last 30 days """
    recent_births = []
    present = Date.today()
    thirty_days = present - timedelta(days=30)
    

    for individual in repo.individuals:

        if individual.birth and (individual.birth <= present and individual.birth >= thirty_days):
            recent_births.append(individual)
    
    return 'Recent Births', recent_births

def list_recent_deaths(repo: GedcomRepository):
    """ US36 List all people in a GEDCOM file who died in the last 30 days """
    recent_deaths = []
    present = Date.today()
    thirty_days = present - timedelta(days=30)

    for individual in repo.individuals:

        if individual.death and (individual.death <= present and individual.death >= thirty_days):
            recent_deaths.append(individual)
    
    return 'Recent Deaths', recent_deaths
