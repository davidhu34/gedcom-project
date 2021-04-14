from gedcom import GedcomRepository


def marriage_after_14(repo: GedcomRepository):
    """ US10 Marriage of individuals should occur after age 14 """
    errors = []
    for family in repo.families:
        marriage_date = family.marriage

        if not marriage_date:
            continue

        for husband in family.husbands:
            if not husband.birth:
                continue
            husband_14th = husband.birth.replace(year=husband.birth.year+14)
            if husband.birth and (husband_14th > marriage_date):
                invalid_marr_date_line_no = family.marriage_line_no
                errors.append(
                    f'ERROR US10: Individual({husband.id}) in Family({family.id}) married (at line {invalid_marr_date_line_no}) when under age 14.')

        for wife in family.wifes:
            if not wife.birth:
                continue
            wife_14th = wife.birth.replace(year=wife.birth.year+14)
            if wife.birth and (wife_14th > marriage_date):
                invalid_marr_date_line_no = family.marriage_line_no
                errors.append(
                    f'ERROR US10: Individual({wife.id}) in Family({family.id}) married (at line {invalid_marr_date_line_no}) when under age 14.')

    return errors


def male_last_names(repo: GedcomRepository):
    """ US16 All males in a family must share the same last name """
    errors = []

    for family in repo.families:
      if not family.children:
        continue

      for husband in family.husbands:
        male_ln = husband.last_name

        for child in family.children:
            child_ln = child.last_name
            if child.is_male and child_ln != male_ln:
                errors.append(
                    f'ERROR US16: In Family({family.id}), Son({child.id}) last name (at line {child.name_line_no}) does not match Father({husband.id}) last name (at line {husband.name_line_no}).'
                )

    return errors
