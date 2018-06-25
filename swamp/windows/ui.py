import subprocess

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QStyle
from PyQt4.QtCore import Qt

from swamp.utils import _
from swamp import log


logger = log.get_logger()


class WindowsBase(QtGui.QDialog):
    with_out_close = True

    def __init__(self, *args, **kwargs):
        super(WindowsBase, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

    def close(self):
        if self.with_out_close:
            win = self.parent()
            win.go_home()
            self.accept()
        else:
            super(WindowsBase, self).close()


class FullWindowsBase(WindowsBase):
    def __init__(self, *args, **kwargs):
        super(WindowsBase, self).__init__(*args, **kwargs)
        self.showFullScreen()


class EditWindowsBase(WindowsBase):

    def __init__(self, *args, **kwargs):
        super(EditWindowsBase, self).__init__(*args, **kwargs)

    def showEvent(self, QShowEvent):
        super(EditWindowsBase, self).showEvent(QShowEvent)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(),
                               QtGui.QDesktopWidget().availableGeometry()))
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
            subprocess.Popen(['killall', '-9', 'pcmanfm'])


class AskWindows(WindowsBase):
    with_out_close = False

    def __init__(self, msg=None, *args, **kwargs):
        super(AskWindows, self).__init__(*args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        msg_lab = MiddleLabel(msg)
        vbox.addWidget(msg_lab)

        select_btn = BigPushButton(_('Submit'))
        select_btn.clicked.connect(self.select_clicked)

        cancel_btn = BigPushButton(_('Cancel'))
        cancel_btn.clicked.connect(self.close)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(select_btn)
        hbox.addWidget(cancel_btn)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def select_clicked(self):
        self.accept()


class BigLabel(QtGui.QLabel):
    def __init__(self, *args, **kwargs):
        super(BigLabel, self).__init__(*args, **kwargs)
        self.setStyleSheet('QLabel {font-size: 30pt;}')


class MiddleLabel(QtGui.QLabel):
    def __init__(self, *args, **kwargs):
        super(MiddleLabel, self).__init__(*args, **kwargs)
        self.setStyleSheet('QLabel {font-size: 16pt;}')


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


class MenuBigPushButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MenuBigPushButton, self).__init__(*args, **kwargs)
        self.setStyleSheet('QPushButton {font-size: 30pt;'
                           'padding: 30px 0px 30px 0px;}')


class SuperButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(SuperButton, self).__init__(*args, **kwargs)
        self.setStyleSheet('QPushButton {font-size: 30pt; '
                           'background-color: orange;'
                           'padding: 1em 0em 1em 0em;'
                           'border-radius: 30px;}')


class DeviceListWidgetItem(QtGui.QListWidgetItem):
    device = None


class InfoListWidgetItem(QtGui.QListWidgetItem):
    info = None


class ListWidget(QtGui.QListWidget):
    def __init__(self, *args, **kwargs):
        super(ListWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet('QListWidget {font-size: 25pt;}')


def warring(parent, msg):
    QMessageBox.warning(
        parent, _('Message'), msg,
        QMessageBox.Yes, QMessageBox.Yes)


def ask(parent, msg):
    askBox = AskWindows(msg=msg)
    ret = askBox.exec_()
    logger.debug("Select %s" % ret)
    return ret
