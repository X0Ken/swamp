import json

from PyQt4 import QtGui
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QMessageBox
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import \
    NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from swamp import exception
from swamp import log
from swamp import models
from swamp.utils import _
from swamp.windows.asyncio import coroutine, AsyncTask
from swamp.windows.ui import BigPushButton, BigLabel, MiddleLabel
from swamp.windows.ui import WindowsBase
from swamp.windows.ui import warring

logger = log.get_logger()


class DeviceCheck(WindowsBase):
    device = None
    _info = None
    no_selected_err_msg = _('No device info!')

    def __init__(self, parent=None, device=None):
        super(DeviceCheck, self).__init__(parent)
        self.device = device
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

        self.setLayout(layout)

        self.set_device()

    def init_menu_area(self):
        # button grid begin
        btn_grid = QtGui.QVBoxLayout()

        get_info_btn = BigPushButton(_('Start test'))
        get_info_btn.clicked.connect(self.check_btn_click)
        btn_grid.addWidget(get_info_btn)
        self.get_info_btn = get_info_btn

        save_info_btn = BigPushButton(_('Save Info'))
        save_info_btn.clicked.connect(self.save_info_click)
        btn_grid.addWidget(save_info_btn)
        save_info_btn.setDisabled(True)
        self.save_info_btn = save_info_btn

        exit_btn = BigPushButton(_('Go Back'))
        exit_btn.clicked.connect(self.close)
        btn_grid.addWidget(exit_btn)

        return btn_grid

    def init_info_area(self):
        # label grid
        label_grid = QtGui.QGridLayout()
        name_lable = MiddleLabel(_("Name:"))
        device_name = MiddleLabel("")
        label_grid.addWidget(name_lable, 0, 0)
        label_grid.addWidget(device_name, 0, 1)
        self.device_name = device_name

        max_current_label = MiddleLabel(_("Max current value:"))
        max_current = MiddleLabel("")
        label_grid.addWidget(max_current_label, 2, 0)
        label_grid.addWidget(max_current, 2, 1)
        self.max_current = max_current

        max_time_label = MiddleLabel(_("Max time:"))
        max_time = MiddleLabel("")
        label_grid.addWidget(max_time_label, 3, 0)
        label_grid.addWidget(max_time, 3, 1)
        self.max_time = max_time

        return label_grid

    def check(self, device_id, max_i, max_t):
        info = models.CheckInfo.get_new(device_id, max_i, max_t)
        return info

    @coroutine
    def check_btn_click(self, arg):
        logger.debug("Check device btn clicked.")
        self.get_info_btn.setDisabled(True)
        try:
            max_t = self.device.get_max_time(default=200)
            max_i = self.device.get_max_current(default=40.0)
            info = yield AsyncTask(self.check, self.device.id, max_i, max_t)
        except exception.DataSourceGetError:
            QMessageBox.warning(
                self, _('Message'), _("Data source error"),
                QMessageBox.Yes, QMessageBox.Yes)
            return
        except Exception as e:
            logger.error(e)
            QMessageBox.warning(
                self, _('Error'), _("Unknow Error"),
                QMessageBox.Yes, QMessageBox.Yes)
            return

        data = json.loads(info.data)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot([t for t, v in data], [v for t, v in data], '.-')
        self.canvas.draw()
        self._info = info
        self.get_info_btn.setDisabled(False)
        self.save_info_btn.setDisabled(False)

    def save_info_click(self):
        logger.debug("save device info button clicked")
        if self._info:
            win = self.parent()
            win.go_save_device_info(self._info)
            self.accept()
        else:
            warring(self, self.no_selected_err_msg)


    def set_device(self):
        device = self.device
        logger.debug("load device %s" % device.name)
        self.device_name.setText(device.name)
        max_time = device.get_setting(models.MAX_TIME, default="")
        self.max_time.setText(_("%s ms") % max_time)
        max_current = device.get_setting(models.MAX_CURRENT, default="")
        self.max_current.setText(_("%s A") % max_current)
