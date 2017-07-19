import sys

from PyQt4 import QtGui

from swamp import log
from swamp.models import DB
from swamp.windows.device_show import MainWindow

logger = log.get_logger()


def app():
    log.setup()
    logger.debug("App start")

    logger.debug("Create DB")
    db = DB()
    db.create_tables()

    logger.debug("Start Window")
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    return app.exec_()
