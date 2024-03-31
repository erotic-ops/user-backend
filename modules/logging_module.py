"""
This module sets up a logger for the application. It uses the built-in logging
module and the LogtailHandler from the logtail module to send logs to a
remote server. It includes a custom logging filter, ContextFilter, that
adds the hostname to the log record.
"""

import logging
from logging.handlers import SysLogHandler
from os import environ
from socket import gethostname

from logtail import LogtailHandler  # type: ignore

# Initialising the logger
logger = logging.getLogger("my_application_logger")
logger.setLevel(logging.INFO)
LOG_FORMAT = "{asctime} | {hostname} | {filename} | {funcName} | {lineno} | {message}"
formatter = logging.Formatter(LOG_FORMAT, style="{")


# Papertrail Logging
class ContextFilter(logging.Filter):
    """
    A custom logging filter that adds the hostname to the log record.

    Attributes:
        hostname (str): The hostname of the system where the log record is created.
    """

    hostname = gethostname()

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Adds the hostname to the log record.

        Args:
            record (logging.LogRecord): The log record to be filtered.

        Returns:
            bool: Always returns True to allow the log record to be processed.
        """
        record.hostname = ContextFilter.hostname
        return True


syslog = SysLogHandler(address=(environ.get("PAPERTRAIL_HOST_ADDRESS", ""), int(environ.get("PAPERTRAIL_HOST_PORT", 0))))
syslog.addFilter(ContextFilter())
syslog.setFormatter(formatter)
logger.addHandler(syslog)

# BetterStack Logging
handler = LogtailHandler(source_token=environ.get("BETTERSTACK_SOURCE_TOKEN"))
logger.addHandler(handler)

print("User form backend logging started")
logger.info("User form backend logging started")
