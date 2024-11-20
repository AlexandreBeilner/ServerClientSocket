const onReceiveVideoFrame = (socket, clientsToShow, connectedClients, data) => {
    clientsToShow.forEach(item => {
        if (connectedClients[item]) {
            connectedClients[item].emit('video_frame', data);
        }
    })
};

module.exports = onReceiveVideoFrame;
