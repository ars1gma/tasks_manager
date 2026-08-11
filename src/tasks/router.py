from fastapi import APIRouter, Depends, HTTPException
from src.tasks.schemas import STaskAdd, STaskReplace, STaskResponse, STaskUpdate
from src.tasks.servise import TaskService
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.deps import CurrentUser, SessionDBDep

router = APIRouter(prefix="/task", tags=["Задачи"])


@router.post(
    "/", 
    status_code = 201,
    response_model=STaskResponse,
    summary="Создание задачи."
)
async def create_task(task_input: STaskAdd, current_user: CurrentUser, session: SessionDBDep):
    """Принимает задачу в формате JSON и сохраняет.

    Args:
        task_input (STaskAdd): Схема для валидации задачи при создании.
        current_user (CurrentUser): Зависимость, которая охраняет и 
                                    извлекает номер текущего пользователя.
        sessesion (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    return await service.create(current_user.user_id, task_input)

@router.get(
    "/",
    response_model=list[STaskResponse],
    summary="Получить список всех своих задач."
)
async def get_user_tasks(
    current_user: CurrentUser,
    session: SessionDBDep,
    skip: int = 0,
    limit: int = 0
):
    """Получить все задачи текущего пользователя

    Args:
        task_id (int): Номер 
        сurrent_user (CurrentUser): Зависимость, которая охраняет и 
                                    извлекает номер текущего пользователя.
        session (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    return await service.get_user_tasks(current_user.user_id, skip=skip, limit=limit)

@router.get(
    "/{task_id}",
    response_model=STaskResponse,
    summary="Найти задачу по её номеру."
)
async def get_task_by_id(task_id: int, current_user: CurrentUser, session: SessionDBDep):
    """Получить задачу по task_id.

    Args:
        task_id (int): Номер задачи.
        current_user (CurrentUser): Зависимость, которая охраняет и 
                                    извлекает номер текущего пользователя.
        session (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    task = await service.get_task_by_id(current_user.user_id, task_id)
    if task is None:
        HTTPException(
            status_code=404,
            detail=f"Задача с номером {task_id} не найдена."
        )
    return task

@router.get(
    "/{task_name}",
    response_model=STaskResponse,
    summary="Найти задачу по её имени."
)
async def get_taks_by_name(task_name: str, curren_user: CurrentUser, session: SessionDBDep):
    """Получить задачу по её названию.

    Args:
        task_name (str): Название задачи.
        curren_user (CurrentUser): Зависимость, которая охраняет и 
                                   извлекает номер текущего пользователя.
        session (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    task = await service.get_task_by_name(curren_user.user_id, task_name)
    if task is None:
        HTTPException(
            status_code=404,
            detail=f"Задача с названием {task_name} не найдена."
        )
    return task

@router.patch(
    "/{task_id}",
    response_model=STaskResponse,
    summary="Обновить данные о задаче."
)
async def task_update(
    task_id: int,
    task_input: STaskUpdate,
    current_user: CurrentUser,
    session: SessionDBDep
):
    """Частично обновить данные о задаче.

    Args:
        task_id (int): Номер задачи
        taks_input (STaskUpdate): Схема валидации для обновления задачи.
        current_user (CurrentUser): Зависимость, которая охраняет и 
                                    извлекает номер текущего пользователя.
        session (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    task = await service.update(current_user.user_id, task_id, task_input)
    if task is None:
        HTTPException(
            status_code=404,
            detail=f"Задача с номером {task_id} не найдена или у вас нет прав на её изменение."
        )
    return task

@router.put(
    "/{task_id}",
    summary="Обновить все данные о задаче."
)
async def task_replace(
    task_id: int,
    task_input: STaskReplace,
    current_user: CurrentUser,
    session: SessionDBDep
):
    """Заменить данные о задаче по task_id.

    Args:
        task_id (int): Номер задачи
        task_input (STaskReplace): Схема для валидации данных при полном обновении задачи.
        current_user (CurrentUser): Зависимость, которая охраняет и 
                                    извлекает номер текущего пользователя.
        session (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    task = await service.replace(current_user.user_id, task_id, task_input)
    if task is None:
        HTTPException(
            status_code=404, 
            detail=f"Задача с номером {task_id} не найдена или у вас нет прав её изменить."
        )
    return task

@router.delete(
    "/{task_id}",
    status_code=204,
    summary="Удалить задачу"
)
async def task_delete(
    task_id: int,
    current_user: CurrentUser,
    session: SessionDBDep
):
    """Удалить задачу по task_id.

    Args:
        task_id (int): Номер задачи.
        current_user (CurrentUser): Зависимость, которая охраняет и 
                                    извлекает номер текущего пользователя.
        session (SessionDBDep): Сессия для обращения к БД.
    """
    service = TaskService(session)
    deleted = await service.delete(current_user.user_id, task_id)
    if not deleted:
        HTTPException(
            statuc_code=404,
            detail=f"Задача с номером {task_id} не найдена или у вас нет прав её удалить."
        )
