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
    power_time = None
    keyboard = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle(_("Create New Device"))

        grid = QtGui.QGridLayout()

        name_label = QtGui.QLabel(_("Name:"))
        self.name = QtGui.QLineEdit()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name, 0, 1)

        power_time_label = QtGui.QLabel(_("Power time(s):"))
        self.power_time = QtGui.QLineEdit()
        grid.addWidget(power_time_label, 1, 0)
        grid.addWidget(self.power_time, 1, 1)

        set_current_label = QtGui.QLabel(_("Set current value(A):"))
        self.set_current = QtGui.QLineEdit()
        grid.addWidget(set_current_label, 2, 0)
        grid.addWidget(self.set_current, 2, 1)

        fault_judgment_label = QtGui.QLabel(_("Fault judgment value(%):"))
        self.fault_judgment = QtGui.QLineEdit()
        grid.addWidget(fault_judgment_label, 3, 0)
        grid.addWidget(self.fault_judgment, 3, 1)

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

    def check_power_time(self, power_time):
        try:
            power_time = int(power_time)
        except ValueError:
            raise exception.InvalidError(_("Power time must be a number!"))
        if power_time < 1:
            raise exception.InvalidError(_("Power time must bigger than 1!"))

    def check_set_current(self, set_current):
        try:
            set_current = int(set_current)
        except ValueError:
            raise exception.InvalidError(_("Current must be a number!"))
        if set_current < 1:
            raise exception.InvalidError(_("Current must bigger than 1!"))

    def check_fault_judgment(self, fault_judgment):
        try:
            fault_judgment = int(fault_judgment)
        except ValueError:
            raise exception.InvalidError(_("Fault judgment value must be a number!"))
        if fault_judgment < 1 or fault_judgment > 99:
            raise exception.InvalidError(_("Fault judgment value must between "
                                           "1 and 99!"))

    def select_clicked(self):
        logger.debug("Device select button clicked")
        name = unicode(self.name.text())
        power_time = unicode(self.power_time.text())
        set_current = unicode(self.set_current.text())
        fault_judgment = unicode(self.fault_judgment.text())
        try:
            self.check_name(name)
            self.check_power_time(power_time)
            self.check_set_current(set_current)
            self.check_fault_judgment(fault_judgment)
        except exception.InvalidError as e:
            QMessageBox.warning(
                self, _('Message'), e.message,
                QMessageBox.Yes, QMessageBox.Yes)
            return

        device = models.Device(name)
        device.save()
        device.settings.append(
            models.DeviceSetting(device_id=device.id, key=models.POWER_TIME,
                                 value=unicode(self.power_time.text()))
        )
        device.settings.append(
            models.DeviceSetting(device_id=device.id, key=models.SET_CURRENT,
                                 value=unicode(self.set_current.text()))
        )
        device.settings.append(
            models.DeviceSetting(device_id=device.id,
                                 key=models.FAULT_JUDGMENT,
                                 value=unicode(self.fault_judgment.text()))
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
