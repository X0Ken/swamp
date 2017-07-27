
from PyQt4 import QtGui, QtCore


class PushButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(PushButton, self).__init__(*args, **kwargs)
        self.setStyleSheet('QPushButton {font-size: 18pt;}')
