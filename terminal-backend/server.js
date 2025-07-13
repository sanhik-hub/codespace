
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const pty = require('node-pty');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static(path.join(__dirname, 'terminal-frontend')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'terminal-frontend', 'index.html'));
});

wss.on('connection', function (ws) {
  const shell = process.platform === 'win32' ? 'powershell.exe' : 'bash';
  const ptyProcess = pty.spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 24,
    cwd: process.env.HOME,
    env: process.env
  });

  ptyProcess.on('data', function (data) {
    ws.send(data);
  });

  ws.on('message', function (msg) {
    ptyProcess.write(msg);
  });

  ws.on('close', function () {
    ptyProcess.kill();
  });
});

server.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
