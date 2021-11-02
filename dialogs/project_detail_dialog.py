import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import *

DIALOG_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'project_detail.ui'))


class ProjectDetailDialog(QDialog, DIALOG_CLASS):
    def __init__(self):
        super(ProjectDetailDialog, self).__init__()
        self.setupUi(self)    
