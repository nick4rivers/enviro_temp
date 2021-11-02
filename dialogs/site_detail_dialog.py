import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import *

from qgis.core import QgsProject, QgsFeature

DIALOG_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'site_detail.ui'))


class SiteDetailDialog(QDialog, DIALOG_CLASS):
    def __init__(self):
        super(SiteDetailDialog, self).__init__()
        self.setupUi(self)
    
        # populate the site status combo box
        self.site_status_table = QgsProject.instance().mapLayersByName('site_status')[0]
        self.comboBox_site_status
        for status in self.site_status_table.getFeatures():
            self.comboBox_site_status.addItem(status['site_status_name'], status['site_status_id'])
