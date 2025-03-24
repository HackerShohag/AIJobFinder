import React, { useState } from "react";
import axios from "axios";
import JobScraper from "./JobScraper";

const UploadCV = () => {
  const [file, setFile] = useState(null);
  const [keywords, setKeywords] = useState([]);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.data.success) {
        setKeywords(response.data.extracted_keywords);
        setMessage(response.data.message);
      } else {
        setMessage("Error: " + response.data.error);
      }
    } catch (error) {
      console.error("Upload Error:", error);
      setMessage("Error uploading file.");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Upload CV</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button
        onClick={handleUpload}
        style={styles.button}
        onMouseOver={(e) => (e.target.style.backgroundColor = "#45a049")}
        onMouseOut={(e) => (e.target.style.backgroundColor = "#4CAF50")}
      >
        Upload CV
      </button>

      {message && <p>{message}</p>}

      {keywords.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h3>Extracted Keywords:</h3>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {keywords.map((keyword, index) => (
              <li key={index}>{keyword}</li>
            ))}
          </ul>

          {/* Auto-render JobScraper after keywords extraction */}
          <JobScraper keywords={keywords} />
        </div>
      )}
    </div>
  );
};

export default UploadCV;

const styles = {
  container: { textAlign: "center", padding: "30px" },
  heading: { color: "#333" },
  button: {
    padding: "10px 20px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginTop: "10px",
  },
};
