from PySide6.QtCore import QStandardPaths


def get_temp_dir():
    return QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation)
