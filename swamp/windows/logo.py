from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from swamp import log
from swamp.utils import _
from swamp.windows.ui import BigPushButton, LogoLabel
from swamp.windows.ui import WindowsBase

logger = log.get_logger()


class LogoWindow(WindowsBase):
    no_selected_err_msg = _('No device selected!')

    def __init__(self, parent=None):
        super(LogoWindow, self).__init__(parent)
        self.setStyleSheet('QDialog {background-image: url(img/logo.jpg)}'
                           '')

        vbox = QtGui.QVBoxLayout()

        logo_lable = LogoLabel(_("Excitation Winding Inter-turn Short "
                                 "Circuit Test"))
        logo_lable.setAlignment(Qt.AlignCenter)
        logo_lable.setStyleSheet('color: orange;font-size: 65pt;')
        vbox.addWidget(logo_lable)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        login_btn = BigPushButton(_('Start'))
        login_btn.setStyleSheet('QPushButton {font-size: 40pt;}')
        login_btn.clicked.connect(self.close)
        hbox.addWidget(login_btn)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

