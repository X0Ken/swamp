from PyQt4 import QtGui, QtCore

from swamp import log
from swamp.models import Device
from swamp.windows.create_new import Window as CreateWindow

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

        create_btn = QtGui.QPushButton('Create')
        create_btn.clicked.connect(self.create_clicked)

        select_btn = QtGui.QPushButton('Select')
        select_btn.clicked.connect(self.select_clicked)

        cancel_btn = QtGui.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(create_btn)
        hbox.addWidget(select_btn)
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
        logger.debug("DeviceSelect select button clicked")
        self.parent().device = self.list_widget.currentItem().device
        self.close()

    def create_clicked(self):
        logger.debug("create new button clicked")
        create = CreateWindow(self)
        create.show()
