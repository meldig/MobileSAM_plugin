from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import QgsApplication
from .processing_provider.provider import Provider


class MobileSamPlugin:
    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        self.provider = None

    def initProcessing(self):
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(QIcon("testplug:icon.png"),
                              "Mobile SAM Plugin",
                              self.iface.mainWindow())
        self.action.setObjectName("testAction")
        self.action.setWhatsThis("Configuration for mobile sam plugin")
        self.action.setStatusTip("This is status tip")
        self.action.triggered.connect(self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Mobile SAM Plugin", self.action)

        # connect to signal renderComplete which is emitted when canvas
        # rendering is done
        self.iface.mapCanvas().renderComplete.connect(self.renderTest)
        self.initProcessing()

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&Mobile SAM Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

        # disconnect form signal of the canvas
        self.iface.mapCanvas().renderComplete.disconnect(self.renderTest)
        QgsApplication.processingRegistry().removeProvider(self.provider)

    def run(self):
        # create and show a configuration dialog or something similar
        print("MobileSamPlugin: run called!")

    def renderTest(self, painter):
        # use painter for drawing to map canvas
        print("MobileSamPlugin: renderTest called!")