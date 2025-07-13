from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
import os

class TerminalWebView(QWebEngineView):
    def __init__(self, shell_type="bash"):
        super().__init__()

        html_path = os.path.abspath("static/terminal.html")
        url = QUrl.fromLocalFile(html_path).toString() + f"?shell={shell_type}"
        self.load(QUrl(url))

        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
