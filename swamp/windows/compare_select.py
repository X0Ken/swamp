from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox

from swamp import log
from swamp.utils import _
from swamp.windows.ui import BigPushButton
from swamp.windows.ui import InfoListWidgetItem
from swamp.windows.ui import ListWidget
from swamp.windows.ui import WinidowsBase

logger = log.get_logger()


class CompareSelectWindow(WinidowsBase):
    device = None

    def __init__(self, parent=None, device=None):
        super(CompareSelectWindow, self).__init__(parent)
        self.device = device
        layout = QtGui.QHBoxLayout()

        info_list_widget = ListWidget()
        layout.addWidget(info_list_widget)
        self.info_list_widget = info_list_widget

        com_info_list_widget = ListWidget()
        layout.addWidget(com_info_list_widget)
        self.com_info_list_widget = com_info_list_widget

        btns = QtGui.QVBoxLayout()

        compare_btn = BigPushButton(_('Compate Infos'))
        compare_btn.clicked.connect(self._on_compare_click)
        btns.addWidget(compare_btn)

        back_btn = BigPushButton(_('Go Back'))
        back_btn.clicked.connect(self.close)
        btns.addWidget(back_btn)

        layout.addLayout(btns)
        self.setLayout(layout)
        self._load_info()

    def _load_info(self):
        logger.debug("Reload device info list")
        infos = self.device.check_infos

        self.info_list_widget.clear()
        for info in infos:
            item = InfoListWidgetItem()
            item.setText(info.name)
            item.info = info
            self.info_list_widget.addItem(item)
        item = self.info_list_widget.itemAt(0, 0)
        if item:
            item.setSelected(True)

        self.com_info_list_widget.clear()
        for info in infos:
            item = InfoListWidgetItem()
            item.setText(info.name)
            item.info = info
            self.com_info_list_widget.addItem(item)
        item = self.info_list_widget.itemAt(1, 0)
        if item:
            item.setSelected(True)

    def _on_compare_click(self):
        win = self.parent()
        info = self._get_select_info(self.info_list_widget)
        if not info:
            self._warrning_no_info(_("Plesae Select first info"))
            return
        info2 = self._get_select_info(self.com_info_list_widget)
        if not info2:
            self._warrning_no_info(_("Plesae Select second info"))
            return
        if info.id == info2.id:
            self._warrning_no_info(_("Plesae Select different info"))
            return
        win.go_compare_device(self.device, info, info2)
        self.accept()

    def _get_select_info(self, list_widget):
        infos = list_widget.selectedItems()
        info = None
        if infos:
            info = infos[0].info
        return info

    def _warrning_no_info(self, msg):
        QMessageBox.warning(
            self, _('Message'), msg,
            QMessageBox.Yes, QMessageBox.Yes)
