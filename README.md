# Face Recognition Attendance & Notification System

An AI-powered attendance system using FaceNet, MTCNN, FastAPI, Streamlit, and modern HTML5/CSS3/Vanilla JS Single Page Application (SPA).

## Features

- **Modern Web Frontend**: Glassmorphism UI with real-time biometric HUD, dark/light mode toggle, live audio synthesizer, and responsive layout.
- **AI Face Scanner**: Live webcam face detection, alignment, FaceNet embedding comparison, and sub-second attendance marking.
- **Person Registration**: Interactive multi-shot capture with 5x auto-burst mode and live gallery.
- **Instant Alerts**: SMS and WhatsApp notifications dispatched upon check-in (Twilio / Fast2SMS / CallMeBot / Simulation).
- **Attendance Records**: Searchable and filterable history table by name, ID, department, and date with one-click CSV export.
- **People Management**: Complete CRUD directory with search, inline editing, and deletion.
- **Telemetry & Settings**: Live dashboard KPIs, adjustable Euclidean distance threshold, and duplicate cooldown slider.

## Technology Stack

- **Backend**: FastAPI, Uvicorn, SQLite3, PyTorch / TensorFlow (FaceNet & MTCNN)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism Design System), Modern ES6+ JavaScript
- **Legacy UI**: Streamlit (optional alternative interface)

## Quick Start

### 1. Launch Modern Web UI (Recommended)
Double-click `run_web.bat` or run:
```bash
python server.py
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**

### 2. Launch Streamlit UI
Double-click `run.bat` (select option 2) or run:
```bash
streamlit run app.py
```