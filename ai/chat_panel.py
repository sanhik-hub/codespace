# ai/chat_panel.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ai_engines.gpt4free import GPT4FreeEngine

class ChatWorker(QThread):
    result = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        self.ai = GPT4FreeEngine()

    def run(self):
        response = self.ai.ask(self.prompt)
        self.result.emit(response)

class ChatPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(400)
        self.setWindowTitle("AI Assistant")

        layout = QVBoxLayout(self)

        self.chat_display = QTextBrowser()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Send")

        self.send_button.clicked.connect(self.send_prompt)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)

    def send_prompt(self):
        prompt = self.input_field.text().strip()
        if not prompt:
            return
        self.chat_display.append(f"<b>You:</b> {prompt}")
        self.input_field.clear()

        self.worker = ChatWorker(prompt)
        self.worker.result.connect(self.show_response)
        self.worker.start()

    def show_response(self, response):
        self.chat_display.append(f"<b>AI:</b> {response}")
