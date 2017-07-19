import json

import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas

from swamp.windows.device_select import Window as SelectWindow
from swamp import log
from swamp import models
from swamp import exception

logger = log.get_logger()


class MainWindow(QtGui.QMainWindow):
    _device = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Device Detail")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        btn_layout = QtGui.QVBoxLayout()

        select_btn = QtGui.QPushButton('Select Device')
        select_btn.clicked.connect(self.select_btn_click)
        btn_layout.addWidget(select_btn)

        check_btn = QtGui.QPushButton('Check Device')
        check_btn.clicked.connect(self.check_btn_click)
        btn_layout.addWidget(check_btn)

        history_btn = QtGui.QPushButton('Historical Data')
        history_btn.clicked.connect(self.history_btn_click)
        btn_layout.addWidget(history_btn)

        exit_btn = QtGui.QPushButton('Exit')
        exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(exit_btn)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.canvas)
        layout.addStretch(1)
        layout.addLayout(btn_layout)

        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(layout)

        self.statusBar().showMessage("Please select device.")

        self.showFullScreen()

    def select_btn_click(self):
        logger.debug("select_btn_click")
        select_device = SelectWindow(self)
        select_device.show()

    def history_btn_click(self):
        logger.debug("history_btn_click")

    def check_btn_click(self):
        logger.debug("check_btn_click")

        if not self._device:
            QMessageBox.warning(
                self, 'Message', "You need to select device!",
                QMessageBox.Yes, QMessageBox.Yes)
            return

        try:
            info = models.CheckInfo.get_new(self._device.id)
        except exception.DataSourceGetError:
            QMessageBox.warning(
                self, 'Message', "Data source error",
                QMessageBox.Yes, QMessageBox.Yes)
            return

        ax = self.figure.add_subplot(111)
        ax.hold(True)
        ax.plot(json.loads(info.data), '.-')
        self.canvas.draw()

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value
        self.statusBar().showMessage("Device: %s" % value.name)
