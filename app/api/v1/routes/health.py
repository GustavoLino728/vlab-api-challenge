from fastapi import APIRouter
from app.api.deps import DbSession


router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(db: DbSession):
    await db.execute("SELECT 1")

    return {
        "status": "ok",
        "version": "1.0.0",
        "database": "up",
    }
