const fs = require("fs");

let index = 0;
for (const file of fs.readdirSync("src/resources/music/lofi")) {
    index++;
    fs.renameSync("src/resources/music/lofi/" + file, `track${index}.mp3`);
}