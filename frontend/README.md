# Smart Attendance – React frontend

HTML, CSS, and JavaScript (React) UI for the Smart Attendance system.

## Setup

```bash
cd frontend
npm install
```

## Development

1. Start the **Flask API** (from project root):
   ```bash
   cd "c:\Users\konag\Downloads\smart attendance"
   python -m app.main
   ```
   Flask runs at http://127.0.0.1:5000

2. Start the **React dev server**:
   ```bash
   cd frontend
   npm run dev
   ```
   React runs at http://localhost:5173 and proxies `/api` to Flask.

3. Open **http://localhost:5173** in your browser and allow camera access.

## Production build (optional)

To serve the React app from Flask (single server):

```bash
cd frontend
npm run build:flask
```

Then run only Flask and open http://127.0.0.1:5000. The built React app is in `app/static/`.

To build only to `frontend/dist/` (e.g. for a separate host):

```bash
npm run build
```

## Stack

- **React 18** (JSX)
- **Vite** (build and dev server)
- **CSS** (global + component-level)
