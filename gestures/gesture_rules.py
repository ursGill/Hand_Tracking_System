from typing import Dict,List,Tuple,Optional
import math


class GestureRuleEngine:
    """
    Converts finger states and landmarks into high-level gesture labels.
    Right-Hand only (phase 1)
    """

    PINCH_THRESHOLD = 0.04 # Tunable
    DRAG_ACTIVE = False

    THUMB_TIP = 4
    INDEX_TIP = 8

    def _distance(self,p1:Tuple[float,float,float],p2: Tuple[float,float,float],)->float:
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    
    def classify_gesture(self,landmarks: List[Tuple[float,float,float]],finger_states: Dict[str,int],)->str:

        thumb = finger_states["thumb"]
        index = finger_states["index"]
        middle = finger_states["middle"]
        ring = finger_states["ring"]
        pinky = finger_states["pinky"]


        # --- Pinch for click ---
        pinch_distance = self._distance(landmarks[self.THUMB_TIP],landmarks[self.INDEX_TIP],)

        if index==1 and pinch_distance<self.PINCH_THRESHOLD:
            return "CLICK"
        
        # --- Drag(fist) ---
        if thumb== index==middle==ring==pinky==0:
            if not self.DRAG_ACTIVE:
                self.DRAG_ACTIVE = True
                return "DRAG_START"
            return "DRAGGING"
        
        # --- Release Drag ---
        if self.DRAG_ACTIVE and all(v==1 for v in finger_states.values()):
            self.DRAG_ACTIVE = False
            return "DRAG_END"
        
        # --- Move (index only)---
        if index==1 and middle==ring==pinky==0:
            return "MOVE"
        return "NONE"

