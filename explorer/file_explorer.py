# explorer/file_explorer.py

import os
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog
from PyQt5.QtCore import QDir

class FileExplorer(QTreeView):
    def __init__(self, main_window, path=QDir.currentPath()):
        super().__init__()
        self.main_window = main_window

        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(path))

        self.doubleClicked.connect(self.open_file)

    def open_file(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            editor = self.main_window.tabs.widget(self.main_window.tabs.currentIndex())
            editor.setText(content)
            self.main_window.tabs.setTabText(self.main_window.tabs.currentIndex(), os.path.basename(path))

    def open_new_folder(self):
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder:
            self.model.setRootPath(folder)
            self.setRootIndex(self.model.index(folder))
