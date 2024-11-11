import React, { useState, useEffect } from 'react';
import './App.css';

const questions = [
  { id: 1, question: "What is 2 + 2?", answer: "4" },
  { id: 2, question: "Capital of France?", answer: "Paris" },
  { id: 3, question: "What does 'www' stand for in a website browser?", answer: "World Wide Web" },
  { id: 4, question: "Year the first man landed on the moon?", answer: "1969" },
  { id: 5, question: "Is Java a type of OS?", answer: "No" },
];

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [timer, setTimer] = useState(10);

  useEffect(() => {
    if (timer === 0) {
      setCurrentQuestion((prev) => (prev < questions.length - 1 ? prev + 1 : prev));
      setTimer(10); // reset timer for next question
    }
    const interval = setInterval(() => {
      setTimer((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [timer]);

  return (
    <div className="App">
      <header className="App-header">
        <p>Question {currentQuestion + 1}/{questions.length}</p>
        <p>{questions[currentQuestion].question}</p>
        <p>Time left: {timer}</p>
      </header>
    </div>
  );
}

export default App;
