import process from "child_process";

import { objectToArguments } from "../arguments";

export interface TriviaShortOptions {
    count: number;
    category: string;
    background: string;
    music: string;
    font: string;
    output: string;
}

export async function produceTriviaShort(options: TriviaShortOptions) {
    return new Promise((res, rej) => {
        const args = objectToArguments(options as any);

        const renderProcess = process.spawn("python", ["src/lib/python/trivia.py", ...args]);

        renderProcess.stdout.on("data", (data: Buffer) => {
            console.log(data.toString());
        });
    });
}