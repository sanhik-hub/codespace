from PyQt5.QtWidgets import QTextEdit

class OutputConsole(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def write(self, text):
        self.append(text)
