const onPrivateMessage = (socket, connectedClients, data) => {
    console.log(data)
    const { message, user, to } = data;
    const recipientSocket = connectedClients[to];

    if (recipientSocket) {
        recipientSocket.emit('private_message', { message, user });
    }
};

module.exports = onPrivateMessage;
