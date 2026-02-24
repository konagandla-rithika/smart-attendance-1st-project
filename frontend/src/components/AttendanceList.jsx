import { useState, useEffect, useCallback } from 'react';
import { getAttendance } from '../api';
import './AttendanceList.css';

export default function AttendanceList({ refreshTrigger }) {
  const [rows, setRows] = useState(null);
  const [error, setError] = useState(false);

  const load = useCallback(async () => {
    try {
      const data = await getAttendance(30);
      setRows(data);
      setError(false);
    } catch {
      setRows([]);
      setError(true);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load, refreshTrigger]);

  return (
    <div className="card attendance-card">
      <h2>Recent attendance</h2>
      <div className="attendance-list">
        {rows === null && <div className="empty">Loading…</div>}
        {rows && rows.length === 0 && !error && <div className="empty">No attendance records yet.</div>}
        {error && <div className="empty">Could not load attendance.</div>}
        {rows && rows.length > 0 &&
          rows.map((r, i) => (
            <div key={`${r.Name}-${r.Date}-${r.Time}-${i}`} className="row">
              <span className="name">{r.Name}</span>
              <span className="date">{r.Date}</span>
              <span className="time">{r.Time}</span>
            </div>
          ))}
      </div>
    </div>
  );
}
