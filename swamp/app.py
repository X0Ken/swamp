import signal
import sys

from PyQt4 import QtGui

from swamp import log
from swamp import utils
from swamp.models import DB
from swamp.utils import CONF
from swamp.utils import load_i18n
from swamp.windows.window_switch import WindowsSwitch

logger = log.get_logger()


def signal_term_handler(signal, frame):
    sys.exit(0)


def app():
    signal.signal(signal.SIGTERM, signal_term_handler)
    log.setup()
    logger.info("App start")

    logger.info("Load config")
    kwargs = utils.convert_args(sys.argv)
    CONF.load(kwargs)

    logger.info("Create DB")
    db = DB()
    db.create_tables()

    logger.info("Load i18n")
    load_i18n()

    logger.info("Start Window")
    app = QtGui.QApplication(sys.argv)
    win = WindowsSwitch()
    win.run()
