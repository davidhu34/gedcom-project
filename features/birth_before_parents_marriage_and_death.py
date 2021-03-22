from datetime import date as Date
from gedcom import GedcomRepository

def birth_before_parents_marriage(repo: GedcomRepository):
    """ US08 Individual birth date should occur after parents marriage date """
    errors = []
    for family in repo.families:
        marriage_date = family.marriage

        if len(family.children) == 0:
            continue
        
        for child in family.children:
            if not marriage_date or child.birth < marriage_date:
                errors.append(
                    f"ANOMALY US08: Birth date (at line {child.birth_line_no}) for Individual({child.id}) in Family({family.id}) occurs before parent's marriage date (at line {family.marriage_line_no}).")
    
    return errors

def birth_before_parents_death(repo: GedcomRepository):
    """ US09 Individual birth date should occur before parents death date """
    errors = []
    for family in repo.families:
        father = family.husband
        mother = family.wife

        if len(family.children) == 0:
            continue

        for child in family.children:
            if father.death and father.death < child.birth:
                errors.append(
                    f"ERROR US09: Birth date (at line {child.birth_line_no}) for Individual({child.id}) in Family({family.id}) occurs after Father's({father.id}) death date (at line {father.death_line_no}).")
            
            if mother.death and mother.death < child.birth:
                errors.append(
                    f"ERROR US09: Birth date (at line {child.birth_line_no}) for Individual({child.id}) in Family({family.id}) occurs after Mother's({mother.id}) death date (at line {mother.death_line_no}).")
    
    return errors
            

            

