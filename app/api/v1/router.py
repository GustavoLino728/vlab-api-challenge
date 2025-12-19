from fastapi import APIRouter
from app.api.v1.routes.abastecimentos import router as abastecimentos_router
from app.api.v1.routes.motoristas import router as motoristas_router
from app.api.v1.routes.health import router as health_router


api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(abastecimentos_router)
api_v1_router.include_router(motoristas_router)
api_v1_router.include_router(health_router)
