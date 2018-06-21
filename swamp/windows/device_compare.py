# -*- coding: utf-8 -*-

import json

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import \
    NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from swamp import log
from swamp.utils import _
from swamp.windows.ui import BigPushButton, BigLabel, MiddleLabel
from swamp.windows.ui import WindowsBase

logger = log.get_logger()


class DeviceCompare(WindowsBase):
    device = None
    infos = None

    def __init__(self, parent=None, device=None, infos=None):
        super(DeviceCompare, self).__init__(parent)
        self.device = device
        self.infos = infos
        self._init_ui()
        self._draw_infos(infos)
        self.set_device(device)

    def _draw_infos(self, infos):
        self.ax = self.figure.add_subplot(111)
        for info in infos:
            self._draw_info(info)
        if len(self.infos) > 1:
            self.calculator_t(infos)
        self.ax.legend()
        self.canvas.draw()

    def calculator_t(self, infos):
        ts = map(lambda info: json.loads(info.data)[-1][0], infos)
        self.t_value.setText("{} ms".format(max(ts)-min(ts)))

    def _init_ui(self):
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

    def init_menu_area(self):
        # button grid begin
        btn_grid = QtGui.QVBoxLayout()

        exit_btn = BigPushButton(_('Go Back'))
        exit_btn.clicked.connect(self.close)
        btn_grid.addWidget(exit_btn)

        return btn_grid

    def init_info_area(self):
        # label grid
        label_grid = QtGui.QGridLayout()
        name_lable = MiddleLabel(_("Device Name:"))
        device_name = MiddleLabel("")
        self.device_name = device_name
        label_grid.addWidget(name_lable, 0, 0)
        label_grid.addWidget(device_name, 0, 1)

        if len(self.infos) > 1:
            t_lable = MiddleLabel(_("dt:"))
            t_value = MiddleLabel("")
            label_grid.addWidget(t_lable, 1, 0)
            label_grid.addWidget(t_value, 1, 1)
            self.t_value = t_value
        else:
            tname_lable = MiddleLabel(_("Test Name:"))
            tname_value = MiddleLabel(self.infos[0].name)
            label_grid.addWidget(tname_lable, 1, 0)
            label_grid.addWidget(tname_value, 1, 1)

        return label_grid

    def _draw_info(self, info):
        data = json.loads(info.data)
        self.ax.plot([t for t, v in data], [v for t, v in data],
                     '.-', label=str(info))

    def set_device(self, device):
        logger.debug("load device %s" % device.name)
        self.device_name.setText(device.name)
