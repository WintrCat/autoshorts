import { sample } from "lodash";

import { renderVideo } from "../video";
import { TriviaVideoCategory } from "../types/trivia";
import { TriviaVideoOptions } from "../types/options";
import { readdirSync } from "fs";

export async function produceTriviaShort(output: string) {

    const questionCount = 3;

    // Pick a random category of trivia questions
    const questionsCategory = sample(
        Object.values(TriviaVideoCategory)
    )!;

    // Pick a random lofi music track
    const lofiTrackFile = sample(
        readdirSync("src/resources/music/lofi")
    );
    if (!lofiTrackFile) {
        throw Error("there are no defined lofi music tracks.");
    }

    // Render video
    renderVideo<TriviaVideoOptions>(
        "trivia",
        {
            output: output,
            count: questionCount,
            category: questionsCategory,
            assets: {
                background: "src/resources/parkour.mp4",
                font: "src/resources/default.ttf",
                music: "src/resources/music/lofi/" + lofiTrackFile
            }
        }
    );

}