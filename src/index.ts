import { TriviaVideoOptions } from "./lib/video/options";
import { MEDIA, produceVideo } from "./lib/video/video";

produceVideo<TriviaVideoOptions>("trivia", {
    count: 1,
    category: "games",
    output: "out/result.mp4",
    assets: {
        background: `${MEDIA}/starrynight.jpg`,
        font: `${MEDIA}/Madimi.ttf`,
        music: `${MEDIA}/shootingstars.mp3`
    }
});