import React, { useState, useEffect } from 'react';
import JobScraper from './JobScraper';

function ExpectedKeywords({ keywords, originalText, isLoading }) {
    
    const [expectedKeywords, setExpectedKeywords] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editedKeywords, setEditedKeywords] = useState(keywords.join(', '));
    const [selectedKeywords, setSelectedKeywords] = useState([]);

    useEffect(() => {
        setExpectedKeywords(keywords);
      }, [keywords]);
    
    
    console.log("keywords", keywords);
    // setExpectedKeywords(keywords);
    console.log("expectedKeywords", expectedKeywords);


    const handleEditClick = () => {
        setIsModalOpen(true);
    };

    const handleSave = () => {
        setExpectedKeywords(editedKeywords.split(',').map(keyword => keyword.trim()));
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setEditedKeywords(expectedKeywords.join(', '));
        setIsModalOpen(false);
    };

    const handleKeywordClick = (keyword) => {
        setSelectedKeywords((prevSelected) => {
            if (prevSelected.includes(keyword)) {
                return prevSelected.filter((k) => k !== keyword);
            } else if (prevSelected.length < 5) {
                return [...prevSelected, keyword];
            }
            return prevSelected;
        });
    };

    return (
        <>
            <div style={{ position: "relative" }}>
                <h3 className="subHeading">Extracted Keywords</h3>
                <button
                    onClick={handleEditClick}
                    style={{
                        position: "absolute",
                        top: "0px",
                        right: "0px",
                        marginTop: "0",
                        backgroundColor: "transparent",
                        border: "none",
                        cursor: "pointer",
                        hover: "pointer",
                    }}
                >
                    <span role="img" aria-label="edit" style={{ fontSize: "16px" }}>✏️</span>
                </button>
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
                {expectedKeywords.length > 0 ? (
                    <div className="keywordContainer">
                        {expectedKeywords.map((keyword, index) => (
                            <span
                                key={index}
                                className={`keyword ${selectedKeywords.includes(keyword) ? 'selected' : ''}`}
                                onClick={() => handleKeywordClick(keyword)}
                                style={{
                                    cursor: "pointer",
                                    backgroundColor: selectedKeywords.includes(keyword) ? "#d3f9d8" : "transparent",
                                }}
                            >
                                {keyword}
                            </span>
                        ))}
                    </div>
                ) : (
                    <p style={{ textAlign: "center" }}>No keywords extracted.</p>
                )}
            </div>

            {isModalOpen && (
                <div className="modal">
                    <div className="modalContent">
                        <h3>Edit Keywords</h3>
                        <textarea
                            value={editedKeywords}
                            onChange={(e) => setEditedKeywords(e.target.value)}
                            rows="5"
                            style={{ width: "100%" }}
                        ></textarea>
                        <div style={{ marginTop: "10px" }}>
                            <button onClick={handleSave} style={{ marginRight: "10px" }}>
                                Save
                            </button>
                            <button onClick={handleCancel}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}
            <div style={{ paddingTop: "50px" }}>
            {
                selectedKeywords.length > 0 && <JobScraper originalText={originalText} keywords={selectedKeywords} />
            }
            </div>
        </>
    );
}

export default ExpectedKeywords;