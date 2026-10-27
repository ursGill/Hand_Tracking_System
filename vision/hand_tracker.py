import cv2
import mediapipe as mp
import numpy as np
import time 
from typing import Dict,List,Tuple,Optional


class HandTracker:
    """
Detects RIGHT hand landmarks using MediaPipe and provides
structured landmark output along with optional debug visualization.
"""
    def __init__(self,max_num_hands:int=2,detection_confidence: float=0.7,tracking_confidence:float=0.7,model_complexity:int=1,enable_visualization:bool=True)->None:
        self.enable_visualization =enable_visualization
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # starts webcam capture
        
        # Set high resolution for wide area capturing and better accuracy at a distance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        if not self.cap.isOpened():
            raise RuntimeError("Failed to Open Webcam.")
        self.mp_hands =mp.solutions.hands  #Load ML tracking model
        self.mp_draw =mp.solutions.drawing_utils #Loads helper to draw skeleton

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=model_complexity,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )   #Initialize Hand ML Model

        self.prev_time = 0.0


    def _calculate_fps(self)->float:  #Private method
        current_time = time.time()
        fps = 1/(current_time - self.prev_time) if self.prev_time else 0.0
        self.prev_time = current_time

        return fps  # fps = how fast camera runs
        
    def _extract_landmarks(self,hand_landmarks)->List[Tuple[float,float,float]]:  # Converts MediaPipe format-> simple python list
        return [(lm.x,lm.y,lm.z) for lm in hand_landmarks.landmark]
        

    def _draw_debug(self,frame:np.ndarray,hand_landmarks, fps:float)->None:   #Draws hand skeleton + FPS on scree
        if hand_landmarks:
            self.mp_draw.draw_landmarks(frame,hand_landmarks,self.mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame,f"FPS: {int(fps)}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    def process_frame(self)-> Dict[str,Optional[List[Tuple[float,float,float]]]]:
            """
            Capture and process a single frame. 
        x    Returns: 
            {"detected":bool,
            "landmarks": List[(x,y,z)] or None,
            "hand_label": "Right" or None
            }
            """
            success,frame = self.cap.read()
            if not success:
                return {"detected": False,"landmarks":None,"hand_label":None}
            frame = cv2.flip(frame,1) # Mirror view
            rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            right_hand_landmarks =None

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks,handedness in zip(results.multi_hand_landmarks,results.multi_handedness,):

                    label = handedness.classification[0].label # "left" or "Right"
                    if label=="Right":
                        right_hand_landmarks =hand_landmarks
                        break

            fps = self._calculate_fps()

            if self.enable_visualization:
                self._draw_debug(frame,right_hand_landmarks,fps)
                cv2.imshow("Hand Tracker- Debug",frame)
                cv2.waitKey(1)

            if right_hand_landmarks:
                landmarks = self._extract_landmarks(right_hand_landmarks)
                return{
                    "detected":True,
                    "landmarks":landmarks,
                    "hand_label":"Right",
                }
            return {"detected":False, "landmarks":None,"hand_label":None}
        
    def release(self)->None:
        """Release camera and close windows safely."""
        self.cap.release()
        cv2.destroyAllWindows()









