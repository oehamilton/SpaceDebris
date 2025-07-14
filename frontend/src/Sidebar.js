// src/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";

function Sidebar({ isOpen }) {
  return (
    <aside
      className={`bg-gray-800 text-white p-4 border border-gray-300 rounded-lg shadow-md transition-all duration-300 ${
        isOpen ? "w-64" : "w-0 overflow-hidden"
      }`}
      aria-label="Navigation Menu"
      aria-expanded={isOpen}
    >
      <h2 className="text-xl font-bold mb-4 text-gray-100 sr-only">
        Navigation
      </h2>
      <ul className="space-y-2">
        <li>
          <Link
            to="/classifier"
            className="block px-4 py-2 hover:bg-gray-700 rounded transition-colors text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-gray-300"
            onClick={(e) => !isOpen && e.preventDefault()} // Prevent navigation if closed
            aria-label="Space Debris Classifier"
          >
            Space Debris Classifier
          </Link>
        </li>
      </ul>
    </aside>
  );
}

export default Sidebar;
