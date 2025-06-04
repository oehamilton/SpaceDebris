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
      <div className="flex flex-col h-screen bg-space-blue">
        {/* Top Pane: Header */}
        <Header />

        {/* Main Content: Sidebar + Main Pane */}
        <div className="flex flex-1">
          {/* Left Sidebar */}
          <Sidebar />

          {/* Right Main Pane */}
          <main className="flex-1 bg-blue-50 overflow-y-auto">
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
