import os
import sys
import platform
import subprocess
import threading

from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QFileDialog, QAction, QPlainTextEdit, QWidget,
    QVBoxLayout, QDockWidget, QTreeView, QFileSystemModel, QInputDialog,
    QToolBar, QMessageBox, QToolButton
)
from PyQt5.QtCore import Qt, QModelIndex, QSize, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Code Editor with xterm.js")
        self.resize(1400, 900)

        self.terminal_count = 0
        self.process = None
        self.terminals = []

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.output_console = QPlainTextEdit()
        self.output_console.setFont(QFont("Courier New", 10))
        self.output_console.setReadOnly(True)

        self.setup_output_dock()
        self.setup_file_explorer()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_terminal_dock()

        self.add_new_editor_tab()
        self.start_terminal_backend()

    # ---------------- Backend Startup ----------------

    def start_terminal_backend(self):
        node_path = "node"
        if platform.system() == "Windows":
            node_path += ".exe"

        backend_path = os.path.abspath("server.js")

        def run():
            try:
                subprocess.Popen(
                    [node_path, backend_path],
                    cwd=os.path.dirname(backend_path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True
                )
                print(" Terminal backend started.")
            except Exception as e:
                print(" Failed to start terminal backend:", e)

        threading.Thread(target=run, daemon=True).start()

    # ---------------- UI ----------------

    def setup_output_dock(self):
        dock = QDockWidget("Output", self)
        dock.setWidget(self.output_console)
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def setup_file_explorer(self):
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setColumnWidth(0, 300)  # wider column for filename
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(0, self.tree.header().ResizeToContents)

        self.tree.setHeaderHidden(False)
        self.tree.header().setStretchLastSection(True)
        self.tree.doubleClicked.connect(self.open_file_from_tree)

        self.folder_dock = QDockWidget("Explorer", self)
        self.folder_dock.setWidget(self.tree)
        self.folder_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.folder_dock)

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.make_action("New File", "Ctrl+N", self.add_new_editor_tab))
        file_menu.addAction(self.make_action("Open File", "Ctrl+O", self.open_file_dialog))
        file_menu.addAction(self.make_action("Open Folder", None, self.open_folder_dialog))
        file_menu.addAction(self.make_action("Save", "Ctrl+S", self.save_current_file))
        file_menu.addAction(self.make_action("Save As", "Ctrl+Shift+S", self.save_current_file_as))

        view_menu = menubar.addMenu("View")
        toggle_dark = QAction("Toggle Dark Mode", self)
        toggle_dark.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(toggle_dark)

        terminal_menu = menubar.addMenu("Terminal")
        terminal_menu.addAction(self.make_action("New Terminal Tab", "Ctrl+Shift+T", self.create_terminal_tab))

    def setup_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(22, 22))

        self.run_btn = QToolButton()
        self.run_btn.setText("▶ Run")
        self.run_btn.clicked.connect(self.run_current_file)
        self.toolbar.addWidget(self.run_btn)

        self.term_btn = QToolButton()
        self.term_btn.setText("➕ Terminal")
        self.term_btn.clicked.connect(self.create_terminal_tab)
        self.toolbar.addWidget(self.term_btn)

        open_folder_btn = QToolButton()
        open_folder_btn.setText("📁")
        open_folder_btn.setToolTip("Open Folder")
        open_folder_btn.clicked.connect(self.open_folder_dialog)
        self.toolbar.addWidget(open_folder_btn)

        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.style_toolbar_buttons()

    def style_toolbar_buttons(self):
        dark = self.is_dark_mode()
        style = (
            "QToolButton { background-color: #0f0; color: black; }"
            if dark else
            "QToolButton { background-color: #333; color: white; }"
        )
        self.run_btn.setStyleSheet(style)
        self.term_btn.setStyleSheet(style)

    def make_action(self, name, shortcut, slot):
        action = QAction(name, self)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        return action

    # ---------------- Terminal (QWebEngineView Tabbed) ----------------

    def setup_terminal_dock(self):
        self.terminal_tab_widget = QTabWidget()
        self.terminal_tab_widget.setTabsClosable(True)
        self.terminal_tab_widget.tabCloseRequested.connect(self.close_terminal_tab)

        self.terminal_dock = QDockWidget("Terminal", self)
        self.terminal_dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.terminal_dock.setWidget(self.terminal_tab_widget)
        self.terminal_dock.resize(600, 300)
        self.addDockWidget(Qt.RightDockWidgetArea, self.terminal_dock)

    def create_terminal_tab(self):
        term_view = QWebEngineView()
        html_path = os.path.abspath("web/index.html")
        term_view.load(Qt.QUrl.fromLocalFile(html_path))

        index = self.terminal_tab_widget.addTab(term_view, f"Terminal {self.terminal_count + 1}")
        self.terminal_tab_widget.setCurrentIndex(index)
        self.terminal_count += 1

    def close_terminal_tab(self, index):
        self.terminal_tab_widget.removeTab(index)

    # ---------------- File Management ----------------

    def add_new_editor_tab(self):
        editor = QPlainTextEdit()
        editor.setFont(QFont("Courier New", 11))
        editor.setObjectName("")
        editor.textChanged.connect(self.auto_save)
        self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentWidget(editor)

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            self.open_file_in_editor(path)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder and os.path.isdir(folder):
            self.model.setRootPath(folder)
            self.tree.setRootIndex(self.model.index(folder))

    def open_file_from_tree(self, index: QModelIndex):
        if not self.model.isDir(index):
            self.open_file_in_editor(self.model.filePath(index))

    def open_file_in_editor(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.output_console.appendPlainText(str(e))
            return
        editor = QPlainTextEdit()
        editor.setPlainText(content)
        editor.setFont(QFont("Courier New", 11))
        editor.setObjectName(path)
        editor.textChanged.connect(self.auto_save)
        self.tabs.addTab(editor, os.path.basename(path))
        self.tabs.setCurrentWidget(editor)

    def save_current_file(self):
        editor = self.tabs.currentWidget()
        path = editor.objectName()
        if not path:
            return self.save_current_file_as()
        with open(path, "w", encoding="utf-8") as f:
            f.write(editor.toPlainText())

    def save_current_file_as(self):
        editor = self.tabs.currentWidget()
        path, _ = QFileDialog.getSaveFileName(self, "Save As")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            editor.setObjectName(path)
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(path))

    def auto_save(self):
        editor = self.tabs.currentWidget()
        path = editor.objectName()
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())

    # ---------------- Run ----------------

    def run_current_file(self):
        editor = self.tabs.currentWidget()
        if not isinstance(editor, QPlainTextEdit):
            return

        path = editor.objectName()
        if not path or not os.path.isfile(path):
            QMessageBox.warning(self, "Run", "Please save the file before running.")
            return

        self.save_current_file()

        self.process = subprocess.Popen(
            [sys.executable, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        self.output_console.clear()
        self.output_console.appendPlainText(f"Running: {path}\n")

        threading.Thread(target=self.read_process_output, daemon=True).start()

    def read_process_output(self):
        for line in self.process.stdout:
            self.output_console.appendPlainText(line)

    # ---------------- View / Theme ----------------

    def toggle_dark_mode(self):
        dark = not self.is_dark_mode()
        if dark:
            self.setStyleSheet("""
                QMainWindow { background-color: #121212; color: white; }
                QPlainTextEdit, QTreeView { background-color: #1e1e1e; color: white; }
                QMenuBar, QMenu, QTabWidget::pane { background-color: #1e1e1e; color: white; }
            """)
        else:
            self.setStyleSheet("")
        self.style_toolbar_buttons()

    def is_dark_mode(self):
        return "background-color: #121212" in self.styleSheet()
