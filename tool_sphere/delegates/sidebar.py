from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QStyledItemDelegate, QStyle


class SidebarDelegate(QStyledItemDelegate):
    def __init__(self, is_expanded_callback, parent=None):
        super().__init__(parent)
        self.is_expanded_callback = is_expanded_callback

    def paint(self, painter, option, index):
        is_expanded = self.is_expanded_callback()
        icon = index.data(Qt.DecorationRole)
        text = index.data(Qt.DisplayRole)

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        icon_rect = option.rect.adjusted(10, 10, -10, -10)
        icon.paint(painter, icon_rect, Qt.AlignVCenter | Qt.AlignLeft)

        if is_expanded:
            text_rect = option.rect.adjusted(50, 0, 0, 0)
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)

    def sizeHint(self, option, index):
        return QSize(200 if self.is_expanded_callback() else 60, 40)
