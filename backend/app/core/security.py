from datetime import datetime, timedelta, timezone

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Создание токена для аутентификации.

    :param data: Payload для создания токена.
    :type data: dict
    :param expires_delta: Срок действия токена.
    :type expires_delta: timedelta
    :return: Токен.
    :rtype: str
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля.

    :param plain_password: Пользовательский пароль.
    :type plain_password: str
    :param hashed_password: Хэш пароля.
    :type hashed_password: str
    :return: Результат проверки.
    :rtype: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хэширование пароля.

    :param password: Пользовательский пароль.
    :type password: str
    :return: Хэш пароля.
    :rtype: str
    """
    return pwd_context.hash(password)
