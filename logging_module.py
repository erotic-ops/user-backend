import logging
import socket
from logging.handlers import SysLogHandler
from os import environ

from logtail import LogtailHandler

# Initialising the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Papertrail Logging
HOST_ADDRESS = environ.get("PAPERTRAIL_HOST_ADDRESS")
HOST_PORT = int(environ.get("PAPERTRAIL_HOST_PORT"))


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


syslog = SysLogHandler(address=(HOST_ADDRESS, HOST_PORT))
syslog.addFilter(ContextFilter())

log_format = "{asctime} | {hostname} | {filename} | {funcName} | {lineno} | {message}"
formatter = logging.Formatter(log_format, style="{")
syslog.setFormatter(formatter)
logger.addHandler(syslog)

# BetterStack Logging
SOURCE_TOKEN = environ.get("BETTERSTACK_SOURCE_TOKEN")
handler = LogtailHandler(source_token=SOURCE_TOKEN)
logger.addHandler(handler)

# Stream Logging
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

print("User form backend logging started")
