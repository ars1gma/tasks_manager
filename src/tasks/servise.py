from src.tasks.model import Task
from src.tasks.repository import TaskRepository
from src.tasks.schemas import STaskAdd, STaskReplace, STaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class TaskService:
    """Сервисный слой модуля задач.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.repo = TaskRepository(session)

    async def create(self, user_id: int, task_input: STaskAdd) -> Task:
        """Добавление новой задачи.

        Args:
            user_id (int): Номер пользователя.
            task_data (STaskAdd): ...

        Returns:
            Task: ...
        """
        new_task = Task(
            name=task_input.name,
            description=task_input.description,
            user_id = user_id
        )
        return await self.repo.create(new_task)

    async def get_task_by_id(self, user_id: int, task_id: int) -> Task | None:
        """Получить задачу по id.

        Args:
            user_id (int): Номер пользователя.
            task_id (int): Номер задачи.

        Returns:
            Task | None: ...
        """
        return await self.repo.get_one_id(user_id, task_id)

    async def get_task_by_name(self, user_id: int, name: str) -> Task | None:
        """Получить задачу по её имени.

        Args:
            user_id (int): Номер пользователя.
            name (str): Название задачи.

        Returns:
            Task | None: ...
        """
        return await self.repo.get_one_name(user_id, name)

    async def get_user_tasks(self, user_id: int, skip: int = 0, limit: int = 5) -> list[Task]:
        """Получить список задач пользовтеля с пагинацией.

        Args:
            user_id (int): Номер пользователя.
            skip (int, optional): Сколько задач от начала пропустить. Defaults to 0.
            limit (int, optional): Сколько задач вывести. Defaults to 5.

        Returns:
            list[Task]: Список из моделей задач.
        """
        return await self.repo.get_user_tasks(user_id, skip=skip, limit=limit)

    async def update(self, user_id: int, task_id: int, task_input: STaskUpdate) -> Task | None:
        """Обновить данные о задаче по её номеру.

        Args:
            user_id (int): Номер пользователя.
            task_id (int): Номер задачи.
            task_input (STaskUpdate): Схема для валидации.

        Returns:
            Task | None: ...
        """
        task_input_dict = task_input.model_dump(exclude_unset=True)
        return await self.repo.update(
            user_id,
            task_id,
            name=task_input_dict.get("name"),
            description=task_input_dict.get("description")
        )

    async def replace(self, user_id: int, task_id: int, task_input: STaskReplace) -> Task | None:
        """Заменить данные о задаче.

        Args:
            user_id (int): Номер пользователя.
            task_id (int): Номер задачи.
            task_input (STaskReplace): ...

        Returns:
            Task | None: ...
        """
        task_input_dict = task_input.model_dump()
        return await self.repo.replace(
            user_id,
            task_id,
            task_input_dict.get("name"),
            task_input_dict.get("description")
        )

    async def delete(self, user_id: int, task_id: int) -> bool:
        """Удалить задачу по task_id.

        Args:
            user_id (int): Номер пользователя.
            task_id (int): Номер задачи.

        Returns:
            bool: _description_
        """
        return await self.repo.delete(user_id, task_id)
