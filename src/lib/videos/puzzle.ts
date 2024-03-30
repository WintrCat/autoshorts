import { sample } from "lodash";
import { Socket } from "socket.io";
import { config } from "dotenv";
config();

import { renderVideo } from "../video";
import { ShortType } from "../types/short";
import { ChessPuzzleVideoOptions } from "../types/options";

import phonkTracks from "../../resources/music/phonk/tracks.json";

export async function producePuzzleShort(
    output: string,
    socket: Socket,
    pgn: string
) {

    // Pick a random music track from tracks.json
    const musicTrack = sample(phonkTracks);
    if (!musicTrack) {
        throw Error("there are no defined phonk music tracks.");
    }

    // Render the video
    await renderVideo<ChessPuzzleVideoOptions>(
        ShortType.CHESS_PUZZLE,
        {
            output: output,
            pgn: pgn,
            musicDropTime: musicTrack.dropTime,
            assets: {
                background: "src/resources/gridbackground.png",
                font: "src/resources/default.ttf",
                music: "src/resources/music/phonk/" + musicTrack.filename
            }
        },
        socket
    );

}