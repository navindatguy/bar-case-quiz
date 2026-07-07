import { useEffect, useState } from "react";

export default function App() {
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);
  const [answer, setAnswer] = useState(null);

  useEffect(() => {
    fetch("/api/questions?topic=Motions to Suppress")
      .then((r) => r.json())
      .then(setQuestions);
  }, []);

  const question = questions[current];

  function submitAnswer(choice) {
    setSelected(choice);
    fetch(`/api/questions/${question.id}/answer`)
      .then((r) => r.json())
      .then(setAnswer);
  }

  function nextQuestion() {
    setSelected(null);
    setAnswer(null);
    setCurrent((c) => c + 1);
  }

  if (!question) return <p>Loading questions…</p>;

  return (
    <div style={{ maxWidth: 640, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Bar Case Quiz</h1>
      <p>{question.prompt}</p>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {["A", "B", "C", "D"].map((choice) => (
          <li key={choice} style={{ marginBottom: "0.5rem" }}>
            <button
              disabled={!!selected}
              onClick={() => submitAnswer(choice)}
              style={{ width: "100%", textAlign: "left", padding: "0.5rem" }}
            >
              {choice}. {question[`choice_${choice.toLowerCase()}`]}
            </button>
          </li>
        ))}
      </ul>

      {answer && (
        <div style={{ marginTop: "1rem", padding: "1rem", background: "#f5f5f5" }}>
          <p>
            <strong>Correct answer:</strong> {answer.correct_choice}{" "}
            {selected === answer.correct_choice ? "✅" : "❌"}
          </p>
          <p>{answer.explanation}</p>
          <blockquote>{answer.source_excerpt}</blockquote>
          <a href={`/cases/${question.case_id}`}>View full case →</a>
          <br />
          <button onClick={nextQuestion} style={{ marginTop: "1rem" }}>
            Next question
          </button>
        </div>
      )}
    </div>
  );
}
