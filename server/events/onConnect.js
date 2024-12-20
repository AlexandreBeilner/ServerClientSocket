const onConnect = (socket, connectedClients) => {
    console.log(`Client connected: ${socket.id}`);
    connectedClients[socket.id] = socket;

    const users = Object.keys(connectedClients).map((item) => {
        return {
            user: connectedClients[item].handshake.query.user,
            id:
                connectedClients[item].handshake.query.user +
                connectedClients[item].handshake.query.token,
            socketID: item,
        };
    });

    socket.broadcast.emit("connected_users", users);
    setTimeout(() => {
        socket.emit("connected_users", users);
    }, 1000);
};

module.exports = onConnect;
