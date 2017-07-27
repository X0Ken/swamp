from PyQt4 import QtGui, QtCore

from swamp import log
from swamp.models import Device
from swamp.windows.create_new import Window as CreateWindow
from swamp.windows.ui import PushButton

logger = log.get_logger()


class DeviceListWidgetItem(QtGui.QListWidgetItem):
    device = None


class Window(QtGui.QDialog):
    list_widget = None

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle("Device Select")

        list_widget = QtGui.QListWidget()
        self.list_widget = list_widget

        select_btn = PushButton('Select')
        select_btn.clicked.connect(self.select_clicked)

        delete_btn = PushButton('Delete')
        delete_btn.clicked.connect(self.delete_clicked)

        create_btn = PushButton('Create')
        create_btn.clicked.connect(self.create_clicked)

        cancel_btn = PushButton('Cancel')
        cancel_btn.clicked.connect(self.close)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(select_btn)
        hbox.addWidget(create_btn)
        hbox.addWidget(delete_btn)
        hbox.addWidget(cancel_btn)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(list_widget)
        vbox.addLayout(hbox)

        self.reload_device()
        self.setLayout(vbox)

    def reload_device(self):
        logger.debug("Reload device list")
        self.list_widget.clear()
        devices = Device.get_all()
        for device in devices:
            dev = DeviceListWidgetItem()
            dev.setText(device.name)
            dev.device = device
            self.list_widget.addItem(dev)

    def select_clicked(self):
        logger.debug("Select device button clicked")
        self.parent().device = self.list_widget.currentItem().device
        self.close()

    def create_clicked(self):
        logger.debug("Create new device button clicked")
        create = CreateWindow(self)
        create.exec_()

    def delete_clicked(self):
        logger.debug("Delete device button clicked")
        device = self.list_widget.currentItem().device
        logger.info("Delete device %s" % device.name)
        device.destroy()
        self.reload_device()
