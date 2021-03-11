
# from features.project2 import validate_gedcom_file
from features.project3 import print_gedcom_info
from gedcom import GedcomRepository, prompt_repository_file
from features.family_role_validation import correct_gender_roles


if __name__ == "__main__":
    repo: GedcomRepository = prompt_repository_file()

    repo \
        .validate(correct_gender_roles) \
        .showcase(print_gedcom_info)
