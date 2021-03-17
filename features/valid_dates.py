from datetime import date as Date
from gedcom import GedcomRepository


def divorce_before_death(repo: GedcomRepository) -> bool:
    """ US06: Divorce date occurs before death date"""
    errors = []

    for family in repo.families:
        divorce_date = family.divorce
        husband = family.husband
        wife = family.wife

        if not divorce_date:
            continue

        if husband.death and husband.death < divorce_date:
            divorce_line_no = family.divorce_line_no
            death_line_no = husband.death_line_no
            errors.append(
                f'ERROR US06: Divorce date (at line {divorce_line_no}) for Family({family.id}) occurs after Husband({husband.id}) death date (at line {death_line_no}).')

        if wife.death and wife.death < divorce_date:
            divorce_line_no = family.divorce_line_no
            death_line_no = wife.death_line_no
            errors.append(
                f'ERROR US06: Divorce date (at line {divorce_line_no}) for Family({family.id}) occurs after Wife({wife.id}) death date (at line {death_line_no}).')

    return errors


def dates_before_current_date(repo: GedcomRepository):
    """ US01 Dates occur before current date"""
    present = Date.today()
    errors = []

    for family in repo.families:
        marriage_date = family.marriage
        divorce_date = family.divorce

        if marriage_date and marriage_date > present:
            invalid_date_line_no = family.marriage_line_no
            errors.append(
                f'ERROR US01: Family({family.id}) marriage date (at line {invalid_date_line_no}) occurs after current date.')

        if divorce_date and divorce_date > present:
            invalid_date_line_no = family.divorce_line_no
            errors.append(
                f'ERROR US01: Family({family.id}) divorce date (at line {invalid_date_line_no}) occurs after current date.')

    for individual in repo.individuals:
        if individual.birth and individual.birth > present:
            invalid_date_line_no = individual.birth_line_no
            errors.append(
                f'ERROR US01: Individual({individual.id}) birth date (at line {invalid_date_line_no}) occurs after current date.')

        if individual.death and individual.death > present:
            invalid_date_line_no = individual.death_line_no
            errors.append(
                f'ERROR US01: Individual({individual.id}) death date (at line {invalid_date_line_no}) occurs after current date.')

    return errors
