from PyQt4 import QtGui, QtCore

from swamp import log
from swamp import models

logger = log.get_logger()


class Window(QtGui.QDialog):
    name = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

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
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(300, 150)

    def select_clicked(self):
        logger.debug("DeviceSelect select button clicked")
        name = unicode(self.name.text())
        device = models.Device(name)
        device.save()
        self.close()
