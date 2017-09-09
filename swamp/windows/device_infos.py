from PyQt4 import QtGui, QtCore

from swamp import log
from swamp.models import CheckInfo
from swamp.windows.ui import PushButton

logger = log.get_logger()


class InfoListWidgetItem(QtGui.QListWidgetItem):
    info = None


class Window(QtGui.QDialog):
    device = None
    infos = None

    def __init__(self, parent=None, device=None):
        super(Window, self).__init__(parent)
        self.device = device

        self.setWindowTitle(_("Device Info List"))

        infos = QtGui.QListWidget()
        self.infos = infos

        delete_btn = PushButton(_('Remove'))
        delete_btn.clicked.connect(self.remove_clicked)

        cancel_btn = PushButton(_('Cancel'))
        cancel_btn.clicked.connect(self.close)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(delete_btn)
        hbox.addWidget(cancel_btn)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(infos)
        vbox.addLayout(hbox)

        self.reload_info()
        self.setLayout(vbox)

    def reload_info(self):
        logger.debug("Reload device info list")
        self.infos.clear()
        infos = self.device.check_infos
        for info in infos:
            item = InfoListWidgetItem()
            item.setText(str(info.created_at))
            item.info = info
            self.infos.addItem(item)

    def remove_clicked(self):
        logger.debug("Remove info from list")
        info = self.infos.currentItem().info
        logger.info("Delete info %s from device %s",
                    str(info), self.device.name)
        info.destroy()
        self.reload_info()

    def close(self):
        self.parent().load_all_data()
        super(Window, self).close()
