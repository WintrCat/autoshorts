import fs from "fs";
import { sample } from "lodash";

import { renderVideo } from "../video";
import { ChessPuzzleVideoOptions } from "../types/options";

import musicTracks from "../../resources/music/tracks.json";

export async function producePuzzleShort(output: string) {

    // Create the assets folder if necessary
    if (!fs.existsSync("assets")) {
        fs.mkdirSync("assets");
    }

    // Pick a random PGN from the assets folder
    const pgnFile = sample(
        fs.readdirSync("assets").filter(file => file.endsWith(".pgn"))
    );

    if (!pgnFile) {
        throw Error("there are no available PGN files to consume.");
    }

    const pgn = fs.readFileSync(
        "assets/" + pgnFile,
        "utf-8"
    );

    // Pick a random music track from tracks.json
    const musicTrack = sample(musicTracks);
    if (!musicTrack) {
        throw Error("there are no defined music tracks.");
    }

    // Render the video
    await renderVideo<ChessPuzzleVideoOptions>(
        "chess/puzzle",
        {
            output: output,
            pgn: pgn,
            musicDropTime: musicTrack.dropTime,
            assets: {
                background: "src/resources/gridbackground.png",
                font: "src/resources/default.ttf",
                music: "src/resources/music/" + musicTrack.filename
            }
        }
    );

    // Delete the used PGN file
    // fs.rmSync("assets/" + pgnFile);

}