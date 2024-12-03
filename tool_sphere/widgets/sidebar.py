from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton

from tool_sphere.delegates import SidebarDelegate


class Sidebar(QWidget):
    def __init__(self, model):
        super().__init__()
        self.is_expanded = True

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedHeight(40)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.layout.addWidget(self.toggle_button)

        self.list_view = QListView()
        self.list_view.setModel(model)
        self.list_view.setItemDelegate(SidebarDelegate(self.is_sidebar_expanded))
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QSize(24, 24))
        self.list_view.clicked.connect(self.on_item_clicked)
        self.layout.addWidget(self.list_view)

        self.setFixedWidth(200)

    def is_sidebar_expanded(self):
        return self.is_expanded

    def toggle_sidebar(self):
        self.is_expanded = not self.is_expanded
        self.setFixedWidth(200 if self.is_expanded else 60)
        self.toggle_button.setText("←" if self.is_expanded else "☰")

    def on_item_clicked(self, index):
        pass
