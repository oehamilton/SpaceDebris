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
          size: (file.size / 1024).toFixed(2) + " KB",
          dimensions: `${img.naturalWidth} x ${img.naturalHeight} pixels`,
          pixelCount: img.naturalWidth * img.naturalHeight,
          aiProcessing: {
            resized: "128 x 128 pixels",
            normalized: "Pixel values scaled to [0, 1]",
          },
        };
        if (file.size >= 1024 * 1024) {
          stats.size = (file.size / (1024 * 1024)).toFixed(2) + " MB";
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
    <div className="min-h-screen bg-gray-900 p-2 sm:p-4">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl sm:text-3xl font-bold mb-4 text-gray-100 text-center">
          <a
            href="https://github.com/oehamilton/SpaceDebris"
            target="_blank"
            title="Click to See Code"
            rel="noopener noreferrer"
            aria-label="Space Debris Classifier GitHub repository (opens in new tab)"
            className="text-gray-200 hover:underline"
          >
            Space Debris Classifier
          </a>
        </h2>
        <h3 className="text-lg sm:text-xl font-semibold text-gray-200 mb-4 text-center">
          Upload an Image of Space Debris for Classification
        </h3>
        <h4 className="text-sm sm:text-base text-gray-200 mb-4 text-center">
          Supported formats: PNG, JPEG (max size: 10 MB)
        </h4>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="file"
            accept="image/png, image/jpeg"
            onChange={handleImageChange}
            className="w-full text-sm sm:text-base p-2 border rounded mb-2 sm:mb-4 text-gray-200"
          />
          <button
            type="submit"
            className="bg-gray-800 text-white px-6 py-3 rounded hover:bg-gray-700 transition-colors min-h-[48px] text-sm sm:text-base"
            disabled={!image}
          >
            Predict
          </button>
        </form>

        {/* Image Preview Before Prediction */}
        {imagePreview && !prediction && (
          <div className="mt-4">
            <h3 className="text-xl sm:text-2xl font-semibold text-gray-800 mb-2 text-center">
              Image Preview
            </h3>
            <img
              src={imagePreview}
              alt="Preview"
              className="max-w-full max-h-64 object-contain rounded-lg shadow-md mx-auto"
            />
          </div>
        )}

        {/* Post-Prediction Display */}
        {prediction && imagePreview && (
          <div className="mt-4">
            <h3 className="text-xl sm:text-2xl font-semibold text-gray-200 mb-2 text-center">
              Prediction Result
            </h3>
            <div className="flex flex-col md:flex-row gap-6 text-gray-300">
              {/* Image and Prediction */}
              <div className="flex-1 p-2 sm:p-4">
                <img
                  src={imagePreview}
                  alt="Uploaded"
                  className="max-w-full max-h-64 object-contain rounded-lg shadow-md mb-2 sm:mb-4 mx-auto"
                />
                <div className="space-y-1">
                  <p className="text-sm sm:text-base">
                    <strong>Label:</strong> {prediction.label}
                  </p>
                  <p className="text-sm sm:text-base">
                    <strong>Probability:</strong>{" "}
                    {(prediction.probability * 100).toFixed(2)}%
                  </p>
                  <p className="text-sm sm:text-base">
                    <strong>Class:</strong> {prediction.class}
                  </p>
                </div>
              </div>
              {/* Image Stats */}
              {imageStats && (
                <div className="flex-1 p-2 sm:p-4 overflow-x-auto">
                  <h4 className="text-lg sm:text-xl font-semibold text-gray-200 mb-2">
                    Image Stats
                  </h4>
                  <div className="space-y-1 text-sm sm:text-base text-gray-300">
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
                      <strong>Resized:</strong>{" "}
                      {imageStats.aiProcessing.resized}
                    </p>
                    <p>
                      <strong>Normalized:</strong>{" "}
                      {imageStats.aiProcessing.normalized}
                    </p>
                    {location ? (
                      <div className="mt-2">
                        <h5 className="font-semibold" text-gray-300>
                          Location (GPS):
                        </h5>
                        <p>
                          <strong>Latitude:</strong> {location.latitude}°
                        </p>
                        <p>
                          <strong>Longitude:</strong> {location.longitude}°
                        </p>
                      </div>
                    ) : (
                      <p className="mt-2 italic text-gray-300">
                        No location data available.
                      </p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {error && (
          <p className="text-red-600 mt-2 text-sm sm:text-base">{error}</p>
        )}
      </div>
    </div>
  );
}

export default SpaceDebrisClassifier;
