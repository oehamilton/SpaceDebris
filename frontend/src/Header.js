// src/Header.js
import React from "react";
import { FaRocket } from "react-icons/fa";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="bg-blue-950 text-white h-16 flex items-center justify-between px-4 shadow-lg">
      <div className="flex items-center">
        <FaRocket className="text-2xl mr-2 text-blue-300" />
        <span className="text-lg font-bold text-blue-200">SpaceDebris</span>
      </div>
      <nav className="flex space-x-4">
        <Link to="/" className="hover:text-blue-300 transition-colors">
          HOME
        </Link>
        <a href="#" className="hover:text-blue-300 transition-colors">
          Options
        </a>
        <a href="#" className="hover:text-blue-300 transition-colors">
          Help
        </a>
      </nav>
    </header>
  );
}

export default Header;
