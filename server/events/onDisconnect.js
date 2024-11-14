const onDisconnect = (socket, connectedClients) => {
    console.log(`Client disconnected: ${socket.id}`);
    delete connectedClients[socket.id];
};

module.exports = onDisconnect;
