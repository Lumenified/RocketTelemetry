const io = require('socket.io-client');

// Connect to the server
const socket = io('http://localhost:8080'); // replace with your Flask server's URL

socket.on('connect', () => {
  console.log("I'm connected!");
});

socket.on('update_data', (data) => {
  console.log('I received a message!');
  console.log(data);
});

socket.on('disconnect', () => {
  console.log("I'm disconnected!");
});

// Keep the process running
setInterval(() => {}, 1000);