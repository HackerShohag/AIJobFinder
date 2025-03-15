import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [userData, setUserData] = useState({ study_field: "", research_interests: "" });
  const [results, setResults] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post("http://127.0.0.1:5000/recommend", userData);
    setResults(response.data);
  };

  return (
    <div className="app-container">
      <h1>AI Job Finder</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <input
          type="text"
          placeholder="Field of Study"
          onChange={(e) => setUserData({ ...userData, study_field: e.target.value })}
        />
        <input
          type="text"
          placeholder="Research Interests"
          onChange={(e) => setUserData({ ...userData, research_interests: e.target.value })}
        />
        <button type="submit">Find Opportunities</button>
      </form>

      <h2>Results:</h2>
      <div className="results-container">
        {results.map((op, idx) => (
          <p key={idx}>
            <a href={op.link} target="_blank" rel="noopener noreferrer">
              {op.title}
            </a>{" "}
            (Score: {op.score})
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;
