from gedcom import GedcomRepository, prompt_repository_file
from features.project3 import all_gedcom_individuals, all_gedcom_families
from features.family_role_validation import correct_gender_roles, unique_family_spouses
from features.unique_name_first_names_and_birthdate_validations import unique_name_and_birth, unique_first_names_in_families
from features.birth_before import birth_before_death, birth_before_marriage
from features.valid_dates import divorce_before_death, dates_before_current_date
from features.birth_before_parents_marriage_and_death import birth_before_parents_marriage, birth_before_parents_death
from features.mariage_before import marriage_before_death, marriage_before_divorce
from features.id_validations import unique_ids, corresponding_entries
from features.age_less_than_150_years_old_and_siblings_order import age_and_age_at_death, order_siblings_by_age
from features.list_of_all_deceased_and_living_married import deceased_individual_list, living_married_list
from features.marriage_after_14_and_male_last_names import marriage_after_14, male_last_names
from features.parents_too_old import parents_too_old, sibling_spacing
from features.multiple_births import siblings_born_at_same_time,too_many_siblings
from features.list_recent_births_deaths_test import list_recent_births, list_recent_deaths
from features.list_of_living_single_and_multiple_births import  living_single_list, list_multiple_births
from features.large_age_diff import large_age_diff
from features.illegitimate_dates import illegitimate_dates

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
        .validate(corresponding_entries) \
        .validate(marriage_before_death) \
        .validate(marriage_before_divorce) \
        .validate(age_and_age_at_death) \
        .print_individuals(order_siblings_by_age) \
        .validate(marriage_after_14) \
        .validate(male_last_names) \
        .print_individuals(deceased_individual_list) \
        .print_individuals(living_married_list) \
        .validate(sibling_spacing) \
        .validate(parents_too_old) \
        .validate(siblings_born_at_same_time) \
        .validate(too_many_siblings) \
        .print_individuals(list_recent_births) \
        .print_individuals(list_recent_deaths) \
        .print_individuals(living_single_list) \
        .print_individuals(list_multiple_births) \
        .validate(large_age_diff) \
        .validate(illegitimate_dates)
