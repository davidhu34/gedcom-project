class GedcomException(Exception):
    ''' custom GEDCOM base exception '''

    def __init__(self, message='') -> None:
        # construct exception and store erroneous path if given
        super().__init__(message)


class GedcomFileNotFound(GedcomException):
    ''' custom file not found exception '''

    def __init__(self, message, path) -> None:
        # construct exception and store erroneous path if given
        super().__init__(message)
        self.path = path


class GedcomLineParsingException(GedcomException):
    pass


class GedcomDataParsingException(GedcomException):
    pass


class GedcomInvalidData(GedcomException):
    pass


class GedcomDateInvalidFormat(GedcomException):
    pass


class GedcomValidationException(GedcomException):
    pass
