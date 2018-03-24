import subprocess

from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox

from swamp.utils import _
from swamp import log


logger = log.get_logger()


class WindowsBase(QtGui.QDialog):
    with_out_close = True
    full_window = True

    def __init__(self, *args, **kwargs):
        super(WindowsBase, self).__init__(*args, **kwargs)
        if self.full_window:
            self.showFullScreen()

    def close(self):
        if self.with_out_close:
            win = self.parent()
            win.go_home()
            self.accept()
        else:
            super(WindowsBase, self).close()


class EditWindowsBase(WindowsBase):
    full_window = False

    def __init__(self, *args, **kwargs):
        super(EditWindowsBase, self).__init__(*args, **kwargs)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(170, (screen.height() - size.height()) / 2)
        
        try:
            logger.debug("run matchbox-keyboard")
            self.keyboard = subprocess.Popen(['matchbox-keyboard',])
        except Exception as e:
            logger.warning(e)

    def closeEvent(self, evnt):
        self.close()
    
    def close(self):
        logger.debug("kill matchbox-keyboard")
        self.close_keyboard()
        super(EditWindowsBase, self).close()

    def close_keyboard(self):
        if self.keyboard:
            self.keyboard.kill()
            self.keyboard = None


class BigLabel(QtGui.QLabel):
    def __init__(self, *args, **kwargs):
        super(BigLabel, self).__init__(*args, **kwargs)
        self.setStyleSheet('QLabel {font-size: 30pt;}')


class BigLineEdit(QtGui.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(BigLineEdit, self).__init__(*args, **kwargs)
        self.setStyleSheet('QLineEdit {font-size: 30pt;}')


class LogoLabel(QtGui.QLabel):
    def __init__(self, *args, **kwargs):
        super(LogoLabel, self).__init__(*args, **kwargs)
        self.setStyleSheet('QLabel {font-size: 40pt;}')


class BigPushButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(BigPushButton, self).__init__(*args, **kwargs)
        self.setStyleSheet('QPushButton {font-size: 30pt;}')


class SuperButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(SuperButton, self).__init__(*args, **kwargs)
        self.setStyleSheet('QPushButton {font-size: 30pt; '
                           'background-color: orange;'
                           'padding: 1em 0em 1em 0em; '
                           'border-radius: 30px;}')


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
