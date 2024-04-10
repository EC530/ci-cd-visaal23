const socket = io();

document.getElementById('send-button').addEventListener('click', () => {
  const inputElement = document.getElementById('message-input');
  const message = inputElement.value.trim();
  if (message) {
    socket.emit('message', message);
    inputElement.value = '';
  }
});

socket.on('message', (message) => {
  const messagesElement = document.getElementById('messages');
  messagesElement.innerHTML += `<div>${message}</div>`;
});
