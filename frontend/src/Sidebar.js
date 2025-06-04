// src/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="bg-blue-800 w-64 h-full p-4 text-white">
      <h2 className="text-xl font-bold mb-4 text-blue-200">Navigation</h2>
      <ul>
        <li>
          <Link
            to="/classifier"
            className="text-blue-300 hover:text-blue-100 transition-colors"
          >
            Space Debris Classifier
          </Link>
        </li>
      </ul>
    </aside>
  );
}

export default Sidebar;
