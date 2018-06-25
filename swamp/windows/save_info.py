import subprocess

from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox

from swamp import exception
from swamp import log
from swamp import models
from swamp.utils import _
from swamp.windows.ui import BigPushButton, warring, BigLabel, BigLineEdit
from swamp.windows.ui import EditWindowsBase

logger = log.get_logger()


class SaveDeviceInfoWindow(EditWindowsBase):
    _info = None
    keyboard = None

    def __init__(self, parent=None, info=None):
        super(SaveDeviceInfoWindow, self).__init__(parent)
        self._info = info
        self.setWindowTitle(_("Save Device info"))

        grid = QtGui.QGridLayout()

        name_label = BigLabel(_("Name:"))
        self.name = BigLineEdit()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name, 0, 1)

        select_btn = BigPushButton(_('Submit'))
        select_btn.clicked.connect(self.select_clicked)

        cancel_btn = BigPushButton(_('Cancel'))
        cancel_btn.clicked.connect(self.close)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(select_btn)
        hbox.addWidget(cancel_btn)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def select_clicked(self):
        logger.debug("Device info save button clicked")
        name = unicode(self.name.text())
        if not name:
            warring(self, _("You need to input a name!"))
            return
        if models.CheckInfo.name_exist(self._info.device_id, name):
            warring(self, _("Please inpute another name"))
            return
        self._info.name = name
        self._info.save()
        self.close_keyboard()
        win = self.parent()
        win.go_home()
        self.accept()

