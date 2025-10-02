import traceback
from fastapi import HTTPException
from sqlalchemy import  or_, cast, String

from core.utils.log_config import log
from .schema import UserCreate

from core.db.models.user_models import UserModel


def is_active_email_exist(db, unique_email):
    try:
        user = db.query(UserModel).filter_by(email=unique_email).first()

    except Exception as err:
        log.error(f"Check user email {unique_email} Error--> {err}")
        traceback.print_exc()
        raise err

    return user


def get_users_list(db, skip, limit, search_value=None):
    """
    Retrieve a users of files from the database with optional column selection and pagination.
    """
    try:

        users_query = db.query(UserModel)

        if search_value:
            search_conditions = []
            included_columns = ["name", "email"]
            for column in UserModel.__table__.columns:
                if column.name in included_columns:
                    if column.name == "role":
                        search_conditions.append(cast(column, String).ilike(f"%{search_value}%"))
                    else:
                        search_conditions.append(column.ilike(f"%{search_value}%"))

            users_query = users_query.filter(or_(*search_conditions))

        total_count = users_query.with_entities(UserModel.id).count()
        log.info(f"Total Users data found in the database: {total_count}")

    except Exception as err:
        log.error(f"Get Users --> {err}")
        traceback.print_exc()
        raise err

    user_res = users_query.order_by(UserModel.id.asc()).offset(skip).limit(limit).all()

    return {"total_count": total_count, "data": user_res}


def create_user(db, user_request: UserCreate):
    """
    Create a new user.
    """
    log.info(f"Create user {user_request} ")
    try:
        existing_user = is_active_email_exist(db, user_request.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = UserModel(name=user_request.name, email=user_request.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        log.info(f"User created: {new_user.email}")
        return new_user

    except Exception as err:
        log.error(f"User Add Error ==> {err}")
        traceback.print_exc()
        raise err


def get_user_by_id(db, user_id: int):
    """
    Retrieve a user by their ID.
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except Exception as err:
        log.error(f"Get User by ID Error ==> {err}")
        traceback.print_exc()
        raise err
