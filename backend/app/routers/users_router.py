# Bibliotecas Nativas
from typing import Annotated

# Bibliotecas Externas
from fastapi import APIRouter, Depends

# Módulos do Projeto
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user
