from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QFont, QColor

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        font = QFont('Consolas', 12)
        self.setFont(font)
        self.setMarginsFont(font)

        # Line numbers
        font_metrics = self.fontMetrics()
        self.setMarginWidth(0, font_metrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#2e2e2e"))
        self.setMarginsForegroundColor(QColor("#cccccc"))

        # Syntax highlighting
        lexer = QsciLexerPython()
        lexer.setFont(font)
        lexer.setColor(QColor("#ffffff"))
        lexer.setPaper(QColor("#1e1e1e"))  # Background
        lexer.setColor(QColor("#f44747"), QsciLexerPython.ClassName)
        lexer.setColor(QColor("#569cd6"), QsciLexerPython.Keyword)
        lexer.setColor(QColor("#dcdcaa"), QsciLexerPython.Comment)
        lexer.setColor(QColor("#9cdcfe"), QsciLexerPython.DoubleQuotedString)

        self.setLexer(lexer)

        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2a2a2a"))
        self.setPaper(QColor("#1e1e1e"))  # Editor background
        self.setColor(QColor("#ffffff"))  # Default text
