import pytest

from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.model import Task
from src.tasks.repository import TaskRepository

pytestmark = pytest.mark.integration

async def test_create_and_get_one_id_succes(prepare_database, db_session: AsyncSession) -> None:
    repo = TaskRepository(db_session)

    new_task_model = Task(
        name="Купить молоко",
        description="Жирность 2.5 %",
        user_id=10
    )

    created_task = await repo.create(new_task_model)

    assert created_task.task_id is not None
    assert created_task.name == "Купить молоко"

    task_from_db = await repo.get_one_id(user_id=created_task.user_id, task_id=created_task.task_id)

    assert  task_from_db is not None
    assert task_from_db.task_id == craeted_task.task_id
    assert task_from_db.name == "Купить молоко"

@pytest.mark.parametrize(

)
async def test_create_and_get_one_id_and_name(
    function: Callable[[int, int | str], Task | None],
    payload: dict[str, str | int],
    prepare_database,
    db_session: AsyncSession
) -> None:
    repo = TaskRepository(db_session)

    created_task = await repo.create(Task(**payload))

    assert created_task.task_id is not None
    assert created_task.name == "Купить молоко"
    assert created_task.description is not None

    from_task_db = await 