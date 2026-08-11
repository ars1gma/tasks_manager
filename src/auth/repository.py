from src.auth.model import User
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_db: User) -> User:
        """Создать пользователя в БД.

        Args:
            username (str): Имя пользователя.
            email (EmailStr): Электроннная почта пользователя.
            password (str): пароль пользователя, нехешированный.

        Returns:
            User: ...
        """
        self.session.add(user_db)
        await self.session.commit()
        await self.session.refresh(user_db)
        return user_db

    async def get_username_or_email(self, username: str | None = None, email: str | None = None) -> User | None:
        """Получить данные пользователя по айди или электронной почте.
        """
        query = (
            select(User)
            .where((User.username == username) | (User.email == email))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(
            self,
            user_id: int | None = None,
            username: str | None = None,
            email: str | None = None,
            password: str | None = None
            ) -> User | None:
        """Обновить часть данных о пользователе в БД по user_id.

        Args:
            user_id (int | None): Номер пользлователя в БД.
            username (str | None): Имя пользователя.
            email (EmailStr | None): Электронная почта пользователя.
            password (str | None): Пароль пользователя

        Returns:
            User | None: ...
        """
        if not user_id and not username and not email and not password:
            result = await self.session.execute(
                select(User)
                .where((User.user_id == user_id)
                       | (User.username == username)
                       | (User.email == email))
            )
            return result.scalar_one_or_none()
        
        query = (
            update(User)
            .where((User.user_id == user_id)
                   | (User.username == username)
                   | (User.email == email))
            .values(username, email, password)
            .returning(User)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def replace(
            self,
            user_id: int,
            username: str,
            email: str,
            password: str
            ) -> User | None:
        """Заменить данные о пользовтеле в БД.

        Args:
            user_id (int): Номер пользователя в БД.
            username (str): Имя пользователя.
            email (str): Электронная почта пользователя.
            password(str): Пароль пользоветеля.

        Returns:
            User | None: ...
        """

        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(username, email, password)
            .returning(User)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, user_id: int) -> None:
        """Удалить пользователя из БД.

        Args:
            user_id (int):

        Returns: 
            None: ...
        """
        self.session.execute(
            delete(User).where(User.user_id == user_id)
        )
