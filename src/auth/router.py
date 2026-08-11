from src.auth.deps import SessionDBDep
from src.auth.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.schemas import SUserReg
from src.auth.service import AuthServise
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и Аутентификация."]
)

@router.post("/register",status_code=201)
async def register(
    user_input: SUserReg,
    session: SessionDBDep
):
    service = AuthServise(session)

    try:
        await service.register_new_user(user_input)

        return {"status": "success", "detail": "Пользователь успешно создан"}
    
    except UserAlreadyExistsError:
        raise HTTPException(
            starus_code=400,
            detail="Пользователь с таким именем или почтой уже зарегестрирован."
        )

@router.post("/login")
async def login(session: SessionDBDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    service = AuthServise(session)

    try:
        token = await service.authenticate_user(
            username=form_data.username,
            password=form_data.password
        )
        return {"access_token": token, "token_type": "bearer"}

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
