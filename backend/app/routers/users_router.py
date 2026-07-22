# Bibliotecas Nativas
from typing import Annotated

# Bibliotecas Externas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Módulos do Projeto
from app.conn.db import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.user import nickname_exists
from app.repositories.user_key import upsert_public_key
from app.schemas.user import UserFieldCheck, UserPublic
from app.schemas.user_key import PublicKeyUpload
from app.utils.data_validation import check_nickname_validity

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/check-nickname/{nickname}", 
    response_model=UserFieldCheck, tags=["auth"]
)
async def check_nickname(
    nickname: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        check_nickname_validity(nickname)
    except Exception as e:
        error_message = " ".join(e.args[0].split()) # Removendo indentação e caracteres '\n'
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error_message
        )

    does_user_exist = await nickname_exists(db, nickname)

    if does_user_exist is True:
        is_nickname_available = False
    else:
        is_nickname_available = True

    return UserFieldCheck(available=is_nickname_available)

@router.get("/me", response_model=UserPublic)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user

@router.post("/me/public-key", status_code=status.HTTP_204_NO_CONTENT)
async def submit_public_key(
    payload: PublicKeyUpload,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await upsert_public_key(db, current_user.id, payload.public_key)

