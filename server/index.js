// Libraries
const { Server } = require("socket.io");
const express = require("express");
const http = require("http");

// Local
const gatekeeper = require("./middlewares/gatekeeper");
const onConnect = require("./events/onConnect");
const onDisconnect = require("./events/onDisconnect");
const onReceiveMessage = require("./events/onReceiveMessage");
const onCommand = require("./events/onCommand");
const onPrivateMessage = require("./events/onPrivateMessage");
const onReceiveVideoFrame = require("./events/onReceiveVideoFrame");

class App {
    constructor() {
        this.connectedClients = {};
        this.connectedClientsToShowVideo = [];
        this.port = 3000;

        this.app = express();
        this.server = http.createServer(this.app);
        this.io = new Server(this.server);
    }

    middlewares() {
        this.io.use(gatekeeper);
    }

    route() {
        this.app.get("/", (req, res) => {
            res.send("Socket.IO server is running");
        });
    }

    events() {
        this.io.on("connection", (socket) => {
            onConnect(socket, this.connectedClients);

            socket.on("disconnect", () => {
                onDisconnect(socket, this.connectedClients)
                let index = this.connectedClientsToShowVideo.indexOf(socket.id);
                if (index !== -1) {
                    this.connectedClientsToShowVideo.splice(index, 1);
                }
            });

            socket.on("message", (data) =>
                onReceiveMessage(socket, data)
            );

            socket.on("command", (data) => {
                onCommand(socket, data);
            });

            socket.on("private_message", (data) => {
                onPrivateMessage(socket, this.connectedClients, data)
            })

            socket.on('video_frame', (data) => {
                onReceiveVideoFrame(socket, this.connectedClientsToShowVideo, this.connectedClients, data)
            })

            socket.on('video_status', (data) => {
                if (data.status === 'stop') {
                    this.connectedClientsToShowVideo = []
                }
                socket.broadcast.emit('video_status', data)
            })

            socket.on('show_video', () => {
                this.connectedClientsToShowVideo.push(socket.id)
            })
        });
    }

    listen() {
        this.server.listen(this.port, () => {
            console.log(`Server is listening on port ${this.port}`);
        });
    }

    start() {
        this.middlewares();
        this.route();
        this.events();
        this.listen();
    }
}

const app = new App();
app.start();
