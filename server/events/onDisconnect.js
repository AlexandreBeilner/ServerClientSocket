const onDisconnect = (socket, connectedClients) => {
    console.log(`Client disconnected: ${socket.id}`);
    delete connectedClients[socket.id];

    const users = Object.keys(connectedClients).map(item => {
        return {user: connectedClients[item].handshake.query.user, id: connectedClients[item].handshake.query.user + connectedClients[item].handshake.query.token, socketID: item};
    })

    socket.broadcast.emit('connected_users', users);
};

module.exports = onDisconnect;
