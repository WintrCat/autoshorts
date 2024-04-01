import { Server, Socket } from "socket.io";
import { Server as HTTPServer } from "http";
import { v4 as generateUUID } from "uuid";

import { ShortType } from "./lib/types/short";

import { produceTriviaShort } from "./lib/videos/trivia";
import { producePuzzleShort } from "./lib/videos/puzzle";

export function createSocketServer(httpServer: HTTPServer) {

    const io = new Server(httpServer);

    io.on("connection", socket => {
        socket.on("produce", (type?: ShortType, data?: string) => {
            if (!type) return;
            console.log(`received a request to produce a ${type} short.`);

            produceShort(type, socket, data);
        });
    });

}

async function produceShort(
    type: ShortType, // The type of short to be produced
    socket: Socket, // The websocket client to send logs to
    data?: string // Extra required parameters (like a PGN)
) {

    const outputDirectory = "out";
    const outputFilename = `${generateUUID()}.mp4`;
    const outputPath = `${outputDirectory}/${outputFilename}`;

    switch (type) {
        case ShortType.TRIVIA:
            await produceTriviaShort(outputPath, socket);
            break;
        case ShortType.CHESS_PUZZLE:
            if (data) {
                await producePuzzleShort(outputPath, socket, data);
            }
            break;
    }

    socket.emit("render done", outputFilename);

}