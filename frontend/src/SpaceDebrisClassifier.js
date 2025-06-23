// src/SpaceDebrisClassifier.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import EXIF from "exif-js";

function SpaceDebrisClassifier() {
  const [image, setImage] = useState(null); // File object
  const [imagePreview, setImagePreview] = useState(null); // URL for preview
  const [imageStats, setImageStats] = useState(null); // Stats (size, dimensions, etc.)
  const [location, setLocation] = useState(null); // GPS location from EXIF
  const [prediction, setPrediction] = useState(null); // Prediction result
  const [error, setError] = useState(null); // Error message

  // Handle image selection
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Reset previous states
      setImage(file);
      setPrediction(null);
      setError(null);
      setImageStats(null);
      setLocation(null);

      // Generate image preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);

      // Load image to get dimensions and EXIF data
      const img = new Image();
      img.onload = () => {
        const stats = {
          size: (file.size / 1024).toFixed(2) + " KB", // Convert bytes to KB
          dimensions: `${img.naturalWidth} x ${img.naturalHeight} pixels`,
          pixelCount: img.naturalWidth * img.naturalHeight,
          aiProcessing: {
            resized: "128 x 128 pixels",
            normalized: "Pixel values scaled to [0, 1]",
          },
        };
        if (file.size >= 1024 * 1024) {
          stats.size = (file.size / (1024 * 1024)).toFixed(2) + " MB"; // Convert to MB if >= 1MB
        }
        setImageStats(stats);
      };
      img.src = URL.createObjectURL(file);

      // Extract EXIF data for GPS location
      EXIF.getData(file, function () {
        const exifData = EXIF.getAllTags(this);
        if (exifData.GPSLatitude && exifData.GPSLongitude) {
          const lat = convertDMSToDecimal(
            exifData.GPSLatitude,
            exifData.GPSLatitudeRef
          );
          const lon = convertDMSToDecimal(
            exifData.GPSLongitude,
            exifData.GPSLongitudeRef
          );
          setLocation({ latitude: lat, longitude: lon });
        } else {
          setLocation(null);
        }
      });
    }
  };

  // Convert DMS (Degrees, Minutes, Seconds) to decimal for GPS coordinates
  const convertDMSToDecimal = (dms, ref) => {
    const [degrees, minutes, seconds] = dms.map((val) =>
      typeof val === "object" ? val.num / val.den : val
    );
    let decimal = degrees + minutes / 60 + seconds / 3600;
    if (ref === "S" || ref === "W") {
      decimal = -decimal;
    }
    return decimal.toFixed(6);
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
      console.log("Sending request with image:", image.name);
      console.log("xxx");
      const response = await axios.post(
        "https://space-debris-api-2713d4504a5f.herokuapp.com/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Prediction response:", response.data);

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
    <div className="p-6 text-gray-800 shadow-inner">
      <h2 className="text-2xl font-bold mb-4 text-blue-900">
        <a
          href="https://github.com/oehamilton/SpaceDebris"
          target="Click to See Code"
          rel="noopener noreferrer"
          className="text-blue-600 hover:underline"
        >
          Space Debris Classifier
        </a>
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
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-800 transition-colors"
        >
          Predict
        </button>
      </form>

      {/* Image Preview Before Prediction */}
      {imagePreview && !prediction && (
        <div className="mt-4">
          <h3 className="text-xl font-semibold text-blue-800 mb-2">
            Image Preview
          </h3>
          <img
            src={imagePreview}
            alt="Preview"
            className="max-w-xs max-h-64 object-contain rounded-lg shadow-md"
          />
        </div>
      )}

      {/* Post-Prediction Display */}
      {prediction && imagePreview && (
        <div className="mt-4">
          <h3 className="text-xl font-semibold text-blue-800 mb-2">
            Prediction Result
          </h3>
          <div className="flex flex-col md:flex-row gap-4">
            {/* Image and Prediction */}
            <div className="flex-1">
              <img
                src={imagePreview}
                alt="Uploaded"
                className="max-w-xs max-h-64 object-contain rounded-lg shadow-md mb-4"
              />
              <p>
                <strong>Label:</strong> {prediction.label}
              </p>
              <p>
                <strong>Probability:</strong>{" "}
                {(prediction.probability * 100).toFixed(2)}%
              </p>
              <p>
                <strong>Class:</strong> {prediction.class}
              </p>
            </div>
            {/* Image Stats */}
            {imageStats && (
              <div className="flex-1">
                <h4 className="text-lg font-semibold text-blue-800 mb-2">
                  Image Stats
                </h4>
                <p>
                  <strong>Size:</strong> {imageStats.size}
                </p>
                <p>
                  <strong>Dimensions:</strong> {imageStats.dimensions}
                </p>
                <p>
                  <strong>Total Pixels:</strong>{" "}
                  {imageStats.pixelCount.toLocaleString()}
                </p>
                <h5 className="font-semibold mt-2">AI Processing:</h5>
                <p>
                  <strong>Resized:</strong> {imageStats.aiProcessing.resized}
                </p>
                <p>
                  <strong>Normalized:</strong>{" "}
                  {imageStats.aiProcessing.normalized}
                </p>
                {location ? (
                  <div className="mt-2">
                    <h5 className="font-semibold">Location (GPS):</h5>
                    <p>
                      <strong>Latitude:</strong> {location.latitude}°
                    </p>
                    <p>
                      <strong>Longitude:</strong> {location.longitude}°
                    </p>
                  </div>
                ) : (
                  <p className="mt-2 italic text-gray-600">
                    No location data available.
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}

export default SpaceDebrisClassifier;
