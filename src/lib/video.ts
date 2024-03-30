import process from "child_process";
import { Socket } from "socket.io";

import { VideoOptions } from "./types/options";
import { ShortType } from "./types/short";

export async function renderVideo<VOpts extends VideoOptions>(
    type: ShortType, // The type of short to render
    options: VOpts, // The options to pass to Python
    socket: Socket // The websocket client to send logs to
) {
    
    return new Promise(res => {
        const renderProcess = process.spawn("python", [
            `src/lib/python/${type.toLowerCase()}.py`, 
            JSON.stringify(options)
        ]);

        renderProcess.stdout.on("data", (data: Buffer) => {
            socket.emit("render info", data.toString());
            console.log(data.toString());
        });
        
        renderProcess.stderr.on("data", (data: Buffer) => {
            socket.emit("render info", data.toString());
        });

        renderProcess.on("close", res);
    });
    
}

