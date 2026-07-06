from app.conn.db import get_db
from .auth_router import router as auth_router
from .ws_router import router as ws_router

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter();

@router.get("/db")
async def root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 'Hello World'"))
    value = result.scalar()
    return {"message": value}

router.include_router(auth_router)
router.include_router(ws_router)

