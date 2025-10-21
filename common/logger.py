import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "test.log")

logger = logging.getLogger("pytest_ginchat_api")
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2*1024*1024, backupCount=5, encoding="utf-8")
file_handler.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(fmt)
file_handler.setFormatter(fmt)

if not logger.handlers:
    logger.addHandler(console)
    logger.addHandler(file_handler)
