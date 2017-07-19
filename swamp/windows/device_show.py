import json

import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as \
    FigureCanvas

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

        # label grid
        label_grid = QtGui.QGridLayout()
        name_lable = QtGui.QLabel("Name:")
        device_name = QtGui.QLabel("")
        label_grid.addWidget(name_lable, 0, 0)
        label_grid.addWidget(device_name, 0, 1)
        self.device_name = device_name

        health_label = QtGui.QLabel("Health:")
        device_health = QtGui.QLabel("")
        label_grid.addWidget(health_label, 1, 0)
        label_grid.addWidget(device_health, 1, 1)
        self.device_health = device_health

        # button grid begin
        btn_grid = QtGui.QGridLayout()

        select_btn = QtGui.QPushButton('Select Device')
        select_btn.clicked.connect(self.select_btn_click)
        btn_grid.addWidget(select_btn, 0, 0)

        check_btn = QtGui.QPushButton('Check Device')
        check_btn.clicked.connect(self.check_btn_click)
        btn_grid.addWidget(check_btn, 0, 1)

        history_btn = QtGui.QPushButton('Historical Data')
        history_btn.clicked.connect(self.history_btn_click)
        btn_grid.addWidget(history_btn, 1, 0)

        exit_btn = QtGui.QPushButton('Exit')
        exit_btn.clicked.connect(self.close)
        btn_grid.addWidget(exit_btn,  1, 1)

        # right layout
        right_layout = QtGui.QVBoxLayout()
        right_layout.addStretch(1)
        right_layout.addLayout(label_grid)
        right_layout.addStretch(1)
        right_layout.addLayout(btn_grid)

        # window layout
        layout = QtGui.QHBoxLayout()
        layout.addStretch(2)
        layout.addWidget(self.canvas)
        layout.addStretch(1)
        layout.addLayout(right_layout)

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
        if not self._device:
            QMessageBox.warning(
                self, 'Message', "You need to select device!",
                QMessageBox.Yes, QMessageBox.Yes)
            return
        try:
            infos = models.CheckInfo.get_all_by_device(self._device.id)
            self.figure.clear()
            self.canvas.draw()
            for info in infos:
                ax = self.figure.add_subplot(111)
                ax.hold(True)
                ax.plot(json.loads(info.data), '.-')
                self.canvas.draw()
        except exception.DataSourceGetError:
            QMessageBox.warning(
                self, 'Message', "Data source error",
                QMessageBox.Yes, QMessageBox.Yes)
            return

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
        self.device_name.setText(value.name)
        self.figure.clear()
        self.canvas.draw()
        self.statusBar().showMessage("Device: %s" % value.name)
