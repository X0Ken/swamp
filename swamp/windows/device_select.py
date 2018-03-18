import subprocess

from PyQt4 import QtGui

from swamp import log
from swamp.models import Device
from swamp.utils import CONF
from swamp.utils import _
from swamp.windows.ui import BigPushButton, SuperButton
from swamp.windows.ui import DeviceListWidgetItem
from swamp.windows.ui import WindowsBase
from swamp.windows.ui import ListWidget
from swamp.windows.ui import ask
from swamp.windows.ui import warring

logger = log.get_logger()


class DeviceSelectWindow(WindowsBase):
    with_out_close = False
    no_selected_err_msg = _('No device selected!')

    def __init__(self, parent=None):
        super(DeviceSelectWindow, self).__init__(parent)
        
        hbox = QtGui.QHBoxLayout()
        list_widget = ListWidget()
        hbox.addWidget(list_widget)
        self.list_widget = list_widget

        vbox = QtGui.QVBoxLayout()

        select_btn = SuperButton(_('Start the test'))
        select_btn.clicked.connect(self.on_check_clicked)
        vbox.addWidget(select_btn)

        create_btn = BigPushButton(_('New test equipment'))
        create_btn.clicked.connect(self.on_create_clicked)
        vbox.addWidget(create_btn)

        delete_btn = BigPushButton(_('Remove test equipment'))
        delete_btn.clicked.connect(self.on_delete_clicked)
        vbox.addWidget(delete_btn)

        compare_device_btn = BigPushButton(_('Analysis of test data'))
        compare_device_btn.clicked.connect(self.on_compare_device)
        vbox.addWidget(compare_device_btn)

        manager_btn = BigPushButton(_('Management test data'))
        manager_btn.clicked.connect(self.on_manager_clicked)
        vbox.addWidget(manager_btn)

        if not CONF.with_exit:
            exit_btn = BigPushButton(_('Power Off'))
            exit_btn.clicked.connect(self.on_power_off)
            vbox.addWidget(exit_btn)
        else:
            exit_btn = BigPushButton(_('Exit System'))
            exit_btn.clicked.connect(self.close)
            vbox.addWidget(exit_btn)

        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.reload_device()

    def reload_device(self):
        logger.debug("Reload device list")
        self.list_widget.clear()
        devices = Device.get_all()
        for device in devices:
            dev = DeviceListWidgetItem()
            dev.setText(device.name)
            dev.device = device
            self.list_widget.addItem(dev)
        item = self.list_widget.itemAt(0, 0)
        if item:
            item.setSelected(True)

    def on_compare_device(self):
        win = self.parent()
        device = self._get_select_device()
        if device:
            win.go_compare_select(device)
            self.accept()
        else:
            warring(self, self.no_selected_err_msg)

    def _get_select_device(self):
        devices = self.list_widget.selectedItems()
        device = None
        if devices:
            device = devices[0].device
            logger.debug("Select device %s" % device.name)
        return device

    def on_check_clicked(self):
        logger.debug("Select device button clicked")
        win = self.parent()
        device = self._get_select_device()
        if device:
            win.go_device_check(device)
            self.accept()
        else:
            warring(self, self.no_selected_err_msg)

    def on_create_clicked(self):
        logger.debug("Create new device button clicked")
        win = self.parent()
        win.go_create_device()
        self.accept()

    def on_manager_clicked(self):
        logger.debug("Manager device button clicked")
        device = self._get_select_device()
        if device:
            win = self.parent()
            win.go_manager_device(device)
            self.accept()
        else:
            warring(self, self.no_selected_err_msg)

    def on_delete_clicked(self):
        logger.debug("Delete device button clicked")
        device = self._get_select_device()
        if device:
            if not ask(self, _("Are you sure to delete it?")):
                return
            logger.info("Delete device %s" % device.name)
            device.destroy()
            self.reload_device()
        else:
            warring(self, self.no_selected_err_msg)

    def on_power_off(self):
        self.close()
        subprocess.Popen(['sudo', 'shutdown', "-t", "now"])

