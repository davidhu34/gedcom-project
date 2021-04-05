from datetime import date as Date
from gedcom import GedcomRepository

def marriage_after_14(repo: GedcomRepository):
    """ US10 Marriage of individuals should occur after age 14 """
    errors = []
    for family in repo.families:
        marriage_date = family.marriage
        husband = family.husband
        wife = family.wife
        husband_age = marriage_date - husband.birth
        wife_age = marriage_date - wife.birth

        if not marriage_date:
            continue

        # age 14 years is equivalent to 5110 days
        if husband.birth and (husband_age.days < 5110):
            invalid_marr_date_line_no = family.marriage_line_no
            errors.append(
                f'ERROR US10: Individual({husband.id}) in Family({family.id}) married (at line {invalid_marr_date_line_no}) when under age 14.')
        
        if wife.birth and (wife_age.days < 5110):
            invalid_marr_date_line_no = family.marriage_line_no
            errors.append(
                f'ERROR US10: Individual({wife.id}) in Family({family.id}) married (at line {invalid_marr_date_line_no}) when under age 14.')
    
    return errors



