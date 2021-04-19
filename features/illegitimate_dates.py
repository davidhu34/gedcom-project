from typing import List, Optional
from datetime import date as Date
from gedcom import GedcomRepository
from gedcom.tags import GedcomDate


def illegitimate_dates(repo: GedcomRepository) -> List[str]:
  errors: List[str] = []

  for line in repo.lines:
    if line.tag == 'DATE':
      date: Optional[Date] = GedcomDate([line], repo).date
      dd, mmm, yyyy = line.arguments
      day = int(dd)
      month = GedcomDate.month_map[mmm]
      year = int(yyyy)
      if not date or date.year != year or date.month != month or date.day != day:
        errors.append(
            f'ERROR US42: Illegitimate date ({dd} {mmm} {yyyy}) at line ({line.line_no})')

  return errors
