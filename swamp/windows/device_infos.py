from PyQt4 import QtGui

from swamp import log
from swamp.utils import _
from swamp.windows.ui import BigPushButton
from swamp.windows.ui import InfoListWidgetItem
from swamp.windows.ui import ListWidget
from swamp.windows.ui import WindowsBase
from swamp.windows.ui import ask
from swamp.windows.ui import warring

logger = log.get_logger()


class DeviceInfos(WindowsBase):
    device = None
    infos = None

    def __init__(self, parent=None, device=None):
        super(DeviceInfos, self).__init__(parent)
        self.device = device

        infos = ListWidget()
        self.infos = infos

        view_btn = BigPushButton(_('View'))
        view_btn.clicked.connect(self.view_clicked)

        delete_btn = BigPushButton(_('Remove'))
        delete_btn.clicked.connect(self.remove_clicked)

        cancel_btn = BigPushButton(_('Go Back'))
        cancel_btn.clicked.connect(self.close)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        hbox.addWidget(view_btn)
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
            item.setText(info.name)
            item.info = info
            self.infos.addItem(item)

    def remove_clicked(self):
        logger.debug("Remove info from list")
        selected_infos = self.infos.selectedItems()
        if selected_infos:
            if not ask(self, _("Are you sure to delete it?")):
                return
            info = selected_infos[0].info
            logger.info("Delete info %s from device %s",
                        str(info), self.device.name)
            info.destroy()
            self.reload_info()
        else:
            warring(self, _("Info not selected"))

    def view_clicked(self):
        logger.debug("View info from list")
        selected_infos = self.infos.selectedItems()
        if selected_infos:
            info = selected_infos[0].info
            logger.info("View info %s from device %s",
                        str(info), self.device.name)
            win = self.parent()
            win.go_compare_device(self.device, [info])
            self.accept()
        else:
            warring(self, _("Info not selected"))
