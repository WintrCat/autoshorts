import { TriviaVideoCategory } from "./trivia";

export interface VideoOptions {
    output: string;
}

export interface TriviaVideoOptions extends VideoOptions {
    count: number;
    category: TriviaVideoCategory;
    assets: {
        background: string;
        music: string;
        font: string;
    }
}

export interface ChessPuzzleVideoOptions extends VideoOptions {
    pgn: string;
    musicDropTime: number;
    assets: {
        background: string;
        font: string;
        music: string;
    }
}