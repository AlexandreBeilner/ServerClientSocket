const onReceiveMessage = (socket, data) => {
    socket.broadcast.emit('message', data);
};

module.exports = onReceiveMessage;
