// src/DefaultPage.js
import React from "react";

function DefaultPage() {
  return (
    <div className="bg-blue-200 p-6 text-gray-800 shadow-inner">
      <h2 className="text-2xl font-bold mb-4 text-blue-900">
        Welcome to SpaceDebris
      </h2>
      <p className="text-lg">
        This is the default page. Use the sidebar to navigate to the Space
        Debris Classifier or other features.
      </p>
    </div>
  );
}

export default DefaultPage;
