import logging

logger = logging.getLogger("contact_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler("contact.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)