import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [userData, setUserData] = useState({
    study_field: "",
    research_interests: "",
  });
  const [results, setResults] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post(
      "http://127.0.0.1:5000/recommend",
      userData
    );
    setResults(response.data);
  };

  return (
    <div className="app-container">
      <h1>🚀 AI Job Finder</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <input
          type="text"
          placeholder="Field of Study"
          onChange={(e) =>
            setUserData({ ...userData, study_field: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="Research Interests"
          onChange={(e) =>
            setUserData({ ...userData, research_interests: e.target.value })
          }
        />
        <button type="submit">Find Opportunities</button>
      </form>

      <h2>🎯 Recommended Opportunities</h2>
      {results.length === 0 ? (
        <p>No results yet. Submit the form to see suggestions.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Source</th>
                <th>Relevance Score</th>
                <th>Deadline</th>
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              {results.map((op, idx) => (
                <tr key={idx}>
                  <td>{op.title}</td>
                  <td>{op.source || "N/A"}</td>
                  <td>{op.score}</td>
                  <td>{op.deadline || "N/A"}</td>
                  <td>
                    <a href={op.link} target="_blank" rel="noopener noreferrer">
                      View Job
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
