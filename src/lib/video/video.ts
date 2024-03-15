import process from "child_process";
import { VideoOptions } from "./options";

export const MEDIA = "./src/resources/media";

export type VideoType = "trivia" | "chess";

export async function produceVideo<VOpts extends VideoOptions>(type: VideoType, options: VOpts) {
    return new Promise(res => {
        const renderProcess = process.spawn("python", [
            `src/lib/python/${type.toLowerCase()}.py`, 
            JSON.stringify(options)
        ]);

        renderProcess.stdout.on("data", (data: Buffer) => {
            console.log(data.toString());
        });

        renderProcess.on("close", res);
    });
}