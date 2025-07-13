# AI Code Editor

🧠 Offline-installable, Python-based AI-powered code editor with project building from prompts.

## Features
- Syntax-highlighted code editor (like VS Code)
- Free AI assistant (no API keys)
- Explain / refactor / debug / generate code
- Create full projects from plain text prompts
- Plugin system + themes
- Terminal and updater coming soon

## Run It

```bash
pip install -r requirements.txt
python main.py

codespace/
├── main.py                        ✅ Starts app + terminal backend
├── node/node.exe                 ✅ Node runtime (portable)
├── terminal-backend/server.js    ✅ WebSocket backend for terminal
├── static/
│   └── terminal.html             ✅ xterm.js frontend (webview)
├── ui/
│   └── main_window.py            ✅ Main window UI (this file)
├── utils/
│   ├── terminal_webview.py       ✅ Terminal browser with WebSocket hook
│   └── terminal_tab_manager.py   ✅ Wraps terminal views into tabs
