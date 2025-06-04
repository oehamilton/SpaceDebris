// src/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="bg-gray-200 w-64 h-full p-4">
      <h2 className="text-xl font-bold mb-4">Navigation</h2>
      <ul>
        <li>
          <Link to="/classifier" className="text-blue-500 hover:underline">
            Space Debris Classifier
          </Link>
        </li>
        {/* Add more navigation links here as needed */}
      </ul>
    </aside>
  );
}

export default Sidebar;
