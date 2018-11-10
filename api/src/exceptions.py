class PreziException(Exception):
    """ A base class for exceptions used by Prezi. """
    status_code = None

    def __str__(self):
        return repr(self.args[0])


class BadRequestException(PreziException):
    status_code = 400


class ServerErrorException(PreziException):
    status_code = 500


class ResourceNotFoundException(PreziException):
    status_code = 500
