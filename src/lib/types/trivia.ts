import triviaQuestions from "../../resources/trivia/questions.json";

export type TriviaCategory = keyof typeof triviaQuestions;

export interface TriviaQuestion {
    title: string;
    answers: string[];
    correct: number;
}