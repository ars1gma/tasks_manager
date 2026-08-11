class UserAlreadyExistsError(Exception):
    """Логин или пароль уже заняты."""

class InvalidCredentialsError(Exception):
    """Неверный логин или пароль."""
