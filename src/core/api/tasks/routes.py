from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from core.db.db_config import SessionManager
from . import services
from .schema import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post("/", status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(SessionManager.get_session)
):
    return services.create_task(db, task)

@router.get("/")
def get_all_tasks_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(SessionManager.get_session)
):
    return services.get_tasks(
        db=db, skip=skip, limit=limit, status_filter=status, search_term=search
    )


@router.get("/{task_id}")
def get_task_route(
    task_id: int,
    db: Session = Depends(SessionManager.get_session)
):

    return services.get_task(db, task_id)


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(SessionManager.get_session)
):
    return services.update_task(db, task_id, task_data)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(SessionManager.get_session)
):
    return services.delete_task(db, task_id)

