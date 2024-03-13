import { produceTriviaShort } from "./lib/video/trivia";

produceTriviaShort({
    background: "src/resources/media/starrynight.jpg",
    music: "src/resources/media/shootingstars.mp3",
    font: "src/resources/media/Madimi.ttf",
    output: "out/result.mp4",
    count: 2,
    category: "games"    
}).catch(err => console.log).then(a => console.log)