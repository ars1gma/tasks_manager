import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.model import User
from src.auth.repository import UserRepository
from src.tasks.model import Task
from src.tasks.repository import TaskRepository

pytestmark = pytest.mark.anyio

async def test_create_and_get_one_id_succes(prepare_database, db_session: AsyncSession):
    repo = TaskRepository(db_session)
    repo_user = UserRepository(db_session)
    new_task_model = Task(
        name="Купить молоко",
        description="Жирность 2.5 %",
        user_id=1
    )
    user = User(user_id=1, username="username", hashed_password="pass", email="google@gmail.com")
    await repo_user.create(user)
    created_task = await repo.create(new_task_model)

    assert created_task.task_id is not None
    assert created_task.name == "Купить молоко"

    task_from_db = await repo.get_one_id(user_id=created_task.user_id, task_id=created_task.task_id)

    assert  task_from_db is not None
    assert task_from_db.task_id == created_task.task_id
    assert task_from_db.name == "Купить молоко"

@pytest.mark.parametrize(
    "payload",
    [
        ({"name": "Купить хлеб", "user_id": 1})
    ]
)
async def test_create_and_get_one_id(
    payload: dict[str, str | int],
    prepare_database,
    db_session: AsyncSession
):
    repo = TaskRepository(db_session)
    repo_user = UserRepository(db_session)
    await repo_user.create(User(user_id=1, username="username", hashed_password="pass", email="google@gmail.com"))

    created_task = await repo.create(Task(**payload))

    assert created_task is not None
    assert created_task.name == payload["name"]

    from_task_db = await repo.get_one_id(created_task.user_id, created_task.task_id)

    assert from_task_db is not None
    assert from_task_db.name == payload["name"]

@pytest.mark.parametrize(
    "payload",
    [
        ({"name": "купить молоко", "user_id": 1})
    ]
)
async def test_get_one_name(
    payload: dict[str, str | int],
    prepare_database,
    db_session: AsyncSession
):
    repo = TaskRepository(db_session)
    repo_user = UserRepository(db_session)
    await repo_user.create(User(user_id=1, username="username", hashed_password="pass", email="google@gmail.com"))

    await repo.create(Task(**payload))
    from_task_db = await repo.get_one_name(payload["user_id"], payload["name"])

    assert from_task_db is not None
    assert from_task_db.name == payload["name"]

@pytest.mark.parametrize(
    "task_first, task_second",
    [
        ({"name": "Buy milk", "user_id": 1}, {"name": "Buy bread", "user_id": 1}),
        ({"name": "Buy milk", "user_id": 1}, None)
    ]
)
async def test_get_user_tasks(
    task_first: dict[str, str | int],
    task_second: dict[str, str | int] | None,
    prepare_database,
    db_session: AsyncSession
):
    repo = TaskRepository(db_session)
    repo_user = UserRepository(db_session)
    await repo_user.create(User(user_id=1, username="username", hashed_password="pass", email="google@gmail.com"))

    await repo.create(Task(**task_first))

    if task_second is not None:
        await repo.create(Task(**task_second))

        all_task = await repo.get_user_tasks(task_first["user_id"])

        assert len(all_task) == 2

    else:
        all_task = await repo.get_user_tasks(task_first["user_id"])

        assert len(all_task) == 1

async def test_task_delete(prepare_database, db_session: AsyncSession):
    repo = TaskRepository(db_session)
    repo_user = UserRepository(db_session)
    await repo_user.create(User(user_id=1, username="username", hashed_password="pass", email="google@gmail.com"))

    created_task = await repo.create(Task(name="Buy milk", user_id=1))

    deleted_result = await repo.delete(created_task.user_id, created_task.task_id)

    assert deleted_result == True
