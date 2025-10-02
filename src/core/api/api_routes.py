import traceback
from fastapi import APIRouter, Request, HTTPException, status

from core.api.tasks.routes import router as tasks_router
from core.api.user.routes import router as user_router



router = APIRouter(prefix="/api/v1", responses={404: {"description": "Not found"}})


@router.get("/ping")
async def ping_api(request: Request):
    try:
        return "API Server Started"
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")



router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(tasks_router, prefix="/tasks", tags=["To-Do"])

