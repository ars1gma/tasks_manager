from pydantic import ConfigDict, Field

from src.config.settings import SBase


class STaskAdd(SBase):
    """Схема для валидации данных при создании задачи.

    Args:
        SBase (_type_): Базовый класс схем.
    """
    name: str = Field(..., min_length=3, max_length=64, description="Название задачи. Обязательное поле.")
    description: str | None = Field(default=None, max_length=128, description="Описание задачи. Необязательное поле.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Купить молоко.",
                "description": "В магазине у тёти Марины."
            }
        }
    )

class STaskUpdate(SBase):
    """Схема для валидации данных при обновлении задачи.

    Args:
        SBase (_type_): Базовый класс схем.
    """
    name: str | None = Field(default=None, min_length=3, max_length=64)
    description: str | None = Field(default=None, max_length=128)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Купить хлеб.",
                "description": "У тёти Марины или тёти Люды."
            }
        }
    )

class STaskReplace(SBase):
    """Схема для валидации данных при замене данных о задаче.

    Args:
        SBase (_type_): Базовый класс схем.
    """
    name: str = Field(min_length=3, max_length=64)
    description: str | None = Field(default=None, max_length=128)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Сделать уроки.",
                "description": "Математику, Русский язык, Историю."
            }
        }
    )

class STaskResponse(SBase):
    """Схема для валидации ответов.

    Args:
        SBase (_type_): Базовый класс схем.
    """
    task_id: int = Field(..., description="Номер задачи.")
    name: str = Field(..., description="Назвние задачи.")
    description: str | None = Field(..., description="Описание задачи.")
