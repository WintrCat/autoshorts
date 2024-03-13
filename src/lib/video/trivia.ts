import process from "child_process";

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
        const args = Object
            .entries(options)
            .map(entry => {
                entry[0] = "--" + entry[0];
                entry[1] = entry[1].toString();
                return entry;
            })
            .reduce((acc, entry) => acc.concat(entry) as [string, any]);

        const renderProcess = process.spawn("python", ["src/lib/python/trivia.py", ...args]);

        renderProcess.stdout.on("data", (data: Buffer) => {
            console.log(data.toString());
        });
    });
}