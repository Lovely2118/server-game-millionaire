class HandlerUsersException(Exception):
    pass


class UserIsNotInJson(HandlerUsersException):
    pass


class UserAlreadyExists(HandlerUsersException):
    pass


class FailedToReplaceUser(HandlerUsersException):
    pass