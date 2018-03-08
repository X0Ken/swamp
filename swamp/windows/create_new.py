import subprocess

from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox

from swamp import exception
from swamp import log
from swamp import models
from swamp.utils import _
from swamp.windows.ui import BigPushButton
from swamp.windows.ui import SwitchWindowsBase

logger = log.get_logger()


class Window(SwitchWindowsBase):
    name = None
    max_time = None
    keyboard = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle(_("Create New Device"))

        grid = QtGui.QGridLayout()

        name_label = QtGui.QLabel(_("Name:"))
        self.name = QtGui.QLineEdit()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name, 0, 1)

        max_current_label = QtGui.QLabel(_("Max I(A):"))
        self.max_current = QtGui.QLineEdit()
        grid.addWidget(max_current_label, 1, 0)
        grid.addWidget(self.max_current, 1, 1)

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

        try:
            logger.debug("run matchbox-keyboard")
            self.keyboard = subprocess.Popen(['matchbox-keyboard',])
        except Exception as e:
            logger.warning(e)

    def check_name(self, name):
        if not name:
            raise exception.InvalidError(_("You need to input a name!"))
        if models.Device.name_exist(name):
            raise exception.InvalidError(_("This name has been used. "
                                           "Pleas input another!"))

    def check_max_current(self, max_current):
        try:
            max_current = float(max_current)
        except ValueError:
            raise exception.InvalidError(_("Max current must be a number!"))
        if max_current <= 0:
            raise exception.InvalidError(_("Max current must more than 0!"))

    def select_clicked(self):
        logger.debug("Device select button clicked")
        name = unicode(self.name.text())
        max_time = '4000'
        max_current = unicode(self.max_current.text())
        try:
            self.check_name(name)
            self.check_max_current(max_current)
        except exception.InvalidError as e:
            QMessageBox.warning(
                self, _('Message'), e.message,
                QMessageBox.Yes, QMessageBox.Yes)
            return

        device = models.Device(name)

        device.set_max_time(unicode(max_time))
        device.set_max_current(unicode(max_current))
        device.save()

        logger.info("New device %s created" % device.name)
        win = self.parent()
        win.go_home()
        self.close_keyboard()
        self.accept()

    def close(self):
        logger.debug("kill matchbox-keyboard")
        self.close_keyboard()
        win = self.parent()
        win.go_home()
        self.accept()

    def close_keyboard(self):
        if self.keyboard:
            self.keyboard.kill()
            self.keyboard = None
