from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from core.db.models.task_model import TaskModel
from .schema import TaskCreate, TaskUpdate
import core.utils.constants as C
from core.utils.log_config import log


def create_task(db: Session, task: TaskCreate):
    try:
        db_task = TaskModel(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        log.error(f"Task creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task creation failed"
        )


def get_tasks(
    db: Session, skip: int = 0, limit: int = 10, status_filter: str = None, search_term: str = None
):
    try:
        query = db.query(TaskModel)
        if status_filter:
            query = query.filter(
                cast(TaskModel.task_status, String) == status_filter
            )

        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    TaskModel.title.ilike(search_pattern),
                    TaskModel.description.ilike(search_pattern)
                )
            )

            # Apply pagination
        tasks = query.order_by(TaskModel.id.desc()).offset(skip).limit(limit).all()
        total_count = query.count()

        return {
            "data": tasks,
            "total_count": total_count
        }
    except Exception as e:
        log.error(f"Error fetching tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tasks"
        )


def get_task(db: Session, task_id: int):
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(f"Error fetching task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch task"
        )


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        update_dict = task_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(task, key, value)

        if update_dict.get("status"):
            task.task_status = update_dict["status"]

        db.commit()
        db.refresh(task)
        return task
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        log.error(f"Task update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task update failed"
        )


def delete_task(db: Session, task_id: int):
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()
        return {"detail": "Task deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        log.error(f"Task deletion failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task deletion failed"
        )
