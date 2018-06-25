from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QAbstractItemView

from swamp import log
from swamp.utils import _
from swamp.windows.ui import BigPushButton
from swamp.windows.ui import InfoListWidgetItem
from swamp.windows.ui import ListWidget
from swamp.windows.ui import WindowsBase

logger = log.get_logger()


class CompareSelectWindow(WindowsBase):
    with_out_close = False
    device = None

    def __init__(self, parent=None, device=None):
        super(CompareSelectWindow, self).__init__(parent)
        self.setWindowTitle(_("Select Device info"))
        self.device = device
        layout = QtGui.QVBoxLayout()

        info_list_widget = ListWidget()
        info_list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(info_list_widget)
        self.info_list_widget = info_list_widget

        btns = QtGui.QHBoxLayout()

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

    def _on_compare_click(self):
        infos = self._get_select_infos(self.info_list_widget)
        if not infos:
            self._warrning_no_info(_("Please select at least one set of "
                                     "test data"))
        win = self.parent()
        win.infos = infos
        self.accept()

    def _get_select_infos(self, list_widget):
        info_widgets = list_widget.selectedItems()
        if info_widgets:
            infos = map(lambda w: w.info, info_widgets)
        else:
            infos = []
        return infos

    def _warrning_no_info(self, msg):
        QMessageBox.warning(
            self, _('Message'), msg,
            QMessageBox.Yes, QMessageBox.Yes)
