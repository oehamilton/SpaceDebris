// src/Header.js
import React from "react";
import { FaRocket, FaBars } from "react-icons/fa";
import { Link } from "react-router-dom";

function Header({ toggleSidebar, isSidebarOpen }) {
  return (
    <header className="bg-blue-950 text-white flex items-center justify-between px-2 sm:px-4 py-2 border border-blue-300 rounded-lg shadow-md relative">
      <div className="flex items-center">
        <FaRocket className="text-xl sm:text-2xl mr-1 sm:mr-2 text-blue-200" />
        <span className="text-sm sm:text-lg font-bold text-blue-100">
          SpaceDebris
        </span>
        {/* Dropdown Navigation Button */}
        <button
          onClick={toggleSidebar}
          className="ml-2 sm:hidden text-blue-200 hover:text-blue-50 focus:outline-none"
          aria-label="Toggle Navigation"
        >
          <FaBars className="text-xl" />
        </button>
        {/* Dropdown Menu */}
        {isSidebarOpen && (
          <div className="absolute left-0 bottom-0 mt-10 w-48 bg-blue-800 text-white rounded-lg shadow-lg animate-slide-down z-10">
            <ul className="p-2">
              <li>
                <Link
                  to="/classifier"
                  className="block px-4 py-2 hover:bg-blue-700 rounded transition-colors"
                  onClick={toggleSidebar}
                >
                  Space Debris Classifier
                </Link>
              </li>
            </ul>
          </div>
        )}
      </div>
      <nav className="flex space-x-2 sm:space-x-4">
        <Link
          to="/"
          className="hover:text-blue-200 transition-colors text-sm sm:text-base"
        >
          Home
        </Link>
        <a
          href="#"
          className="hover:text-blue-200 transition-colors text-sm sm:text-base"
        >
          Options
        </a>
        <a
          href="#"
          className="hover:text-blue-200 transition-colors text-sm sm:text-base"
        >
          Help
        </a>
      </nav>
    </header>
  );
}

// Animation for dropdown (in a separate CSS file or inline)
const styles = `
  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .animate-slide-down {
    animation: slideDown 0.3s ease-out;
  }
`;

export default Header;
