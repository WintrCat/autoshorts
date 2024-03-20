import process from "child_process";

import { VideoOptions } from "./options";

export async function renderVideo<VOpts extends VideoOptions>(type: string, options: VOpts) {
    return new Promise(res => {
        const renderProcess = process.spawn("python", [
            `src/lib/python/${type.toLowerCase()}.py`, 
            JSON.stringify(options)
        ]);

        renderProcess.stdout.on("data", (data: Buffer) => {
            console.log(data.toString("utf-8"));
        });

        renderProcess.stderr.on("data", (data: Buffer) => {
            console.log(data.toString("utf-8"));
        })

        renderProcess.on("close", res);
    });
}