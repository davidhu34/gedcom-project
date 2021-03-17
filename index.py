from gedcom import GedcomRepository, prompt_repository_file
from features.project3 import print_gedcom_info
from features.family_role_validation import correct_gender_roles, unique_family_spouses
from features.Unique_name_first_names_and_birthdate_validations import unique_name_and_birth, unique_names_in_families


if __name__ == "__main__":
    repo: GedcomRepository = prompt_repository_file()

    repo \
        .showcase(print_gedcom_info) \
        .validate(correct_gender_roles) \
        .validate(unique_family_spouses) \
        .validate(unique_name_and_birth) \
        .validate(unique_names_in_families) 

           
        