import subprocess
import platform

class TerminalTabManager:
    def launch_native_terminal(self, shell_type):
        if platform.system() == "Windows":
            if shell_type == "cmd":
                subprocess.Popen("start cmd", shell=True)
            elif shell_type == "powershell":
                subprocess.Popen("start powershell", shell=True)
        elif platform.system() == "Linux":
            subprocess.Popen([shell_type])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", "Terminal"])
