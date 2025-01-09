import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setResult(null); // Reset result if a new file is uploaded
    setError(null); // Reset error if a new file is uploaded
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please select an image file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://localhost:8082/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response.data); // Debugging: Log the response

      if (response.data.error) {
        setError(response.data.error); // Handle backend error
      } else {
        setResult(response.data); // Set result if successful
      }
    } catch (error) {
      console.error("Axios error:", error); // Debugging: Log the error
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="title">Potato Disease Predictor</h1>
        <p className="description">
          Upload an image of a potato leaf, and we'll predict its condition.
        </p>

        <div className="upload-container">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="file-input"
          />
          <button onClick={handleSubmit} className="submit-btn">
            Upload and Predict
          </button>
        </div>

        {result && (
          <div className="result">
            <h3 className="result-header">Prediction Result</h3>
            <p>
              <strong>Class:</strong> {result.class}
            </p>
            <p>
              <strong>Confidence:</strong>{" "}
              {(result.confidence * 100).toFixed(2)}%
            </p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>{error}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
