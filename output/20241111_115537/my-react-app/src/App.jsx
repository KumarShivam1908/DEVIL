import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const questions = [
    { question: 'What is AI?', answers: ['Artificial Intelligence', 'Artistic Interpretation', 'Arbitrary Inclusion', 'Antarctic Ice'], correct: 'Artificial Intelligence' },
    { question: 'Who is known as the father of AI?', answers: ['John McCarthy', 'Alan Turing', 'Elon Musk', 'John Lennon'], correct: 'John McCarthy' },
    { question: 'Which language is primarily used for AI?', answers: ['JavaScript', 'Python', 'C++', 'Java'], correct: 'Python' },
    { question: 'What is machine learning?', answers: ['A branch of AI', 'A coffee machine learning to make coffee', 'Learning about machines', 'None of the above'], correct: 'A branch of AI' },
    { question: 'What is the Turing Test?', answers: ['A test for computer hardware', 'A test for intelligence', 'A physical test', 'A test for programming skills'], correct: 'A test for intelligence' }
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [timeLeft, setTimeLeft] = useState(10);
  const [score, setScore] = useState(0);
  const [showScore, setShowScore] = useState(false);

  useEffect(() => {
    if (timeLeft === 0) {
      const nextQuestion = currentQuestion + 1;
      if (nextQuestion < questions.length) {
        setCurrentQuestion(nextQuestion);
        setTimeLeft(10);
      } else {
        setShowScore(true);
      }
    }

    const interval = setInterval(() => {
      setTimeLeft(timeLeft - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [currentQuestion, timeLeft, questions.length]);

  const answerClick = (isCorrect) => {
    if (isCorrect) {
      setScore(score + 1);
    }

    const nextQuestion = currentQuestion + 1;
    if (nextQuestion < questions.length) {
      setCurrentQuestion(nextQuestion);
      setTimeLeft(10);
    } else {
      setShowScore(true);
    }
  };

  return (
    <div className="App">
      {showScore ? (
        <div className="score-section">You scored {score} out of {questions.length}</div>
      ) : (
        <>
          <div className="question-section">
            <div className="question-count">
              <span>Question {currentQuestion + 1}</span>/{questions.length}
            </div>
            <div className="question-text">{questions[currentQuestion].question}</div>
          </div>
          <div className="answer-section">
            {questions[currentQuestion].answers.map((answer) => (
              <button onClick={() => answerClick(answer === questions[currentQuestion].correct)} key={answer}>{answer}</button>
            ))}
          </div>
          <div className="timer">Time left: {timeLeft} seconds</div>
        </>
      )}
    </div>
  );
}

export default App;
