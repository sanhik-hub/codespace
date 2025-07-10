# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Optional: load theme
    try:
        with open("themes/dark.qss") as f:
            app.setStyleSheet(f.read())
    except Exception:
        pass

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
