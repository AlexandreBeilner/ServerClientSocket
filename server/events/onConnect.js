const onConnect = (socket, connectedClients) => {
    console.log(`Client connected: ${socket.id}`);
    connectedClients[socket.id] = socket;
};

module.exports = onConnect;
