import subprocess

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox

from swamp import log
from swamp import models
from swamp.windows.ui import PushButton

logger = log.get_logger()


class Window(QtGui.QDialog):
    name = None
    keyboard = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle(_("Create New Device"))

        grid = QtGui.QGridLayout()

        name_label = QtGui.QLabel(_("Name:"))
        name = QtGui.QLineEdit()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(name, 0, 1)
        self.name = name

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

    def select_clicked(self):
        logger.debug("Device select button clicked")
        name = unicode(self.name.text())
        if not name:
            QMessageBox.warning(
                self, _('Message'), _("You need to input a name!"),
                QMessageBox.Yes, QMessageBox.Yes)
            return
        if models.Device.name_exist(name):
            QMessageBox.warning(
                self, _('Message'), _("This name has been used. "
                                      "Pleas input another!"),
                QMessageBox.Yes, QMessageBox.Yes)
            return
        device = models.Device(name)
        device.save()
        logger.info("New device %s created" % device.name)
        self.parent().reload_device()
        self.close()

    def close(self):
        logger.debug("kill matchbox-keyboard")
        if self.keyboard:
            self.keyboard.kill()
        super(Window, self).close()
