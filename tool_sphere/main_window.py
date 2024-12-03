from PySide6.QtWidgets import QMainWindow, QSizePolicy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("ToolSphere")
        self.resize(800, 600)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
