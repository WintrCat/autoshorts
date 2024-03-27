const fs = require("fs");

/**
 * @type {{ [key: string]: any[] }}
 */
const questions = {};

for (const file of fs.readdirSync("src/resources/trivia")) {

    const questionsFile = "src/resources/trivia/" + file;
    const category = file.split(".")[0];
    
    questions[category] = [];

    let latestCorrectAnswer = "";
    for (const line of fs.readFileSync(questionsFile, "utf-8").split("\n")) {
        const lineContent = line.split(" ").slice(1).join(" ");

        if (line.startsWith("#Q")) {
            questions[category].push({});
            questions[category].at(-1)["title"] = lineContent;
        } else if (line.startsWith("^")) {
            latestCorrectAnswer = lineContent;
        } else if (["A", "B", "C", "D"].includes(line.charAt(0))) {
            questions[category].at(-1)["answers"] ??= [];
            questions[category].at(-1)["answers"].push(lineContent);

            const answerIndex = ["A", "B", "C", "D"].indexOf(line.charAt(0));
            if (lineContent == latestCorrectAnswer) {
                questions[category].at(-1)["correct"] = answerIndex;
            }
        }
    }

}

fs.writeFileSync(
    "src/resources/trivia/questions.json",
    JSON.stringify(questions, null, 4)
);