from logtail import LogtailHandler
import logging
from os import environ

SOURCE_TOKEN = environ.get("LOGS_SOURCE_TOKEN")

if SOURCE_TOKEN is None:
    print("[+] Please set the environment variable")
    exit(1)

handler = LogtailHandler(source_token=SOURCE_TOKEN)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)

logger.info("Hello World!")