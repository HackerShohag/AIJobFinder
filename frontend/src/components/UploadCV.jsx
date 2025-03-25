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
      console.log("Uploading file...");
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          withCredentials: true,
        }
      );

      console.log(response);

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
      <h1 style={styles.heading}>
        Skill<span style={{ color: "#4CAF50" }}>Scope</span>
      </h1>

      <div style={styles.card}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          style={styles.fileInput}
        />

        <button
          onClick={handleUpload}
          style={styles.button}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#45a049")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#4CAF50")}
        >
          Upload CV
        </button>

        {message && <p style={styles.message}>{message}</p>}
      </div>

      {keywords.length > 0 && (
        <div style={styles.resultSection}>
          <h3 style={styles.subHeading}>Extracted Keywords</h3>
          <div style={styles.keywordContainer}>
            {keywords.map((keyword, index) => (
              <span key={index} style={styles.keyword}>
                {keyword}
              </span>
            ))}
          </div>

          {/* Auto-render JobScraper after keywords extraction */}
          <JobScraper keywords={keywords} />
        </div>
      )}
    </div>
  );
};

export default UploadCV;

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#f4f6f8",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "30px",
    fontFamily: "Arial, sans-serif",
  },
  heading: {
    fontSize: "3rem",
    color: "#333",
    marginBottom: "20px",
  },
  card: {
    backgroundColor: "#fff",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    textAlign: "center",
    width: "90%",
    maxWidth: "500px",
  },
  fileInput: {
    padding: "10px",
    width: "100%",
    marginBottom: "20px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "12px 30px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "16px",
    transition: "background-color 0.3s ease",
  },
  message: {
    marginTop: "15px",
    color: "#555",
    fontSize: "16px",
  },
  resultSection: {
    marginTop: "40px",
    width: "90%",
    maxWidth: "600px",
    backgroundColor: "#fff",
    padding: "25px",
    borderRadius: "12px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
  },
  subHeading: {
    fontSize: "24px",
    color: "#333",
    marginBottom: "15px",
  },
  keywordContainer: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
  },
  keyword: {
    backgroundColor: "#e0f7e9",
    padding: "8px 15px",
    borderRadius: "20px",
    color: "#333",
    fontSize: "14px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
};
