from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtGui import QIcon


class SidebarModel(QAbstractListModel):
    def __init__(self, items):
        super().__init__()
        self._items = items

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None

        item = self._items[index.row()]

        if role == Qt.DisplayRole:
            return item["name"]
        elif role == Qt.DecorationRole:
            return QIcon(item["icon"])
        return None
