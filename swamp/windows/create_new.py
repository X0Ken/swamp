import subprocess

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox

from swamp import log
from swamp import models
from swamp.models import DB
from swamp.windows.ui import PushButton
from swamp import exception

logger = log.get_logger()


class Window(QtGui.QDialog):
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

        max_time_label = QtGui.QLabel(_("Max T(ms):"))
        self.max_time = QtGui.QLineEdit()
        grid.addWidget(max_time_label, 2, 0)
        grid.addWidget(self.max_time, 2, 1)

        compare_time_label = QtGui.QLabel(_("Compare T(ms):"))
        self.compare_time = QtGui.QLineEdit()
        grid.addWidget(compare_time_label, 3, 0)
        grid.addWidget(self.compare_time, 3, 1)

        select_btn = PushButton(_('Submit'))
        select_btn.clicked.connect(self.select_clicked)

        cancel_btn = PushButton(_('Cancel'))
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
            self.keyboard = subprocess.Popen(['matchbox-keyboard',
                                              '-s',
                                              '50'])
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

    def check_max_time(self, max_time):
        try:
            max_time = int(max_time)
        except ValueError:
            raise exception.InvalidError(_("Max time must be a number!"))
        if max_time <= 0:
            raise exception.InvalidError(_("Max time must more than 0!"))

    def check_compare_time(self, compare_time, max_time):
        try:
            compare_time = int(compare_time)
        except ValueError:
            raise exception.InvalidError(_("Compare time must be a number!"))
        if compare_time <= 0 or compare_time > int(max_time):
            raise exception.InvalidError(_("Compare time must more than 0,"
                                           " and less then Max time!"))

    def select_clicked(self):
        logger.debug("Device select button clicked")
        name = unicode(self.name.text())
        max_time = unicode(self.max_time.text())
        compare_time = unicode(self.compare_time.text())
        max_current = unicode(self.max_current.text())
        try:
            self.check_name(name)
            self.check_max_time(max_time)
            self.check_compare_time(compare_time, max_time)
            self.check_max_current(max_current)
        except exception.InvalidError as e:
            QMessageBox.warning(
                self, _('Message'), e.message,
                QMessageBox.Yes, QMessageBox.Yes)
            return

        device = models.Device(name)
        device.save()
        device.settings.append(
            models.DeviceSetting(device_id=device.id, key=models.MAX_TIME,
                                 value=unicode(max_time))
        )
        device.settings.append(
            models.DeviceSetting(device_id=device.id, key=models.COMPARE_TIME,
                                 value=unicode(compare_time))
        )
        device.settings.append(
            models.DeviceSetting(device_id=device.id,
                                 key=models.MAX_CURRENT,
                                 value=unicode(max_current))
        )
        DB().commit()

        logger.info("New device %s created" % device.name)
        self.parent().reload_device()
        self.close()

    def close(self):
        logger.debug("kill matchbox-keyboard")
        if self.keyboard:
            self.keyboard.kill()
        super(Window, self).close()
