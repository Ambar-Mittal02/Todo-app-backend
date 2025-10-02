import logging
from logging.config import dictConfig

LOGGER_NAME = 'crossway'

# Define the logging configuration dictionary directly
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            "fmt": "%(levelprefix)s %(asctime)s %(filename)s %(lineno)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True
        },
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(filename)s %(lineno)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True
        },
    },
    "handlers": {
        'access': {
            'class': 'logging.StreamHandler',
            'formatter': 'access',
            'stream': 'ext://sys.stdout'
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        LOGGER_NAME: {"handlers": ["default"], "level": "DEBUG", "propagate": False},
        "uvicorn": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.error': {
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Apply the logging configuration
dictConfig(logging_config)
log = logging.getLogger(LOGGER_NAME)