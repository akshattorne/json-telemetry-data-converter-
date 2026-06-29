# Data Format Converter

A virtual internship task that normalizes IoT device data from two different JSON input formats into a single unified output format.

**Live Demo:** [GitHub Pages link here after you enable it]

---

## Project Structure

```
project/
│
├── index.html          ← Static web version (runs on GitHub Pages)
├── style.css
├── script.js
│
├── python-version/     ← Original Python solution
│   ├── main.py
│   ├── data-1.json
│   ├── data-2.json
│   └── data-result.json
│
├── .gitignore
├── .nojekyll
├── requirements.txt
└── README.md
```

---

## What It Does

IoT devices send data in different formats depending on the source system. This project detects the format and converts it into one standard structure.

### Format 1 — Flat location string
```json
{
  "deviceID": "dh28dslkja",
  "deviceType": "LaserCutter",
  "timestamp": 1624445837783,
  "location": "japan/tokyo/keiyō-industrial-zone/daikibo-factory-meiyo/section-1",
  "operationStatus": "healthy",
  "temp": 22
}
```

### Format 2 — Nested device object + ISO timestamp
```json
{
  "device": { "id": "dh28dslkja", "type": "LaserCutter" },
  "timestamp": "2021-06-23T10:57:17.783Z",
  "country": "japan",
  "city": "tokyo",
  ...
}
```

### Unified Output
```json
{
  "deviceID": "dh28dslkja",
  "deviceType": "LaserCutter",
  "timestamp": 1624445837783,
  "location": {
    "country": "japan",
    "city": "tokyo",
    "area": "keiyō-industrial-zone",
    "factory": "daikibo-factory-meiyo",
    "section": "section-1"
  },
  "data": {
    "status": "healthy",
    "temperature": 22
  }
}
```

---

## Running the Web Version (GitHub Pages)

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Set **Source** to `main` branch, `/ (root)` folder
4. Click **Save** — your live URL will be `https://<username>.github.io/<repo-name>/`

---

## Running the Python Version

```bash
cd python-version
pip install flask gunicorn
python main.py
```

Then open `http://localhost:5000`

To run just the unit tests:
```bash
cd python-version
python -m unittest main
```

---

## Tests

Three tests verify the solution:

| Test | Description |
|------|-------------|
| Sanity Test | Validates the expected result JSON is well-formed |
| Data Type 1 Conversion | Confirms Format 1 converts correctly |
| Data Type 2 Conversion | Confirms Format 2 converts correctly (including Unix timestamp conversion) |
