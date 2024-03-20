import { readFileSync } from "fs";
import { ChessShowcaseVideoOptions } from "./lib/video/options";
import { renderVideo } from "./lib/video/video";

renderVideo<ChessShowcaseVideoOptions>(
    "chess/showcase",
    {
        output: "out/chess.mp4",
        pgn: readFileSync("./src/resources/chess/sample.pgn", "utf-8")
    }
);