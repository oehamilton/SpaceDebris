// src/DefaultPage.js
import React from "react";
import { FaBars } from "react-icons/fa"; // Import the hamburger icon

const slideImage = "/Sat_Image_Default.png";

function DefaultPage() {
  return (
    <div className="bg-blue-200 p-6 text-gray-800 shadow-inner">
      <h2 className="text-2xl font-bold mb-4 text-blue-900">
        Welcome to SpaceDebris
      </h2>
      <p className="text-lg">
        This is the default page. Use the{" "}
        <FaBars className="inline text-xl align-middle" /> menu to navigate to
        the Space Debris Classifier or other features.
      </p>
      <div className="relative max-w-full max-h-full">
        <img
          src={slideImage}
          className="w-full h-auto object-contain"
          alt="Satellite Photo"
        />
      </div>
    </div>
  );
}

export default DefaultPage;
