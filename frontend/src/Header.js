// src/Header.js
import React from "react";
import { FaRocket } from "react-icons/fa"; // Space icon (rocket)
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="bg-gray-800 text-white h-16 flex items-center justify-between px-4">
      <div className="flex items-center">
        <FaRocket className="text-2xl mr-2" />
        <span className="text-lg font-bold">SpaceDebris</span>
      </div>
      <nav className="flex space-x-4">
        <Link to="/" className="hover:underline">
          HOME
        </Link>
        <a href="#" className="hover:underline">
          Options
        </a>
        <a href="#" className="hover:underline">
          Help
        </a>
      </nav>
    </header>
  );
}

export default Header;
