from enum import Enum


class CacheNamespace(Enum):
    # === Аккаунт пользователя === #
    ACCOUNT_USER = 'ACCOUNT_USER'

    # === Авторизация === #
    YANDEX_USER_INFO = 'YANDEX_USER_INFO'  # Получение информации о пользователе по токену из Яндекс

    # === Права доступа и группы === #
    PERMISSIONS_SYSTEM = 'PERMISSIONS_SYSTEM'

    # === Операторы === #
    OPERATORS_LIST_ISD = 'OPERATORS_LIST_ISD'  # Список account_user_id операторов по ID группы
    OPERATOR_LIST_INFO = 'OPERATOR_LIST_INFO'  # Список операторов
    OPERATOR_INFO = 'OPERATOR_INFO'  # Информация об операторе

    # === #
    ANY = 'ANY'