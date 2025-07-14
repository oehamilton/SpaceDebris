// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./Header.js";
import DefaultPage from "./DefaultPage.js";
import SpaceDebrisClassifier from "./SpaceDebrisClassifier.js";
import WorkFlow from "./WorkFlow.js";

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <Router>
      <div className="h-screen bg-space-blue p-2 sm:p-4 flex flex-col gap-2 sm:gap-4 overflow-hidden">
        {/* Top Pane: Header with Navigation Toggle */}
        <Header toggleSidebar={toggleSidebar} isSidebarOpen={isSidebarOpen} />

        {/* Main Content: Full-width Main Pane */}
        <main className="flex-1 bg-blue-200 border border-blue-300 rounded-lg shadow-md overflow-y-auto">
          <Routes>
            <Route path="/" element={<DefaultPage />} />
            <Route path="/classifier" element={<SpaceDebrisClassifier />} />
            <Route path="/workflow" element={<WorkFlow />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
