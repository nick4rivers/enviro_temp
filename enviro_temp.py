# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EnviroTemp
                                 A QGIS plugin
 Environmental temperature monitoring data management
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-09-13
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Nick Weber
        email                : nick4rivers@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
# Initialize Qt resources from file resources.py
from .resources import *

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsDataSourceUri,
    QgsMarkerSymbol
    )

from qgis.utils import iface

# Import the code for the DockWidget
from .enviro_temp_dockwidget import EnviroTempDockWidget
import os.path


class EnviroTemp:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EnviroTemp_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Enviro Temp')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EnviroTemp')
        self.toolbar.setObjectName(u'EnviroTemp')

        #print "** INITIALIZING EnviroTemp"

        self.pluginIsActive = False
        self.dockwidget = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EnviroTemp', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/enviro_temp/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING EnviroTemp"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD EnviroTemp"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Enviro Temp'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING EnviroTemp"

            # RUNS WHEN: When plugin is loaded but before the dockwidget is loaded.
            QMessageBox.information(self.dockwidget, "Runs when loaded", "This should run each time the plugin is loaded, but before the dockwidget loads")
            
            # TODO: Check for the database connect before much of anything else....

            # tables to be added from the db, and their geom column
            tables = [
                {'table_name':'projects', 'table_geom': ''},
                {'table_name':'sites', 'table_geom': 'geom'},
                {'table_name':'deployments', 'table_geom': ''},
                {'table_name':'measurements', 'table_geom': ''},
                {'table_name':'site_status', 'table_geom': ''}
            ]

            # Check for a group, add it if it is not there
            tree_root = QgsProject.instance().layerTreeRoot()
            if tree_root.findGroup('Enviro-Temp') is None:
                temperature_group = tree_root.addGroup('Enviro-Temp')

            current_layers = []
            for layer in QgsProject.instance().mapLayers().values():
                current_layers.append(layer.name())
            
            # Create uri connection
            uri = QgsDataSourceUri()
            # set host name, port, database name, username and password
            uri.setConnection("localhost", "5432", "enviro_temp", "postgres", "mykiss28")

            # check if the layer is there and add the layer if not
            for table in tables:
                if table['table_name'] not in current_layers:
                    uri.setDataSource ("public", table['table_name'], table['table_geom'])
                    add_layer = QgsVectorLayer(uri.uri(False), table['table_name'], "postgres")
                    QgsProject.instance().addMapLayer(add_layer, False)
                    temperature_group.addLayer(add_layer)

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = EnviroTempDockWidget()


            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

            # RUNS WHEN: After the dock widget is shown.
            # So, if all goes well...

            # Set some constants
            map_canvas = iface.mapCanvas()

            # TODO: Fix the zoom to the sites layer
            sites_layer = QgsProject.instance().mapLayersByName('sites')[0]
            # map_canvas.setExtent(sites_layer.extent())
            iface.setActiveLayer(sites_layer)
            sites_layer.selectAll()
            map_canvas.zoomToSelected()
            sites_layer.removeSelection()

            # TODO: Symbolize and label the sites layer?
                # TODO: Figure out why the layer symbology in the tree doesn't change when symbolized.
            sites_symbol = QgsMarkerSymbol.createSimple({
                'name': 'circle',
                'color': '#0189ff',
                'size': 4
                })
            sites_layer.renderer().setSymbol(sites_symbol)
            sites_layer.triggerRepaint()

            # TODO: Label the sites