from qgis.PyQt.QtWidgets import QMenu
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QIcon

class ContextMenu(QMenu):
    MENUS =   {
        'ADD_ASSESSMENT': (
            'New Riverscape Assessment',
            ':/plugins/qris_toolbar/Detrend.png'
        ),
        'ADD_DESIGN': (
            'New Low-Tech Design',
            ':/plugins/qris_toolbar/qris_design_new.png'
        )
    }


    def addAction(self, lookup: str, slot: pyqtSlot = None, enabled=True):
        if lookup not in self.MENUS:
            raise Exception('Menu not found')
        action_text = self.MENUS[lookup]
        action = super().addAction(QIcon(action_text[1]), action_text[0])
        action.setEnabled(enabled)

        if slot is not None:
            action.triggered.connect(slot)
