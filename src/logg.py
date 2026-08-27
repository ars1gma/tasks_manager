import logging

LOGGING_CONFIG = {
    "version": 1.0,

    "disable_existing_loggers": False,

    "formatters": {
        "file": {
            "format": "%(asctime)s [%(levelname)s %(name)s:%(lineno)d - %(message)s]"
        },
        "console": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "console"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "file",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 2,
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "tasks_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "prograte": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("tasks_logger")
