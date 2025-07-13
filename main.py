import os
import sys
import subprocess
import threading

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def start_terminal_backend():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    backend_dir = os.path.join(base_dir, "terminal-backend/terminal-frontend")
    node_exe = os.path.join(base_dir, "node", "node.exe")
    server_js = os.path.join(backend_dir, "server.js")

    if not os.path.exists(server_js):
        print("server.js not found in /terminal-backend")
        return

    command = [node_exe, "server.js"] if os.path.exists(node_exe) else ["node", "server.js"]

    def launch():
        try:
            subprocess.Popen(
                command,
                cwd=backend_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            print("Terminal backend started on port 3000")
        except Exception as e:
            print("Terminal backend failed:", e)

    threading.Thread(target=launch, daemon=True).start()


def main():
    app = QApplication(sys.argv)
    start_terminal_backend()
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
