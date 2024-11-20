const onPrivateMessage = (socket, connectedClients, data) => {
    const { message, user, to } = data;
    const recipientSocket = connectedClients[to];

    if (recipientSocket) {
        recipientSocket.emit('private_message', { message, user });
    }
};

module.exports = onPrivateMessage;
