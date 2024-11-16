const onReceiveMessage = (socket, connectedClients, data) => {
    socket.broadcast.emit('message', data);
};

module.exports = onReceiveMessage;