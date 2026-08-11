from pydantic import BaseModel, EmailStr, Field


class SUserMixin(BaseModel):
    model_config = {"from_attributes": True}

class SUserReg(SUserMixin):
    username: str = Field(..., description="Уникальное имя пользователя")
    email: EmailStr = Field(
        ...,
        min_length=3,
        max_length=128, 
        description="Уникальная электронная почта."
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Пароль должен содержать не менее 6 символов."
    )

class SUserUpdate(SUserMixin):
    username: str | None = Field(None, description="Уникальное имя пользователя")
    email: EmailStr | None = Field(
        None,
        min_length=3,
        max_length=128, 
        description="Уникальная электронная почта."
    )
    password: str | None = Field(
        None,
        min_length=6,
        max_length=100,
        description="Пароль должен содержать не менее 6 символов."
    )

class SUserReplace(SUserReg): ...

class SUserGet(SUserMixin):
    username: str | None = None
    email: EmailStr | None = None
