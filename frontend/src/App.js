// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";
import DefaultPage from "./DefaultPage";
import SpaceDebrisClassifier from "./SpaceDebrisClassifier";

function App() {
  return (
    <Router>
      <div className="flex flex-col h-screen bg-space-blue p-4">
        {/* Top Pane: Header */}
        <Header />

        {/* Main Content: Sidebar + Main Pane */}
        <div className="flex flex-1 mt-4 space-x-4">
          {/* Left Sidebar */}
          <Sidebar />

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
