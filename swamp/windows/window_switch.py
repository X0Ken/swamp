from PyQt4 import QtGui

from swamp.windows.compare_select import CompareSelectWindow
from swamp.windows.create_new import Window as CreateWindow
from swamp.windows.device_check import DeviceCheck
from swamp.windows.device_compare import DeviceCompare
from swamp.windows.device_infos import DeviceInfos
from swamp.windows.device_select import DeviceSelectWindow
from swamp.windows.save_info import SaveDeviceInfoWindow


class WindowsSwitch(QtGui.QDialog):
    next_win = None
    kwargs = None
    running = True

    def __init__(self):
        super(WindowsSwitch, self).__init__()
        self.next_win = DeviceSelectWindow
        self.kwargs = {}

    def run(self):
        while self.running:
            win = self.next_win(parent=self, **self.kwargs)
            self.running = win.exec_()

    def go_home(self):
        self.next_win = DeviceSelectWindow
        self.kwargs = {}

    def go_device_check(self, device):
        self.next_win = DeviceCheck
        self.kwargs = {
            'device': device
        }

    def go_compare_select(self, device):
        self.next_win = CompareSelectWindow
        self.kwargs = {
            'device': device
        }

    def go_compare_device(self, device, info, info2):
        self.next_win = DeviceCompare
        self.kwargs = {
            'device': device,
            'info': info,
            'info2': info2,
        }

    def go_create_device(self):
        self.next_win = CreateWindow
        self.kwargs = {}

    def go_manager_device(self, device):
        self.next_win = DeviceInfos
        self.kwargs = {
            'device': device
        }

    def go_save_device_info(self, info):
        self.next_win = SaveDeviceInfoWindow
        self.kwargs = {
            'info': info
        }