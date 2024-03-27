import { TriviaQuestion } from "./trivia";

export interface VideoOptions {
    output: string;
}

export interface VideoResources {
    background: string;
    music: string;
    font: string;
}

export interface TriviaVideoOptions extends VideoOptions {
    questions: TriviaQuestion[];
    assets: VideoResources;
}

export interface ChessPuzzleVideoOptions extends VideoOptions {
    pgn: string;
    musicDropTime: number;
    assets: VideoResources;
}