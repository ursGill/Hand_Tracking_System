import cv2
import mediapipe as mp
import numpy as np
import time 
from typing import Dict,List,Tuple,optional


class HandTracker:
    """
Detects RIGHT hand landmarks using MediaPipe and provides
structured landmark output along with optional debug visualization.
"""
    def __init__(self,max_num_hands:int=2,detection_confidence: float=0.7,tracking_confidence:float=0.7,enable_visualization:bool=True)->None:
        self.enable_visualization =enable_visualization
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # starts webcam capture
        if not self.cap.isOpened():
            raise RuntimeError("Failed to Open Webcam.")
        self.mp_hands =mp.solutions.hands  #Load ML tracking model
        self.mp_draw =mp.solutions.drawing_utils #Loads helper to draw skeleton

        self.hands = self.mp_hands.Hands(max_num_hands=max_num_hands,min_detection_confidence=detection_confidence,min_tracking_confidence=tracking_confidence)   #Initialize Hand ML Model

        self.prev_time = 0.0


        def _calculate_fps(self)->float:  #Private method
            current_time = time.time()
            fps = 1/(current_time - self.prev_time) if self.prev_time else 0.0
            self.prev_time = current_time

            return fps  # fps = how fast camera runs
        
        def _extract_landmarks(self,hand_landmarks)->List[Tuple[float,float,float]]:  # Converts MediaPipe format-> simple python list
            return [(lm.x,lm.y,lm.z) for lm in hand_landmarks.landmark]
        

        def _draw_debug(self,frame:np.ndarray,hand_landmarks, fps:float)->None:   #Draws hand skeleton + FPS on screen
            if hand_landmarks:
                self.mp_draw.draw_landmarks(frame,hand_landmarks,self.mp_hands.HAND_CONNECTIONS)

            cv2.putText(frame,f"FPS: {int(fps)}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)







