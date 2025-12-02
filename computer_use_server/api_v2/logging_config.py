import logging
import logging.config
import os

def setup_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s %(levelname)s %(name)s - %(message)s"},
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {"handlers": ["default"], "level": level},
    }
    logging.config.dictConfig(config)