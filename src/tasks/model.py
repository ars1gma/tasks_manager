from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class Task(Base):
    """...

    Args:
        task_id (int): Номер задачи в БД
        name (str): Название задачи
        description (str | None): Описание задачи
        user_id (int): Номер пользователя, создавшего задачу
    """
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
