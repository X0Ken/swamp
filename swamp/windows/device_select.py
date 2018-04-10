import subprocess
import os

from PyQt4 import QtGui

from swamp import log
from swamp.models import Device
from swamp.utils import CONF
from swamp.utils import _
from swamp.windows.compare_select import CompareSelectWindow
from swamp.windows.device_infos import DeviceInfos
from swamp.windows.ui import MenuBigPushButton
from swamp.windows.ui import BigPushButton
from swamp.windows.ui import SuperButton
from swamp.windows.ui import DeviceListWidgetItem
from swamp.windows.ui import WindowsBase
from swamp.windows.ui import ListWidget
from swamp.windows.ui import ask
from swamp.windows.ui import warring

logger = log.get_logger()


class MenuWindow(WindowsBase):
    devices = None
    with_out_close = False
    no_selected_err_msg = _('No device selected!')

    def __init__(self, parent=None):
        super(MenuWindow, self).__init__(parent)
        
        hbox = QtGui.QHBoxLayout()

        size = self.geometry()
        pic = QtGui.QLabel()
        pixmap = QtGui.QPixmap(os.getcwd() + "/img/logo.jpg")
        logger.debug("Widows size: %d %d" % (size.width(), size.height()))
        pixmap = pixmap.scaled(size.width() / 4 * 2.5 * 2, size.height() * 2.4)
        pic.setPixmap(pixmap)
        hbox.addWidget(pic)

        vbox = QtGui.QVBoxLayout()

        select_btn = SuperButton(_('Start the test'))
        select_btn.clicked.connect(self.on_check_clicked)
        vbox.addWidget(select_btn)

        create_btn = MenuBigPushButton(_('New test equipment'))
        create_btn.clicked.connect(self.on_create_clicked)
        vbox.addWidget(create_btn)

        delete_btn = MenuBigPushButton(_('Remove test equipment'))
        delete_btn.clicked.connect(self.on_delete_clicked)
        vbox.addWidget(delete_btn)

        compare_device_btn = MenuBigPushButton(_('Analysis of test data'))
        compare_device_btn.clicked.connect(self.on_compare_device)
        vbox.addWidget(compare_device_btn)

        manager_btn = MenuBigPushButton(_('Management test data'))
        manager_btn.clicked.connect(self.on_manager_clicked)
        vbox.addWidget(manager_btn)

        if not CONF.with_exit:
            exit_btn = MenuBigPushButton(_('Power Off'))
            exit_btn.clicked.connect(self.on_power_off)
            vbox.addWidget(exit_btn)
        else:
            exit_btn = MenuBigPushButton(_('Exit System'))
            exit_btn.clicked.connect(self.close)
            vbox.addWidget(exit_btn)

        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def on_compare_device(self):
        self.infos = None
        win = self.parent()
        device = self._get_select_device()
        if device:
            com_win = CompareSelectWindow(self, device)
            com_win.exec_()
        if self.infos:
            win.go_compare_device(device, self.infos)
            self.accept()

    def _get_select_device(self):
        select_win = DeviceSelectWindow(self)
        select_win.exec_()
        device = None
        if self.devices:
            device = self.devices[0].device
            logger.debug("Select device %s" % device.name)
        self.devices = None
        return device

    def on_check_clicked(self):
        logger.debug("Select device button clicked")
        win = self.parent()
        device = self._get_select_device()
        if device:
            win.go_device_check(device)
            self.accept()

    def on_create_clicked(self):
        logger.debug("Create new device button clicked")
        win = self.parent()
        win.go_create_device()
        self.accept()

    def on_manager_clicked(self):
        logger.debug("Manager device button clicked")
        self.info = None
        device = self._get_select_device()
        if device:
            manager_win = DeviceInfos(self, device)
            manager_win.exec_()
        if self.info:
            win = self.parent()
            win.go_compare_device(device, [self.info])
            self.accept()

    def on_delete_clicked(self):
        logger.debug("Delete device button clicked")
        device = self._get_select_device()
        if device:
            if not ask(self, _("Are you sure to delete it?")):
                return
            logger.info("Delete device %s" % device.name)
            device.destroy()

    def on_power_off(self):
        if not ask(self, _("Are you sure to power off?")):
            return
        self.close()
        # pcmanfm
        subprocess.Popen(['killall', '-9', 'pcmanfm'])
        subprocess.Popen(['sudo', 'shutdown', "-t", "now"])


class DeviceSelectWindow(WindowsBase):
    single = True
    full_window = False
    center_window = True
    with_out_close = False

    def __init__(self, parent=None, single=True):
        super(DeviceSelectWindow, self).__init__(parent)
        self.setWindowTitle(_("Select Device"))
        self.single = single
        vbox = QtGui.QVBoxLayout()
        list_widget = ListWidget()
        vbox.addWidget(list_widget)
        self.list_widget = list_widget

        hbox = QtGui.QHBoxLayout()
        select_btn = BigPushButton(_('Select'))
        select_btn.clicked.connect(self.select_clicked)
        hbox.addWidget(select_btn)

        cancel_btn = BigPushButton(_('Cancel'))
        cancel_btn.clicked.connect(self.close)
        hbox.addWidget(cancel_btn)

        vbox.addLayout(hbox)
        self.setLayout(vbox)
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

    def _get_select_device(self):
        devices = self.list_widget.selectedItems()
        self.parent().devices = devices

    def select_clicked(self):
        logger.debug("Device select button clicked")
        self._get_select_device()
        self.accept()

