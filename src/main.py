import logging
from exceptiongroup import ExceptionGroup
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import (
    IntegrityError,
    DatabaseError,
    SQLAlchemyError,
    DBAPIError,
    ProgrammingError,
)

from core.api.api_routes import router as api_router
from core.db.db_config import engine
from core.utils.log_config import log

from core.db.models.user_models import Base as UserBase

UserBase.metadata.create_all(bind=engine)


app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    openapi_url="/api/v1/openapi.json",
)

logging.getLogger("uvicorn.error").disabled = True
logging.getLogger("uvicorn.access").disabled = True



@app.exception_handler(Exception)
async def handle_all_exceptions(request, exc):
    detail = {}

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail["detail"] = "Internal server error"

    if isinstance(exc, ExceptionGroup):
        for sub_exc in exc.exceptions:
            log.error(f"Sub Exception --> {sub_exc}")

            if isinstance(sub_exc, IntegrityError):
                status_code = status.HTTP_400_BAD_REQUEST
                detail["detail"] = "Duplicate error"

            elif isinstance(sub_exc, ProgrammingError):
                log.error("Programming Error -->")
                status_code = status.HTTP_400_BAD_REQUEST
                column_name = (
                    str(sub_exc.orig).split("column ")[1].split(" does not exist")[0]
                )
                detail["detail"] = f"Undefined Column: {column_name}"

            elif isinstance(sub_exc, SQLAlchemyError):
                status_code = status.HTTP_400_BAD_REQUEST
                detail["detail"] = "SQL Alchemy Error"

            elif isinstance(sub_exc, DatabaseError):
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                detail["detail"] = "Database error"

            elif isinstance(sub_exc, DBAPIError):
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                detail["detail"] = "DBAPI error"

            elif isinstance(sub_exc, HTTPException):
                detail["detail"] = sub_exc.detail
                status_code = status.HTTP_404_NOT_FOUND

    return JSONResponse(
        content=detail, status_code=status_code, media_type="application/json"
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PATCH", "DELETE", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router)

log.info("To-Do App server started...")