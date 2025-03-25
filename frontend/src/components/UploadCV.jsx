import React, { useState } from "react";
import axios from "axios";
import JobScraper from "./JobScraper";
import "./UploadCV.css"; // Import the CSS file
import ExpectedKeywords from "./Keywords";

const UploadCV = () => {
  const [file, setFile] = useState(null);
  const [keywords, setKeywords] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [extractedText, setExtractedText] = useState("");

  const handleUpload = async () => {
    setIsLoading(true);
    setMessage("");
    setKeywords([]);

    if (!file) {
      setMessage("Please select a file.");
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
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
        setExtractedText(response.data.extracted_text);
      } else {
        setMessage("Error: " + response.data.error);
      }
    } catch (error) {
      console.error("Upload Error:", error);
      setMessage("Please upload a valid file.");
      setKeywords([]);
    }
    setIsLoading(false);
  };

  return (
    <div className="container">
      <h1 className="heading">
        Skill<span style={{ color: "#4CAF50" }}>Scope</span>
      </h1>

      <div className="card">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="fileInput"
        />

        <button
          onClick={handleUpload}
          className={`button ${isLoading ? "disabled" : ""}`}
          onMouseOver={(e) => {
            if (!isLoading) e.target.style.backgroundColor = "#45a049";
          }}
          onMouseOut={(e) => {
            if (!isLoading) e.target.style.backgroundColor = "#4CAF50";
          }}
          disabled={isLoading}
        >
          {isLoading ? (
            <span>
              <span
                style={{
                  display: "inline-block",
                  width: "16px",
                  height: "16px",
                  border: "2px solid white",
                  borderTop: "2px solid transparent",
                  borderRadius: "50%",
                  animation: "spin 1s linear infinite",
                  marginRight: "8px",
                }}
              ></span>
              Uploading...
            </span>
          ) : (
            "Upload CV"
          )}
        </button>

        {isLoading && message && <p className="message">{message}</p>}
      </div>

      <div className="resultSection">
        <ExpectedKeywords
          originalText={extractedText}
          keywords={keywords}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default UploadCV;
