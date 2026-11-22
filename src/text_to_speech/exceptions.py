class ConfigurationError(Exception):
    """Raised when there are problems with configuration files"""

    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)


class InputTextFormatError(Exception):
    """Raised when there are problems reding input text files"""

    def __init__(self, message):
        super(InputTextFormatError, self).__init__(message)


class InputTextValidationError(Exception):
    """
    Raised when there are problems when validating already
    loaded input text files
    """

    def __init__(self, message):
        super(InputTextValidationError, self).__init__(message)


class ProjectDirectoryValidationError(Exception):
    """
    Raised when there are problems when validating the project directory
    """

    def __init__(self, message):
        super(ProjectDirectoryValidationError, self).__init__(message)
