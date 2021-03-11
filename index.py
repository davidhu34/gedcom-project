
# from features.project2 import validate_gedcom_file
from features.project3 import print_gedcom_info
from gedcom import GedcomRepository, prompt_repository_file

if __name__ == "__main__":
    repo: GedcomRepository = prompt_repository_file()

    repo \
        .showcase(print_gedcom_info)
