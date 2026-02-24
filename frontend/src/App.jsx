import { useState, useCallback } from 'react';
import CameraCard from './components/CameraCard';
import AttendanceList from './components/AttendanceList';
import './App.css';

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const refreshAttendance = useCallback(() => {
    setRefreshKey((k) => k + 1);
  }, []);

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>Smart Attendance</h1>
          <p className="subtitle">
            Use your camera to mark attendance. Add face photos in the <code>dataset</code> folder (filename = person name).
          </p>
        </header>
        <div className="grid">
          <CameraCard onAttendanceMarked={refreshAttendance} />
          <AttendanceList refreshTrigger={refreshKey} />
        </div>
      </div>
    </div>
  );
}
