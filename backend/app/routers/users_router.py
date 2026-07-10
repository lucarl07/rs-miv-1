# Bibliotecas Nativas
from typing import Annotated

# Bibliotecas Externas
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Módulos do Projeto
from app.conn.db import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.user_key import upsert_public_key
from app.schemas.user import UserPublic
from app.schemas.user_key import PublicKeyUpload

router = APIRouter(prefix="/users", tags=["users"])

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
