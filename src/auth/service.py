from src.auth.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from src.auth.model import User
from src.auth.repository import UserRepository
from src.auth.schemas import SUserReg
from src.auth.security import create_access_token, hashed_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession


class AuthServise:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def register_new_user(self, user: SUserReg) -> User:
        existing_user = await self.repo.get_username_or_email()

        if existing_user:
            raise UserAlreadyExistsError()

        hashed_pwd = hashed_password(user.password)

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pwd
        )

        return await self.repo.create(new_user)

    async def authenticate_user(
            self,
            username_input: str,
            password_input: str,
            email_input: str | None = None
    ) -> str:
        """Бизнес логика входа в систему.

        Args:
            username_input (str): Имя пользователя.
            password_input (str): Пароль пользователя.

        Returns:
            str: ...
        """

        user_db = await self.repo.get_username_or_email(username=username_input, email=email_input)

        if not user_db or not verify_password(password_input, user_db.hashed_password):
            raise InvalidCredentialsError()

        token_payload = {"sub": str(user_db.user_id)}
        token = create_access_token(data=token_payload)
        return token
    