const API_BASE = '';

export async function recognizeFace(imageDataUrl) {
  const res = await fetch(`${API_BASE}/api/recognize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageDataUrl }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Request failed');
  return data;
}

export async function getAttendance(limit = 30) {
  const res = await fetch(`${API_BASE}/api/attendance?limit=${limit}`);
  const data = await res.json();
  if (!res.ok) throw new Error('Failed to load attendance');
  return data;
}
