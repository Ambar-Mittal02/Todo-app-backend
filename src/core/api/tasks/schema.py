from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskStatus(Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class UserRole(Enum):
    ADMIN = "Admin"
    EXECUTIVE = "Executive"


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[datetime]
    assigned_to: Optional[str]
    assigned_name: Optional[str]
    created_at: datetime
    updated_at: datetime
