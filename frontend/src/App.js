// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";
import DefaultPage from "./DefaultPage";
import SpaceDebrisClassifier from "./SpaceDebrisClassifier";

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <Router>
      <div className="min-h-screen bg-space-blue p-2 sm:p-4">
        {/* Top Pane: Header with Navigation Toggle */}
        <Header toggleSidebar={toggleSidebar} isSidebarOpen={isSidebarOpen} />

        {/* Main Content: Sidebar + Main Pane */}
        <div className="flex flex-1 mt-2 sm:mt-4">
          {/* Left Sidebar - Collapsible on Mobile */}
          <Sidebar isOpen={isSidebarOpen} />

          {/* Right Main Pane */}
          <main className="bg-blue-200 flex-1 border border-blue-300 rounded-lg shadow-md overflow-y-auto">
            <Routes>
              <Route path="/" element={<DefaultPage />} />
              <Route path="/classifier" element={<SpaceDebrisClassifier />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
