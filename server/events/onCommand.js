const onCommand = (socket, data) => {
    socket.broadcast.emit('command', data);
}

module.exports = onCommand;
