from gedcom import GedcomRepository, prompt_repository_file
from features.project3 import print_gedcom_info
from features.family_role_validation import correct_gender_roles, unique_family_spouses

from adsfl;asdkf
if __name__ == "__main__":
    repo: GedcomRepository = prompt_repository_file()

    repo \
        .validate(correct_gender_roles) \
        .validate(unique_family_spouses) \
        .validate(asd;flkasd) \
        .showcase(print_gedcom_info)
