from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, Integer, func
from ..db_config import Base
import core.utils.constants as C
from datetime import datetime
from core.api.tasks.schema import TaskStatus
from ...utils.common_func import get_enum_values


class TaskModel(Base):
    __tablename__ = C.TASKS_TABLE

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    task_status = Column(Enum(TaskStatus, values_callable=get_enum_values), default=TaskStatus.TODO.value)
    due_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.utcnow)
