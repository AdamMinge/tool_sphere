import os
import typing
import zipimport
import importlib
import dataclasses

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, Signal
from PySide6.QtGui import QIcon

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


@dataclasses.dataclasses
class Tool:
    name: str
    icon: QIcon
    widget: QWidget


class ToolsModel(QAbstractListModel):
    dataChanged = Signal()

    def __init__(self, plugins_dir: str):
        super().__init__()
        self.__items: list[Tool] = []
        self.__plugins_dir = plugins_dir
        self.__load_plugins()
        self.__start_watching()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.__items)

    def data(self, index, role) -> typing.Any:
        if not index.isValid() or not (0 <= index.row() < len(self.__items)):
            return None

        if role == Qt.DisplayRole:
            return self.get_tool_name(index)
        elif role == Qt.DecorationRole:
            return self.get_tool_icon(index)
        return None

    def get_tool_name(self, index: QModelIndex) -> typing.Optional[str]:
        item = self.get_item(index)
        return item.name if item else None

    def get_tool_icon(self, index: QModelIndex) -> typing.Optional[QIcon]:
        item = self.get_item(index)
        return item.icon if item else None

    def get_tool_widget(self, index: QModelIndex) -> typing.Optional[QWidget]:
        item = self.get_item(index)
        return item.widget if item else None

    def get_tool(self, index: QModelIndex) -> typing.Optional[Tool]:
        if 0 <= index < len(self.__items):
            return self.__items[index.row()]
        return None

    def __load_plugins(self):
        self.beginResetModel()
        self.__items.clear()

        if not os.path.isdir(self.__plugins_dir):
            self.endResetModel()
            return

        for filename in os.listdir(self.__plugins_dir):
            if filename.endswith(".zip"):
                plugin_path = os.path.join(self.__plugins_dir, filename)
                self.__items.append(self.__load_tool(plugin_path))

        self.endResetModel()

    def __start_watching(self):
        self.watcher = DirectoryWatcher(self.__plugins_dir, self.__reload_plugins)
        self.watcher.start()

    def __reload_plugins(self):
        self.load_plugins()

    def __load_tool(self, filename: str) -> typing.Optional[Tool]:
        zip_loader = zipimport.zipimporter(filename)
        module_spec = zip_loader.find_spec("plugin")
        if module_spec:
            mymodule = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(mymodule)
            return Tool(**mymodule.create_tool())
        return None


class DirectoryWatcher(FileSystemEventHandler):
    def __init__(self, directory: str, callback: callable):
        super().__init__()
        self.directory = directory
        self.callback = callback
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self, self.directory, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".zip"):
            self.callback()
