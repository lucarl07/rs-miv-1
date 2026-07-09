# Módulos da Aplicação
from app.conn.db import get_db
from app.models.user import User
from app.repositories.user import check_if_user_creds_exist, create_new_user, get_user_by_email
from app.schemas.user import Token, UserCreate, UserLogin, UserOut
from app.utils.jwt import create_access_token
from app.utils.pw_hashing import verify_password

# Bibliotecas Externas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    """Registra um novo usuário, validando unicidade de nickname e email."""

    are_user_credentials_used = await check_if_user_creds_exist(
        db, user_data.nickname, user_data.email
    )    
    if are_user_credentials_used is True:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nickname ou email já cadastrado.",
        )

    new_user = await create_new_user(db, user_data)
    return new_user

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Realiza o login na conta de um usuário, atribuindo a ele um JWT de acesso."""

    user = await get_user_by_email(db, user_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    passwords_match = verify_password(user_data.password, user.hashed_password)
    if not passwords_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    access_token = create_access_token(user.id) 

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
