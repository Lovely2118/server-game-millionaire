class HandlerUsersException(Exception):
    pass


class UserIsNotInDatabase(HandlerUsersException):
    pass


class UserAlreadyExists(HandlerUsersException):
    pass


class FailedToReplaceUser(HandlerUsersException):
    pass