import { useState, useRef, useEffect } from 'react';
import { recognizeFace } from '../api';
import './CameraCard.css';

export default function CameraCard({ onAttendanceMarked }) {
  const [stream, setStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);
  const [snapshotUrl, setSnapshotUrl] = useState(null);
  const videoRef = useRef(null);

  useEffect(() => {
    let streamHandle = null;
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: 'user' } })
      .then((s) => {
        streamHandle = s;
        setStream(s);
        if (videoRef.current) videoRef.current.srcObject = s;
      })
      .catch(() => setCameraError('Camera access denied or unavailable.'));

    return () => {
      if (streamHandle) {
        streamHandle.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  useEffect(() => {
    if (stream && videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  function captureFrame() {
    const video = videoRef.current;
    if (!video || !video.videoWidth) return null;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.92);
  }

  async function handleMarkAttendance() {
    const dataUrl = captureFrame();
    if (!dataUrl) return;
    setResult(null);
    setApiError('');
    setSnapshotUrl(dataUrl);
    setLoading(true);
    try {
      const data = await recognizeFace(dataUrl);
      setResult({ name: data.name, marked: data.marked });
      if (data.name !== 'Unknown' || data.marked) {
        onAttendanceMarked?.();
      }
    } catch (e) {
      setApiError(e.message || 'Network error');
    } finally {
      setLoading(false);
      setTimeout(() => setSnapshotUrl(null), 800);
    }
  }

  const resultClass = result
    ? result.name === 'Unknown'
      ? 'unknown'
      : result.marked
        ? 'success'
        : 'already'
    : '';

  return (
    <div className="card camera-card">
      <h2>Camera</h2>
      <div className="video-wrap">
        <video ref={videoRef} autoPlay playsInline muted className="video" />
        {snapshotUrl && (
          <img src={snapshotUrl} alt="Capture" className={`snapshot ${snapshotUrl ? 'visible' : ''}`} />
        )}
      </div>
      <button
        type="button"
        className="btn btn-primary"
        onClick={handleMarkAttendance}
        disabled={!!cameraError || loading}
      >
        {cameraError ? 'Camera unavailable' : loading ? 'Recognizing…' : 'Mark attendance'}
      </button>
      {result && (
        <div className={`result visible ${resultClass}`}>
          {result.name === 'Unknown'
            ? 'Face not recognized. Add your photo to the dataset folder.'
            : result.marked
              ? `Attendance marked for ${result.name}`
              : `${result.name} — already marked today`}
        </div>
      )}
      {apiError && <div className="error">{apiError}</div>}
    </div>
  );
}
