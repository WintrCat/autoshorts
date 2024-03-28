const fs = require("fs");
const questions = require("../resources/trivia/questions.json");

for (const category in questions) {
    questions[category] = questions[category].filter(question => {
        return question.title.length <= 105
    });
}

fs.writeFileSync(
    "src/resources/trivia/questionsshort.json",
    JSON.stringify(questions, null, 4)
);