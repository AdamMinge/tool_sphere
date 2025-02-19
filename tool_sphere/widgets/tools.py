from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton

from tool_sphere.delegates import ToolsSidebarDelegate


class ToolsSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.__is_expanded = True

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.__toggle_button = QPushButton("☰")
        self.__toggle_button.setFixedHeight(40)
        self.__toggle_button.clicked.connect(self.__toggle_sidebar)
        self.layout.addWidget(self.__toggle_button)

        self.__list_view = QListView()
        self.__list_view.setItemDelegate(
            ToolsSidebarDelegate(self.__is_sidebar_expanded)
        )
        self.__list_view.setUniformItemSizes(True)
        self.__list_view.setIconSize(QSize(24, 24))
        self.__list_view.clicked.connect(self.__on_item_clicked)
        self.layout.addWidget(self.__list_view)

        self.setFixedWidth(200)

    def set_model(self, model):
        self.__list_view.setModel(model)

    def __is_sidebar_expanded(self):
        return self.__is_expanded

    def __toggle_sidebar(self):
        self.__is_expanded = not self.__is_expanded
        self.setFixedWidth(200 if self.__is_expanded else 60)
        self.__toggle_button.setText("←" if self.__is_expanded else "☰")

    def __on_item_clicked(self, index):
        pass
