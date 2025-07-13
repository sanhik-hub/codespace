// terminal-backend/terminal.js

const term = new Terminal();
term.open(document.getElementById('terminal'));

const socket = new WebSocket('ws://localhost:3001');
socket.onopen = () => console.log("✅ WebSocket connected");

socket.onmessage = (event) => term.write(event.data);
term.onData(data => socket.send(data));