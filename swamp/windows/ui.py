from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox

from swamp.utils import _


class FullWinidowsBase(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(FullWinidowsBase, self).__init__(*args, **kwargs)
        self.showFullScreen()


class SwitchWindowsBase(QtGui.QDialog):
    def close(self):
        win = self.parent()
        win.go_home()
        self.accept()


class WinidowsBase(FullWinidowsBase, SwitchWindowsBase):
    pass


class BigPushButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(BigPushButton, self).__init__(*args, **kwargs)
        self.setStyleSheet('QPushButton {font-size: 30pt;}')


class DeviceListWidgetItem(QtGui.QListWidgetItem):
    device = None


class InfoListWidgetItem(QtGui.QListWidgetItem):
    info = None


class ListWidget(QtGui.QListWidget):
    def __init__(self, *args, **kwargs):
        super(ListWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet('QListWidget {font-size: 18pt;}')


def warring(parent, msg):
    QMessageBox.warning(
        parent, _('Message'), msg,
        QMessageBox.Yes, QMessageBox.Yes)


def ask(parent, msg):
    ret = QMessageBox.warning(
        parent, _('Message'), msg,
        QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
    return ret == QMessageBox.Yes
