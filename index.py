from gedcom import GedcomRepository, prompt_repository_file
from features.project3 import all_gedcom_individuals, all_gedcom_families
from features.family_role_validation import correct_gender_roles, unique_family_spouses
from features.Unique_name_first_names_and_birthdate_validations import unique_name_and_birth, unique_first_names_in_families
from features.birth_before import birth_before_death, birth_before_marriage
from features.valid_dates import divorce_before_death, dates_before_current_date
from features.birth_before_parents_marriage_and_death import birth_before_parents_marriage, birth_before_parents_death
from features.mariage_before import marriage_before_death,marriage_before_divorce
from features.id_validations import unique_ids, corresponding_entries
from features.age_and_age_at_death_less_than_150_years_old import age_and_age_at_death

if __name__ == "__main__":
    repo: GedcomRepository = prompt_repository_file()

    repo \
        .print_individuals(all_gedcom_individuals) \
        .print_families(all_gedcom_families) \
        .validate(correct_gender_roles) \
        .validate(unique_family_spouses) \
        .validate(unique_name_and_birth) \
        .validate(unique_first_names_in_families) \
        .validate(birth_before_death) \
        .validate(birth_before_marriage) \
        .validate(divorce_before_death) \
        .validate(dates_before_current_date) \
        .validate(birth_before_parents_marriage) \
        .validate(birth_before_parents_death) \
        .validate(unique_ids) \
        .validate(corresponding_entries)\
        .validate(marriage_before_death)\
        .validate(marriage_before_divorce)
        .validate(age_and_age_at_death)
