// src/SpaceDebrisClassifier.js
import React, { useState } from "react";
import axios from "axios";

function SpaceDebrisClassifier() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPrediction(null);
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      setError("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      console.log("Sending request with image:", image.name);
      console.log("xxx");
      const response = await axios.post(
        "http://localhost:5000/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Prediction response:", response.data);
      console.log("xxx");
      setPrediction(response.data);
      setError(null);
    } catch (err) {
      console.error("Request failed:", err);
      console.log("xxx");
      setError(
        err.response?.data?.error ||
          "An error occurred while making the prediction: " + err.message
      );
      setPrediction(null);
    }
  };

  return (
    <div className="bg-blue-200 p-4 text-gray-800">
      <h2 className="text-2xl font-bold mb-4 text-blue-900">
        Space Debris Classifier
      </h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/png, image/jpeg"
          onChange={handleImageChange}
          className="mb-2 text-gray-700"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
        >
          Predict
        </button>
      </form>

      {error && <p className="text-red-600 mt-2">{error}</p>}

      {prediction && (
        <div className="mt-4">
          <h3 className="text-xl font-semibold text-blue-800">
            Prediction Result
          </h3>
          <p>Label: {prediction.label}</p>
          <p>Probability: {(prediction.probability * 100).toFixed(2)}%</p>
          <p>Class: {prediction.class}</p>
        </div>
      )}
    </div>
  );
}

export default SpaceDebrisClassifier;
