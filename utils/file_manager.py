from PyQt5.QtWidgets import QFileDialog, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QFileInfo

class FileManager:
    def __init__(self, main_window):
        self.main = main_window

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self.main, "Open File")
        if path:
            self.open_file(path)

    def open_file(self, path):
        for i in range(self.main.editor_tabs.count()):
            if self.main.editor_tabs.tabText(i) == QFileInfo(path).fileName():
                self.main.editor_tabs.setCurrentIndex(i)
                return

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        editor = QTextEdit()
        editor.setPlainText(content)
        editor.setFont(QFont("Consolas", 11))
        self.main.editor_tabs.addTab(editor, QFileInfo(path).fileName())
        self.main.editor_tabs.setCurrentWidget(editor)

    def save_current_tab(self):
        editor = self.main.editor_tabs.currentWidget()
        if not editor:
            return

        index = self.main.editor_tabs.currentIndex()
        filename = self.main.editor_tabs.tabText(index)

        path, _ = QFileDialog.getSaveFileName(self.main, "Save File", filename)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            self.main.editor_tabs.setTabText(index, QFileInfo(path).fileName())

    def save_as(self):
        self.save_current_tab()

    def new_file(self):
        editor = QTextEdit()
        editor.setFont(QFont("Consolas", 11))
        self.main.editor_tabs.addTab(editor, "Untitled")
        self.main.editor_tabs.setCurrentWidget(editor)
