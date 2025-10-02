from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request

from core.db.db_config import SessionManager
from .schema import UserCreate


from core.api.user.services import create_user, get_users_list, get_user_by_id

router = APIRouter()


@router.post("/user")
async def create_user_route(
    user_request: UserCreate,
    db: Session = Depends(SessionManager.get_session),
):
    user_res = create_user(db, user_request)
    return {"data": user_res}


@router.get("/list")
async def get_user_route(
    skip: int = 0,
    limit: int = 10,
    search_value: str = None,
    db: Session = Depends(SessionManager.get_session),
):
    user_details = get_users_list(db, skip, limit, search_value)
    return user_details


@router.get("/user")
async def get_user_route(
    user_id: int, db: Session = Depends(SessionManager.get_session)
):

    user_details = get_user_by_id(db, user_id)
    return {"data": user_details}


