import React, { useState } from "react";
import axios from "axios";
import JobScraper from "./JobScraper";
import './UploadCV.css'; // Import the CSS file

const UploadCV = () => {
  const [file, setFile] = useState(null);
  const [keywords, setKeywords] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

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
        <h3 className="subHeading">Extracted Keywords</h3>
        {isLoading && (
          <div style={{ textAlign: "center", padding: "20px" }}>
            <span
              style={{
                display: "inline-block",
                width: "50px",
                height: "50px",
                border: "5px solid black",
                borderTop: "5px solid transparent",
                borderRadius: "50%",
                animation: "spin 1s linear infinite",
                marginRight: "8px",
              }}
            ></span>
          </div>
        )}
        {keywords.length > 0 ? (
          <div className="keywordContainer">
            {keywords.map((keyword, index) => (
              <span key={index} className="keyword">
                {keyword}
              </span>
            ))}
          </div>
        ) : (
          <p style={{ textAlign: "center" }} >No keywords extracted.</p>
        )
        }
      </div>
      <div className="resultSection">
        <JobScraper keywords={keywords} />
      </div>
    </div>
  );
};

export default UploadCV;