class MyException(Exception):
    pass


class UserIsNotInDatabase(MyException):
    pass


class UserAlreadyExists(MyException):
    pass


class FailedToReplaceUser(MyException):
    pass


class LevelModelDoesNotExist(MyException):
    pass


class BlockModelDoesNotExist(MyException):
    pass
