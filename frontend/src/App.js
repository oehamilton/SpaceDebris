import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  // Handle image selection
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPrediction(null);
      setError(null);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      setError("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      console.log("Sending image to server:", image.name);
      const response = await axios.post(
        "http://192.168.0.104:5000/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Received prediction response:", response.data);
      setPrediction(response.data);
      setError(null);
    } catch (err) {
      console.error("Error during prediction:", err);
      setError(
        err.response?.data?.error ||
          "An error occurred while making the prediction."
      );
      setPrediction(null);
    }
  };

  return (
    <div className="App">
      <h1>Space Debris Classifier</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/png, image/jpeg"
          onChange={handleImageChange}
        />
        <button type="submit">Predict</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {prediction && (
        <div>
          <h2>Prediction Result</h2>
          <p>Label: {prediction.label}</p>
          <p>Probability: {(prediction.probability * 100).toFixed(2)}%</p>
          <p>Class: {prediction.class}</p>
        </div>
      )}
    </div>
  );
}

export default App;
