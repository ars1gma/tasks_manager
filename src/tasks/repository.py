from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.model import Task


class TaskRepository:
    """Класс для обращения к базе данных.
       Реализует базовые методы CRUD.
       Защищает от вмешательств одних пользователей к другим.
    """
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, task: Task) -> Task:
        """Добавить задачу в БД.

        Args:
            task (Task): модель для БД.

        Returns:
            Task
        """
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_one_id(self, user_id: int, task_id: int) -> Task | None:
        """Поиск задачи по idю

        Args:
            user_id (int): Номер пользователя в БД.
            task_id (int): Номер задачи в БД.

        Returns:
            Task | None: ...
        """
        result = await self.session.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.task_id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_one_name(self, user_id: int, name: str) -> Task | None:
        result = await self.session.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.name == name)
        )
        return result.scalars().first()

    async def get_user_tasks(self, user_id: int, skip: int, limit: int) -> list[Task]:
        """ Найти задачи пользователя с пагинацией.

        Args:
            user_id (str): Номер пользователя в БД.
            skip (int, optional): Количество пропущенных задач. Defaults to 0.
            limit (int, optional): Количество выведенных задач. Defaults to 5.

        Returns:
            list[Task]: Список из экземпляров класса Task.
        """
        query = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(
            self,
            user_id: int,
            task_id: int,
            task_update_dict: dict[str, str]
            ) -> Task | None:
        """ Обновить задачу в БД.

        Args:
            task_id (int): Номер задачи в БД.
            name (str): ...
            description (str): ...

        Returns:
            Task | None: ...
        """
        if not task_update_dict:
            return self.get_one_id(user_id, task_id)

        query = (
            update(Task)
            .where(Task.task_id == task_id)
            .values(**task_update_dict)
            .returning(Task)
        )
        result = await self.session.execute(query)
        await self.session.commit()

        return result.scalar_one_or_none()

    async def replace(self,
                      user_id: int,
                      task_id: int,
                      name: str,
                      description: str | None = None
                    ) -> Task | None:
        """Заменить задачу в БД.

        Args:
            task_id (int): Номер задачи в БД.
            name (str): ...
            description (str | None): ...

        Returns:
            Task | None: ...
        """

        query = (
            update(Task)
            .where(Task.user_id == user_id)
            .where(Task.task_id == task_id)
            .values(name=name, description=description)
            .returning(Task)
        )

        result = await self.session.execute(query)
        await self.session.commit()

        return result.scalar_one_or_none()

    async def delete(self, user_id: int, task_id: int) -> bool:
        """Удалить задачу с БД.

        Args:
            task_id (int): Номер задачи в БД.

        Returns:
            bool: Если True, то такая задача есть в БД,
                  если False, то такой задачи нет в БД.
        """
        query = delete(Task).where(Task.user_id == user_id).where(Task.task_id == task_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
