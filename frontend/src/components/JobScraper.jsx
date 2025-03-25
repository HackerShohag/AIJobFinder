import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Sidebar from './Sidebar'; // Adjust the import path as necessary

const JobScraper = ({ originalText, keywords }) => {
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] = useState('No jobs found.');
  const [isLoading, setIsLoading] = useState(false);
  const [comparisonMessage, setComparisonMessage] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      setJobs([]);
      setIsLoading(true);
      try {
        const response = await axios.post('http://127.0.0.1:5000/scrape_jobs', { keywords });
        if (response.data.jobs?.length) {
          setJobs(response.data.jobs);
        } else {
          setMessage('No jobs found.');
        }
      } catch (error) {
        console.error('Error fetching jobs:', error);
        setMessage('Failed to fetch jobs.');
      }
      setIsLoading(false);
    };

    if (keywords?.length) {
      fetchJobs();
    }
  }, [keywords]);

  const compareCVWithJob = async (job) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/compare', {
        cv_text: originalText,
        job_url: job.link,
      });
      if (response.data?.message) {
        setComparisonMessage(response.data.response);
      } else {
        setComparisonMessage('No comparison message received.');
      }
    } catch (error) {
      console.error('Error comparing CV with job:', error);
      setComparisonMessage('Failed to fetch comparison message.');
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: 1, textAlign: 'center', marginTop: '20px', padding: '20px' }}>
        <h2>Recommended Jobs</h2>
        {isLoading && (
          <div style={{ padding: '20px' }}>
            <span style={{
              display: 'inline-block',
              width: '50px',
              height: '50px',
              border: '5px solid #007bff',
              borderTop: '5px solid transparent',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              marginRight: '8px',
            }}></span>
            <p style={{ fontSize: '16px', color: '#555' }}>Loading jobs...</p>
          </div>
        )}

        {!isLoading && jobs.length > 0 ? (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {jobs.map((job, index) => (
              <li
                key={index}
                style={{
                  border: '1px solid #ddd',
                  margin: '10px',
                  padding: '15px',
                  borderRadius: '8px',
                  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                  textAlign: 'left',
                }}
              >
                <div style={{ textAlign: 'right', marginTop: '10px' }}>
                  <button
                    onClick={() => compareCVWithJob(job)}
                    style={{
                      display: 'inline-block',
                      padding: '10px 15px',
                      backgroundColor: '#aa7bbb',
                      color: '#fff',
                      textDecoration: 'none',
                      borderRadius: '5px',
                      fontSize: '14px',
                      fontWeight: 'bold',
                    }}
                  >
                    Compare
                  </button>
                </div>
                <h3 style={{ fontSize: '20px', marginBottom: '10px' }}>
                  {job.title}
                </h3>
                <p style={{ margin: '5px 0' }}>
                  <strong>Company:</strong> {job.company}
                </p>
                <p style={{ margin: '5px 0' }}>
                  <strong>Location:</strong> {job.location}
                </p>
                <p style={{ margin: '5px 0' }}>
                  <strong>Source:</strong> {job.source}
                </p>
                {job.link && (
                  <div style={{ textAlign: 'right', marginTop: '10px' }}>
                    <a
                      href={job.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: 'inline-block',
                        padding: '10px 15px',
                        backgroundColor: '#007bff',
                        color: '#fff',
                        textDecoration: 'none',
                        borderRadius: '5px',
                        fontSize: '14px',
                        fontWeight: 'bold',
                      }}
                    >
                      View Job
                    </a>
                  </div>
                )}
              </li>
            ))}
          </ul>
        ) : (
          !isLoading && <p style={{ fontSize: '18px', color: '#555' }}>{message}</p>
        )}
      </div>
      <Sidebar message={comparisonMessage} />
    </div>
  );
};

export default JobScraper;
