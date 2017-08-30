import sys

from PyQt4 import QtGui

from swamp import log
from swamp.models import DB
from swamp.windows.device_show import MainWindow
from swamp.utils import load_i18n

logger = log.get_logger()


def app():
    log.setup()
    logger.info("App start")

    logger.info("Create DB")
    db = DB()
    db.create_tables()

    logger.info("Load i18n")
    load_i18n()

    logger.info("Start Window")
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    return app.exec_()
