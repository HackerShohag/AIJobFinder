import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [userData, setUserData] = useState({
    study_field: "",
    job_type: "",
    job_role: "",
    skills: "",
    location: "",
    min_salary: "",
  });
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(""); // Store error messages

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form fields
    for (const key in userData) {
      if (!userData[key].trim()) {
        setError("⚠️ All fields are required!");
        return;
      }
    }

    setError(""); // Clear previous errors
    setLoading(true); // Show loading spinner

    try {
      const response = await axios.post("http://127.0.0.1:5000/recommend", userData);
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching job recommendations:", error);
      setError("❌ Failed to fetch job opportunities. Try again.");
    }

    setLoading(false); // Hide loading spinner
  };

  return (
    <div className="app-container">
      <h1>🚀 AI Job Finder</h1>

      <form onSubmit={handleSubmit} className="form-container">
        <input
          type="text"
          placeholder="Field of Study"
          value={userData.study_field}
          onChange={(e) => setUserData({ ...userData, study_field: e.target.value })}
        />

        <div className="select-container">
          <select
            value={userData.job_type}
            onChange={(e) => setUserData({ ...userData, job_type: e.target.value })}
          >
            <option value="">Select Job Type</option>
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="internship">Internship</option>
            <option value="remote">Remote</option>
          </select>
        </div>

        <input
          type="text"
          placeholder="Preferred Job Role (e.g., AI Engineer)"
          value={userData.job_role}
          onChange={(e) => setUserData({ ...userData, job_role: e.target.value })}
        />

        <input
          type="text"
          placeholder="Programming Skills (e.g., Python, TensorFlow)"
          value={userData.skills}
          onChange={(e) => setUserData({ ...userData, skills: e.target.value })}
        />

        <input
          type="text"
          placeholder="Preferred Location (e.g., USA, Remote)"
          value={userData.location}
          onChange={(e) => setUserData({ ...userData, location: e.target.value })}
        />

        <input
          type="number"
          placeholder="Minimum Expected Salary ($)"
          value={userData.min_salary}
          onChange={(e) => setUserData({ ...userData, min_salary: e.target.value })}
        />

        {error && <p className="error-message">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? <span className="spinner"></span> : "Find Opportunities"}
        </button>
      </form>

      <h2>🎯 Recommended Opportunities</h2>

      {loading ? (
        <div className="loading-container">
          <span className="spinner"></span>
          <p>Fetching job opportunities...</p>
        </div>
      ) : results.length === 0 ? (
        <p>No results yet. Submit the form to see suggestions.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Company</th>
                <th>Location</th>
                <th>Job Type</th>
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
                  <td>{op.company || "N/A"}</td>
                  <td>{op.location || "N/A"}</td>
                  <td>{op.job_type || "N/A"}</td>
                  <td>{op.source || "N/A"}</td>
                  <td>{op.similarity_score}</td>
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