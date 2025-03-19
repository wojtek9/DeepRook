from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenuBar, QMenu, QApplication

from src.gui.menu.settings.SettingsWindow import SettingsWindow


class MenuBar(QMenuBar):
    def __init__(self, app: QApplication, parent=None):
        super().__init__(parent)

        self.app = app

        # Settings Menu
        self.settings_window = SettingsWindow(app=app, parent=self)
        settings_menu = QMenu("", self)
        settings_menu.setIcon(QIcon(":/icn/menu_settings_icon"))
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        self.addMenu(settings_menu)

        # Help Menu
        help_menu = QMenu("", self)
        help_menu.setIcon(QIcon(":/icn/menu_help_icon"))
        help_action = QAction("About", self)
        help_action.triggered.connect(self.show_about)
        help_menu.addAction(help_action)
        self.addMenu(help_menu)

    def open_settings(self):
        self.settings_window.setModal(True)
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def show_about(self):
        print("Help menu clicked")
