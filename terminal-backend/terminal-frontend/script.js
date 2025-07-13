const socket = new WebSocket("ws://localhost:3000");

const term = new Terminal();
term.open(document.getElementById("terminal"));

term.write('Welcome to your local terminal\r\n');

socket.onopen = () => {
  term.write('Terminal connected.\r\n');

  term.onData(data => {
    socket.send(data);
  });
};

socket.onmessage = (e) => {
  term.write(e.data);
};
