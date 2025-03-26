import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const Sidebar = ({ message }) => {
  const [isVisible, setIsVisible] = useState(true);

  if (!message || !isVisible) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      right: 0,
      width: '100%',
      height: '100%',
      backgroundColor: '#f4f4f4',
      boxShadow: '-2px 0 5px rgba(0,0,0,0.1)',
      padding: '20px',
      overflowY: 'auto',
      wordWrap: 'break-word',
    }}>
      <button
        onClick={() => setIsVisible(false)}
        style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          background: 'transparent',
          border: 'none',
          fontSize: '18px',
          cursor: 'pointer',
        }}
      >
        &times;
      </button>
      <h3>Comparison Result</h3>
      <ReactMarkdown>{message}</ReactMarkdown>
    </div>
  );
};

export default Sidebar;
