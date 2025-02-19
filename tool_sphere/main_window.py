from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QSizePolicy,
    QHBoxLayout,
    QStackedWidget,
)

from tool_sphere import ToolsSidebar, ToolsModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("ToolSphere")
        self.resize(800, 600)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.__tools = ToolsModel(
            plugins_dir="/home/adam/Documents/projects/tool_sphere/.dist/plugins"
        )

        self.__sidebar = ToolsSidebar()
        self.__sidebar.set_model(self.__tools)

        self.__stacked_widget = QStackedWidget()

        self.__main_layout = QHBoxLayout(central_widget)
        self.__main_layout.addWidget(self.__sidebar)
        self.__main_layout.addWidget(self.__stacked_widget)
