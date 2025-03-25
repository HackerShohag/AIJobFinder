import React, { useEffect, useState } from "react";
import axios from "axios";

const JobScraper = ({ keywords }) => {
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] = useState("No jobs found.");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchJobs = async () => {
      setIsLoading(true);
      try {
        const response = await axios.post("http://127.0.0.1:5000/scrape_jobs", {
          keywords,
        });
        console.log("Jobs fetched:", response.data); // Double-check the response

        if (response.data.jobs && response.data.jobs.length > 0) {
          setJobs(response.data.jobs);
        } else {
          setMessage("No jobs found.");
        }
      } catch (error) {
        console.error("Error fetching jobs:", error);
        setMessage("Failed to fetch jobs.");
      }
      setIsLoading(false);
    };

    if (keywords && keywords.length > 0) {
      fetchJobs();
    }
  }, [keywords]);

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h2>Recommended Jobs</h2>
      {!isLoading && message && <p>{message}</p>}

      {isLoading && <div style={{ textAlign: "center", padding: "20px" }}>
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
      </div>}

      {jobs.length > 0 && (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {jobs.map((job, index) => (
            <li
              key={index}
              style={{
                border: "1px solid #ccc",
                margin: "10px",
                padding: "10px",
                borderRadius: "8px",
              }}
            >
              <h3>{job.title}</h3>
              <p>
                <strong>Company:</strong> {job.company}
              </p>
              <p>
                <strong>Location:</strong> {job.location}
              </p>
              <p>
                <strong>Source:</strong> {job.source}
              </p>
              {job.link && (
                <a
                  href={job.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: "#007bff" }}
                >
                  View Job
                </a>
              )}
            </li>
          ))}
        </ul>
      )      }
    </div>
  );
};

export default JobScraper;
