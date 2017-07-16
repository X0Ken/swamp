import logging
import logging.handlers

def setup():
    LOG_FILE = 'app.log'

    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    ch = logging.StreamHandler()
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)

    logger = logging.getLogger("app")
    logger.addHandler(handler)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

def get_logger():
    return logging.getLogger("app")