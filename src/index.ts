import { readFileSync } from "fs";
import { ChessShowcaseVideoOptions } from "./lib/video/options";
import { renderVideo } from "./lib/video/video";

renderVideo<ChessShowcaseVideoOptions>(
    "chess/puzzle",
    {
        output: "out/chess.mp4",
        pgn: readFileSync("./src/resources/chess/sample.pgn", "utf-8"),
        assets: {
            background: "./src/resources/chess/gridbackgroundportrait.png",
            font: "./src/resources/media/Madimi.ttf",
            music: "./src/resources/media/shootingstars.mp3"
        }
    }
);