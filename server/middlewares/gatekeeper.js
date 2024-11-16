const gatekeeper = (socket, next) => {
    const token = socket.handshake.query.token;

    if (token) {
        return next();
    }
    return next(new Error("Authentication error"));
};

module.exports = gatekeeper;
