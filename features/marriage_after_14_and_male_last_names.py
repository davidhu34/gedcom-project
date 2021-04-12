from datetime import date as Date
from prettytable import PrettyTable
from gedcom import GedcomRepository

def marriage_after_14(repo: GedcomRepository):
    """ US10 Marriage of individuals should occur after age 14 """
    errors = []
    for family in repo.families:
        marriage_date = family.marriage
        husband = family.husband
        wife = family.wife
        husband_14th = husband.birth.replace(year=husband.birth.year+14)
        wife_14th = wife.birth.replace(year=wife.birth.year+14)

        if not marriage_date:
            continue

        if husband.birth and (husband_14th > marriage_date):
            invalid_marr_date_line_no = family.marriage_line_no
            errors.append(
                f'ERROR US10: Individual({husband.id}) in Family({family.id}) married (at line {invalid_marr_date_line_no}) when under age 14.')
        
        if wife.birth and (wife_14th > marriage_date):
            invalid_marr_date_line_no = family.marriage_line_no
            errors.append(
                f'ERROR US10: Individual({wife.id}) in Family({family.id}) married (at line {invalid_marr_date_line_no}) when under age 14.')
    
    return errors

def male_last_names(repo: GedcomRepository):
    """ US16 List of all the male last names """
    male_last_names = []
    male_ln_dict = {}
    pt = PrettyTable()
    pt.field_names = ['ID', 'Last Name']
    for individual in repo.individuals:

        if individual.sex and individual.sex == 'M':
            if individual not in male_last_names:
                male_last_names.append(individual)
    
    for item in male_last_names:
        name_list = item.name.split()
        last_name = name_list[1]
        if last_name in male_ln_dict:
            male_ln_dict[last_name] = male_ln_dict[last_name] + ',' + item.id

        else:
            male_ln_dict[last_name] = item.id

    for key, value in male_ln_dict.items():
        pt.add_row([value, key])
    

    print('Male Last Names', pt)

    return 'Male Last Names', male_last_names

    



