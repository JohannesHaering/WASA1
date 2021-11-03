class NotFoundException(Exception):
    def __init__(self, message):
        self.errorCode = 404
        self.message = message
        super().__init__(message)


class InvalidArgumentsException(Exception):
    def __init__(self, message):
        self.errorCode = 400
        self.message = message
        super().__init__(message)


class InternalServerError(Exception):
    def __init__(self, message):
        self.errorCode = 500
        self.message = message
        super().__init__(message)


class ConflictException(Exception):
    def __init__(self, message):
        self.errorCode = 409
        self.message = message
        super().__init__(message)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
            self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
