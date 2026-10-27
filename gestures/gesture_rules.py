import time
import math
from typing import Dict, List, Tuple


class GestureRuleEngine:
    RELATIVE_PINCH_THRESHOLD = 0.4
    CLICK_COOLDOWN = 0.6  # seconds

    

    THUMB_TIP = 4
    INDEX_TIP = 8
    INDEX_MCP = 5
    WRIST = 0

    def __init__(self) -> None:
        self.drag_active = False
        self.last_click_time = 0.0

    def _distance(
        self,
        p1: Tuple[float, float, float],
        p2: Tuple[float, float, float],
    ) -> float:
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def classify_gesture(
        self,
        landmarks: List[Tuple[float, float, float]],
        finger_states: Dict[str, int],
    ) -> str:

        thumb = finger_states["thumb"]
        index = finger_states["index"]
        middle = finger_states["middle"]
        ring = finger_states["ring"]
        pinky = finger_states["pinky"]

        # ---- CLICK (pinch with cooldown) ----
        pinch_distance = self._distance(
            landmarks[self.THUMB_TIP],
            landmarks[self.INDEX_TIP],
        )

        hand_size = self._distance(
            landmarks[self.WRIST],
            landmarks[self.INDEX_MCP],
        )
        relative_pinch = pinch_distance / hand_size if hand_size > 0 else float('inf')

        current_time = time.time()
        # Remove 'index == 1' because when pinching, the index finger often reads as '0' (curled).
        # We also ensure it's not a closed fist (which is for dragging).
        is_fist = (thumb == 0 and index == 0 and middle == 0 and ring == 0 and pinky == 0)
        
        if (
            relative_pinch < self.RELATIVE_PINCH_THRESHOLD
            and not is_fist
        ):
            return "CLICK"

        # ---- DRAG ----
        if thumb == index == middle == ring == pinky == 0:
            if not self.drag_active:
                self.drag_active = True
                return "DRAG_START"
            return "DRAGGING"

        # ---- DRAG END ----
        if self.drag_active and all(v == 1 for v in finger_states.values()):
            self.drag_active = False
            return "DRAG_END"

        # ---- PLAY / PAUSE (Peace Sign) ----
        if index == 1 and middle == 1 and thumb == 0 and ring == 0 and pinky == 0:
            return "PLAY_PAUSE"

        # ---- VOLUME UP (Index + Pinky Up / Rock Sign) ----
        if index == 1 and pinky == 1 and thumb == 0 and middle == 0 and ring == 0:
            return "VOLUME_UP"

        # ---- VOLUME DOWN (Thumb + Pinky / Shaka) ----
        if pinky == 1 and thumb == 1 and index == 0 and middle == 0 and ring == 0:
            return "VOLUME_DOWN"

        # ---- MOVE ----
        if index == 1 and middle == 0 and ring == 0 and pinky == 0:
            return "MOVE"

        return "NONE"