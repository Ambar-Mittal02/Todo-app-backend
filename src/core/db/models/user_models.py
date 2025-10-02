from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime

import core.utils.constants as C
from ..db_config import Base

class UserModel(Base):
    __tablename__ = C.USER_MODEL

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    user_id = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column( DateTime(timezone=True), server_default=func.now())
