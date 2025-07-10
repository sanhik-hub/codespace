# editor/code_editor.py

from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QFont

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        # Font
        font = QFont('Courier', 12)
        self.setFont(font)
        self.setMarginsFont(font)

        # Line numbers
        font_metrics = self.fontMetrics()
        self.setMarginWidth(0, font_metrics.width("0000") + 6)
        self.setMarginLineNumbers(0, True)

        # Syntax highlighting
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)

        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor("#e8f2fe")
