import logging
import logging.handlers


def setup():
    log_file = 'app.log'

    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s ' \
          '%(message)s'
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
