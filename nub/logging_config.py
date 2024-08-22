import logging
import logging.config
from datetime import datetime as date_time
from logging import getLogger, Handler
from sqlite3 import connect


class DatabaseHandler(Handler):
    def __init__(self, db_file: str = "summarizer_log.db"):
        super().__init__()
        self.db_file = db_file
        self.db_file = connect(self.db_file)
        self.db_file.execute(
            "CREATE TABLE IF NOT EXISTS logs (date TEXT, "
            "time TEXT, lvl INTEGER, lvl_name TEXT, msg TEXT, "
            "logger TEXT, lineno INTEGER)"
        )

    def emit(self, record):
        """
        Conditionally emit the specified logging record.

        Emission depends on filters which may have been added to the handler.
        Wrap the actual emission of the record with acquisition/release of
        the I/O thread lock. Returns whether the filter passed the record for
        emission.
        """
        self.db_file.execute(
            'INSERT INTO logs VALUES (:1,:2,:3,:4, :5, :6, :7)', (
                date_time.now().strftime('%A, the %d of %B, %Y'),
                date_time.now().strftime('%I:%M %p'),
                record.levelno,
                record.levelname,
                record.msg,
                record.name,
                record.lineno
            )
        )
        self.db_file.commit()
        self.db_file.close()


def setup_logging(default_level=logging.INFO):
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'standard',
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': default_level,
        },
    }

    logging.config.dictConfig(log_config)



setup_logging()