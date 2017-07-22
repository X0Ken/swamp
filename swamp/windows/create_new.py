from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox

from swamp import log
from swamp import models

logger = log.get_logger()


class Window(QtGui.QDialog):
    name = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle("Create New Device")

        grid = QtGui.QGridLayout()

        name_label = QtGui.QLabel("name:")
        name = QtGui.QLineEdit()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(name, 0, 1)
        self.name = name

        select_btn = QtGui.QPushButton('Submit')
        select_btn.clicked.connect(self.select_clicked)

        cancel_btn = QtGui.QPushButton('Cancel')
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
        logger.debug("Device select button clicked")
        name = unicode(self.name.text())
        if not name:
            QMessageBox.warning(
                self, 'Message', "You need to input a name!",
                QMessageBox.Yes, QMessageBox.Yes)
            return
        if models.Device.name_exist(name):
            QMessageBox.warning(
                self, 'Message', "This name has been used. "
                                 "Pleas input another!",
                QMessageBox.Yes, QMessageBox.Yes)
            return
        device = models.Device(name)
        device.save()
        logger.info("New device %s created" % device.name)
        self.parent().reload_device()
        self.close()
