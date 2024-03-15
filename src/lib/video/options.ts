export interface VideoOptions {
    output: string;
}

type TriviaVideoCategory = "animals" | "games";

export interface TriviaVideoOptions extends VideoOptions {
    count: number;
    category: TriviaVideoCategory;
    assets: {
        background: string;
        music: string;
        font: string;
    }
}