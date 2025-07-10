# ui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox,
    QTextEdit, QSplitter, QWidget, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from editor.code_editor import CodeEditor
from ai.chat_panel import ChatPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Code Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.chat_panel = ChatPanel()

        # Layout: code editor + chat assistant
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.chat_panel)
        splitter.setSizes([800, 400])

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

        self.init_menu()
        self.new_tab()

    def init_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction("New File", self)
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)

        open_action = QAction("Open File", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save File", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def new_tab(self):
        editor = CodeEditor()
        self.tabs.addTab(editor, "Untitled")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            editor = CodeEditor()
            editor.setPlainText(content)
            self.tabs.addTab(editor, path.split("/")[-1])

    def save_file(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, QTextEdit):
            path, _ = QFileDialog.getSaveFileName(self, "Save File")
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(current_widget.toPlainText())
                QMessageBox.information(self, "Saved", "File saved successfully.")
