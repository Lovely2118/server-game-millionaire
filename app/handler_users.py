from app.core.utils import get_users, save_users
from app.errors import UserAlreadyExists, FailedToReplaceUser
from app.schemes.quiz import User


def add_user(user: User) -> None:
    """
        Добавление нового пользователя в бд (json)
    :param user:
    :return:
    """

    users = get_users()

    is_uniqueness = check_uniqueness(user, users)
    if is_uniqueness:
        users.append(user)
        save_users(users)

    raise UserAlreadyExists()


def update_user(user: User) -> None:
    """
        Обновление данных пользователя в бд (json)
    :param user:
    :return:
    """

    users = get_users()

    is_uniqueness = check_uniqueness(user, users)
    if is_uniqueness is False:
        replace_user(user, users)
        save_users(users)
        return
    raise UserAlreadyExists()


def check_uniqueness(user: User, users: list['User']) -> bool:
    for user_from_bd in users:
        if user_from_bd.id == user.id:
            return False
    return True


def replace_user(user: User, users: list['User']) -> None:
    selected_index = -1
    for index in range(len(users)):
        user_from_bd = users[index]
        if user_from_bd.id == user.id:
            selected_index = index
            break

    if selected_index == -1:
        raise FailedToReplaceUser()

    users[selected_index] = user
