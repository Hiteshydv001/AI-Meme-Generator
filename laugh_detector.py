# laugh_detector.py

import cv2
import mediapipe as mp
import numpy as np
import time
import config

class LaughDetector:
    def __init__(self):
        try:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MediaPipe FaceMesh. Error: {e}")

        self.mp_drawing = mp.solutions.drawing_utils
        self.LIP_CORNERS = [61, 291]
        self.UPPER_LIP, self.LOWER_LIP = [13], [14]
        
        # Load thresholds and rewards from config
        self.smile_threshold = config.SMILE_THRESHOLD
        self.laugh_threshold = config.LAUGH_THRESHOLD
        self.smile_reward = config.SMILE_REWARD
        self.laugh_reward = config.LAUGH_REWARD
        self.cooldown = config.REWARD_COOLDOWN
        
        self.last_reward_time = 0

    def get_reward_from_frame(self, frame):
        """Analyzes a single frame for a smile/laugh and returns a reward."""
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)
        
        reward = 0.0
        status = "Neutral"

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_c = face_landmarks.landmark[self.LIP_CORNERS[0]]
                right_c = face_landmarks.landmark[self.LIP_CORNERS[1]]
                upper_l = face_landmarks.landmark[self.UPPER_LIP[0]]
                lower_l = face_landmarks.landmark[self.LOWER_LIP[0]]

                mouth_width = np.linalg.norm([left_c.x - right_c.x, left_c.y - right_c.y])
                mouth_height = np.linalg.norm([upper_l.x - lower_l.x, upper_l.y - lower_l.y])
                
                ratio = mouth_height / mouth_width if mouth_width > 0.05 else 0

                if ratio > self.laugh_threshold:
                    reward, status = self.laugh_reward, "LAUGHING!"
                elif ratio > self.smile_threshold:
                    reward, status = self.smile_reward, "Smiling"
                
                self._draw_on_frame(frame, face_landmarks, status, reward, ratio)
        
        # Apply cooldown
        if reward > 0 and (time.time() - self.last_reward_time) < self.cooldown:
            return 0.0, frame
        if reward > 0:
            self.last_reward_time = time.time()

        return reward, frame

    def _draw_on_frame(self, frame, landmarks, status, reward, ratio):
        """Draws debug information on the frame."""
        self.mp_drawing.draw_landmarks(
            image=frame, landmark_list=landmarks, connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(121, 80, 242), thickness=1, circle_radius=1))
        
        cv2.putText(frame, f"Status: {status}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Reward: {reward:.1f}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def close(self):
        self.face_mesh.close()