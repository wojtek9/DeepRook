from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QPlainTextEdit
from src.logger.AppLogger import AppLogger, LogLevel
from datetime import datetime


class LogView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.app_logger = AppLogger()
        self.app_logger.new_msg.connect(self._write_to_log)

        self.main_layout = QVBoxLayout(self)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.main_layout.addWidget(self.log_view)

        # AppLogger.verbose("VERBOSE")
        # AppLogger.debug("DEBUG")
        # AppLogger.info("INFO")
        # AppLogger.warn("WARN")
        # AppLogger.error("ERROR")

    def _write_to_log(self, log_type: LogLevel, msg: str):
        color, level, spaces = self._get_log_styles(log_type)
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        full_msg = f"[{current_time} {level}{spaces}] -- {msg}"
        self.log_view.appendHtml(f"<pre><font color='{color}' style='font-size:15px;'>{full_msg}</font></pre>")

    @staticmethod
    def _get_log_styles(log_type: LogLevel) -> tuple:
        match log_type:
            case LogLevel.VERBOSE:
                color = "#888888"  # Gray
                level = "VERBOSE"
                spaces = ""
            case LogLevel.DEBUG:
                color = "#4682B4"  # Blue
                level = "DEBUG"
                spaces = "  "
            case LogLevel.INFO:
                color = "#37d60f"  # Green
                level = "INFO"
                spaces = "   "
            case LogLevel.WARN:
                color = "#E3B505"  # Yellow
                level = "WARNING"
                spaces = ""
            case LogLevel.ERROR:
                color = "#D72638"  # Red
                level = "ERROR"
                spaces = "  "
            case _:
                color = "#4682B4"  # Blue
                level = "DEBUG"
                spaces = "  "

        return color, level, spaces
