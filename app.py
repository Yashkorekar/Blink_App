import tkinter as tk
from tkinter import messagebox
import cv2
import time
import threading
from collections import deque
import dlib
import numpy as np
from scipy.spatial import distance
from data_logger import DataLogger
from performance_logger import PerformanceLogger

class FaceAnalyzer:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        try:
            self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        except:
            messagebox.showerror("Error", "Could not load shape_predictor_68_face_landmarks.dat file")
            return
            
        self.EYE_AR_THRESH = 0.25
        self.EYE_AR_CONSEC_FRAMES = 3
        self.BLINK_COOLDOWN = 10
        self.blink_counter = 0
        self.frame_counter = 0
        self.blink_cooldown_counter = 0
        self.is_eye_closed = False
        self.start_time = time.time()

    def calculate_eye_aspect_ratio(self, eye_points):
        A = distance.euclidean(eye_points[1], eye_points[5])
        B = distance.euclidean(eye_points[2], eye_points[4])
        C = distance.euclidean(eye_points[0], eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def process_frame(self, frame):
        if frame is None:
            return frame
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        
        for face in faces:
            landmarks = self.predictor(gray, face)
            points = np.array([[p.x, p.y] for p in landmarks.parts()])
            
            left_eye = points[42:48]
            right_eye = points[36:42]
            
            left_ear = self.calculate_eye_aspect_ratio(left_eye)
            right_ear = self.calculate_eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0
            
            if ear < self.EYE_AR_THRESH and not self.is_eye_closed and self.blink_cooldown_counter == 0:
                self.is_eye_closed = True
                self.blink_counter += 1
                self.blink_cooldown_counter = self.BLINK_COOLDOWN
            elif ear >= self.EYE_AR_THRESH:
                self.is_eye_closed = False
            
            if self.blink_cooldown_counter > 0:
                self.blink_cooldown_counter -= 1
            
            for point in points:
                cv2.circle(frame, tuple(point), 1, (0, 255, 0), -1)
            
            cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
            cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)
            
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return frame

    def reset_blink_counter(self):
        self.blink_counter = 0

class CameraApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Camera App with Blink Detection")
        self.app.geometry("300x250")
        
        self.stop_camera = False
        self.cap = None
        self.face_analyzer = FaceAnalyzer()
        self.data_logger = DataLogger()
        self.performance_logger = PerformanceLogger()
        self.setup_ui()

    def setup_ui(self):
        label = tk.Label(self.app, text="Click below to start the camera!")
        label.pack(pady=10)

        camera_button = tk.Button(self.app, text="Start Camera", command=self.start_camera)
        camera_button.pack(pady=10)

        stop_button = tk.Button(self.app, text="Stop Camera", command=self.stop_camera_func)
        stop_button.pack(pady=10)

        reset_button = tk.Button(self.app, text="Reset Blink Counter", 
                               command=self.face_analyzer.reset_blink_counter)
        reset_button.pack(pady=5)

        check_threads_button = tk.Button(self.app, text="Check Active Threads", 
                                       command=self.check_threads)
        check_threads_button.pack(pady=5)

        self.blink_label = tk.Label(self.app, text="Blinks: 0")
        self.blink_label.pack(pady=10)

    def check_threads(self):
        print("Active threads:", threading.active_count())
        print("Threads list:", threading.enumerate())

    def start_camera(self):
        self.stop_camera = False
        self.cap = cv2.VideoCapture(0)
        self.performance_logger.start_logging()

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return

        threading.Thread(target=self.capture_frames, daemon=True).start()

    def capture_frames(self):
        prev_time = 0
        fps_limit = 30
        frame_count = 0
        fps_history = deque(maxlen=30)

        while not self.stop_camera:
            ret, frame = self.cap.read()
            if not ret:
                break

            curr_time = time.time()
            elapsed_time = curr_time - prev_time

            if elapsed_time < (1 / fps_limit):
                time.sleep((1 / fps_limit) - elapsed_time)

            prev_time = time.time()

            if elapsed_time > 0:
                fps_history.append(1 / elapsed_time)
            avg_fps = sum(fps_history) / len(fps_history)
            frame_count += 1
            processed_frame = self.face_analyzer.process_frame(frame)

            self.blink_label.config(text=f"Blinks: {self.face_analyzer.blink_counter}")

            if frame_count % 30 == 0:  # Log data every 30 frames
                self.data_logger.log_data(self.face_analyzer.blink_counter)

            cv2.putText(processed_frame, 
                       f"FPS: {int(avg_fps)} | Blinks: {self.face_analyzer.blink_counter}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Camera Feed", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Camera Feed", cv2.WND_PROP_VISIBLE) < 1:
                self.stop_camera = True

        self.cap.release()
        cv2.destroyAllWindows()
        self.data_logger.close()

    def stop_camera_func(self):
        self.stop_camera = True
        self.performance_logger.stop_logging()
        summary = self.performance_logger.get_performance_summary()
        print(summary)

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = CameraApp()
    app.run()