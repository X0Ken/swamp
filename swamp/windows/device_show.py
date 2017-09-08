import json

import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as \
    FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as \
    NavigationToolbar

from swamp.diagnosis import diagnosis
from swamp.windows.device_select import Window as SelectWindow
from swamp.windows.device_infos import Window as InfoWindow
from swamp import log
from swamp import models
from swamp import exception
from swamp.windows.ui import PushButton

logger = log.get_logger()


class MainWindow(QtGui.QMainWindow):
    _device = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(_("Device Detail"))
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        label_grid = self.init_info_area()

        btn_grid = self.init_menu_area()

        # right layout
        right_layout = QtGui.QVBoxLayout()
        right_layout.addStretch(1)
        right_layout.addLayout(label_grid)
        right_layout.addStretch(1)
        right_layout.addLayout(btn_grid)

        # left layout
        left_layout = QtGui.QVBoxLayout()
        left_layout.addWidget(self.toolbar)
        left_layout.addWidget(self.canvas)

        # window layout
        layout = QtGui.QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(layout)

        self.statusBar().showMessage(_("Please select device."))

        self.showMaximized()

    def init_menu_area(self):
        # button grid begin
        btn_grid = QtGui.QVBoxLayout()
        select_btn = PushButton(_('Select Device'))
        select_btn.clicked.connect(self.select_btn_click)
        btn_grid.addWidget(select_btn)

        check_btn = PushButton(_('Get New Device Info'))
        check_btn.clicked.connect(self.check_btn_click)
        btn_grid.addWidget(check_btn)

        check_btn = PushButton(_('Delete Line'))
        check_btn.clicked.connect(self.delete_line_btn_click)
        btn_grid.addWidget(check_btn)

        exit_btn = PushButton(_('Exit'))
        exit_btn.clicked.connect(self.close)
        btn_grid.addWidget(exit_btn)

        return btn_grid

    def init_info_area(self):
        # label grid
        label_grid = QtGui.QGridLayout()
        name_lable = QtGui.QLabel(_("Name:"))
        device_name = QtGui.QLabel("")
        label_grid.addWidget(name_lable, 0, 0)
        label_grid.addWidget(device_name, 0, 1)
        self.device_name = device_name

        health_label = QtGui.QLabel(_("Diagnosis:"))
        device_health = QtGui.QLabel("")
        label_grid.addWidget(health_label, 1, 0)
        label_grid.addWidget(device_health, 1, 1)
        self.device_health = device_health

        max_current_label = QtGui.QLabel(_("Max current value:"))
        max_current = QtGui.QLabel("")
        label_grid.addWidget(max_current_label, 2, 0)
        label_grid.addWidget(max_current, 2, 1)
        self.max_current = max_current

        max_time_label = QtGui.QLabel(_("Max time:"))
        max_time = QtGui.QLabel("")
        label_grid.addWidget(max_time_label, 3, 0)
        label_grid.addWidget(max_time, 3, 1)
        self.max_time = max_time

        compare_time_label = QtGui.QLabel(_("Compare time:"))
        compare_time = QtGui.QLabel("")
        label_grid.addWidget(compare_time_label, 4, 0)
        label_grid.addWidget(compare_time, 4, 1)
        self.compare_time = compare_time

        return label_grid

    def select_btn_click(self):
        logger.debug("Select device button clicked")
        select_device = SelectWindow(self)
        select_device.exec_()

    def load_all_data(self):
        logger.debug("Load device history data button clicked.")
        try:
            infos = models.CheckInfo.get_all_by_device(self._device.id)
            self.figure.clear()
            self.ax = self.figure.add_subplot(111)

            compare_time = self._device.get_compare_time(default=0)
            max_time = self._device.get_max_time(default=0)

            vline = False
            for info in infos:
                data = json.loads(info.data)
                self.ax.plot([t for t, v in data], [v for t, v in data],
                             '.-', label=str(info))
                if max_time and compare_time:
                    index = compare_time * len(data) / max_time
                    if not vline:
                        self.ax.axvline(compare_time, linestyle='--')
                        vline = True
                    self.ax.axhline(data[index][1], linestyle='--')

            self.ax.legend(bbox_to_anchor=(0.02, 0.98), loc=2,
                           borderaxespad=0.)
            self.canvas.draw()
        except exception.DataSourceGetError:
            QMessageBox.warning(
                self, _('Message'), _("Data source error"),
                QMessageBox.Yes, QMessageBox.Yes)
        self._diagnosis()

    def check_btn_click(self):
        logger.debug("Check device btn clicked.")

        if not self._device:
            QMessageBox.warning(
                self, _('Message'), _("You need to select device!"),
                QMessageBox.Yes, QMessageBox.Yes)
            return

        try:
            max_t = self._device.get_max_time(default=200)
            max_i = self._device.get_max_current(default=40.0)
            models.CheckInfo.get_new(self._device.id, max_i, max_t)
        except exception.DataSourceGetError:
            QMessageBox.warning(
                self, _('Message'), _("Data source error"),
                QMessageBox.Yes, QMessageBox.Yes)
            return

        self.load_all_data()

    def delete_line_btn_click(self):
        logger.debug("Delete line button clicked")

        if not self._device:
            QMessageBox.warning(
                self, _('Message'), _("You need to select device!"),
                QMessageBox.Yes, QMessageBox.Yes)
            return

        infos = InfoWindow(device=self.device, parent=self)
        infos.exec_()

    def _diagnosis(self):
        info_number = models.CheckInfo.get_all_by_device(
            self._device.id).count()
        if info_number < 2:
            self.device_health.setText(_("Insufficient data"))
            return

        if diagnosis(self._device):
            self.device_health.setText(_("Health"))
        else:
            self.device_health.setText(_("Fault"))

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value
        self.device_name.setText(value.name)
        max_time = self._device.get_setting(models.MAX_TIME, default="")
        self.max_time.setText(_("%s ms") % max_time)
        compare_time = self._device.get_setting(models.COMPARE_TIME,
                                                default="")
        self.compare_time.setText(_("%s ms") % compare_time)
        max_current = self._device.get_setting(models.MAX_CURRENT, default="")
        self.max_current.setText(_("%s A") % max_current)
        self.load_all_data()
        self.statusBar().showMessage(_("Device: %s") % value.name)
