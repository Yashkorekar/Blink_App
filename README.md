# Blink Detection and Performance Monitoring

## Overview
This project is a **Blink Detection System** using **OpenCV, Dlib, and Tkinter**, which detects blinks in real-time through a webcam. Additionally, it logs performance metrics such as CPU and memory usage and provides an API to fetch the last 10 blink logs using Flask.

## Features
- **Blink Detection**: Uses dlib's face landmark detector to analyze eye aspect ratio (EAR) and detect blinks.
- **GUI Interface**: A Tkinter-based application allows users to start/stop the camera and monitor blinks.
- **Data Logging**: Stores blink count data into an SQLite database (`face_data.db`).
- **Performance Monitoring**: Logs CPU and memory usage in real time.
- **Flask API**: Provides a REST API to retrieve the last 10 blink logs.
- **Standalone EXE**: The project is bundled into an executable file for easy local execution.

## Technologies Used
- **Python**
- **OpenCV**
- **Dlib**
- **Tkinter**
- **SQLite3**
- **Flask**
- **Psutil** (for performance monitoring)
- **Threading**

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/blink-detection.git
cd blink-detection
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Required Dlib Model
Download **shape_predictor_68_face_landmarks.dat** from the repository and place it in the project directory.

---

## Running the Application

### 1. Run the Blink Detection GUI
```bash
python app.py
```
This opens a Tkinter-based GUI where you can start/stop the camera and track blinks.

### 2. Run the Flask API (Optional)
To start the API for retrieving blink logs, run:
```bash
python api.py
```
Then, visit: `http://localhost:5000/metrics` to see the last 10 blink logs.

---

## Project Structure
```
blink-detection/
│── shape_predictor_68_face_landmarks.dat
│── app.py               # Main application (Tkinter GUI + Blink Detection)
│── api.py               # Flask API for retrieving blink logs
│── performance_logger.py  # Logs CPU & memory usage
│── data_logger.py        # Logs blink data into SQLite
│── requirements.txt      # Project dependencies
│── README.md            # Project documentation
```

---

## Packaging the Project into an Executable
To create a standalone `.exe` file, install **pyinstaller**:
```bash
pip install pyinstaller
```
Then, generate the executable:
```bash
pyinstaller --onefile --windowed app.py
```
The `.exe` file will be available inside the `dist/` folder.

---

## API Endpoints
### 1. Get Last 10 Blink Logs
**Endpoint:** `GET /metrics`

**Response:**
```json
[
  {"id": 1, "timestamp": "2025-02-11 12:34:56", "blink_count": 5},
  {"id": 2, "timestamp": "2025-02-11 12:36:10", "blink_count": 3}
]
```

---

## Troubleshooting
### 1. **Dlib Model Not Found Error**
- Ensure `shape_predictor_68_face_landmarks.dat` is in the project folder.

### 2. **Could Not Open Camera**
- Check if the webcam is being used by another application.
- Try running `cv2.VideoCapture(0)` in Python to test camera access.

### 3. **Flask API Not Working**
- Ensure the API server is running (`python api.py`).
- Try using `http://127.0.0.1:5000/metrics` instead of `localhost`.

---

## License
This project is open-source and available under the MIT License.

## Author
Yash Korekar

