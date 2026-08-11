from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.auth.repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.model import User
from src.config.database import get_session_db
from src.config.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SessionDBDep = Annotated[AsyncSession, Depends(get_session_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(
        session: SessionDBDep,
        token: TokenDep
) -> User:
    """Проверка авторизации.

    Args:
        session (AsyncSession): _description_
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).
    """
    credantials_exception = HTTPException(
        status_code=401, 
        detail="Не удалось валидировать токен доступа или его срок действия истёк."
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credantials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Срок действия токена истёк, пожалуйста, войдите заново."
        )
    except jwt.PyJWTError:
        raise credantials_exception
    
    repo = UserRepository(session)
    user = await repo.get_one_id(int(user_id))
    if user is None:
        raise credantials_exception

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
