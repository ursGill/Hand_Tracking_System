from typing import Dict,List,Tuple

class FingerStateDetector:
    """
    Determines which fingers are UP or DOWN for a right hand based on MediaPipe landmarks
    """


    THUMB_TIP = 4
    THUMB_IP = 3

    INDEX_TIP = 8
    INDEX_PIP = 6

    MIDDLE_TIP = 12
    MIDDLE_PIP = 10

    RING_TIP = 16
    RING_PIP =14

    PINKY_TIP =20
    PINKY_PIP = 18

    def get_finger_states(self,landmarks: List[Tuple[float,float,float]])->Dict[str,int]:
        """
        Args: 
            landmarks: List of 21 (x,y,z) normalized coordinates

        Returns: 
            Dictionary of finger states(1=UP,0=DOWN)
        """
        if not landmarks or len(landmarks)!=21:
            raise ValueError("Invalid Landmarks input. Expected 21 points")
        states = {}


        #-- Thumb (Horizontal Check)--
        thumb_tip_x = landmarks[self.THUMB_TIP][0]
        thumb_ip_x = landmarks[self.THUMB_IP][0]
        states["thumb"]=1 if thumb_tip_x < thumb_ip_x else 0

        # --other Fingers (Vertical Check)--
        def finger_up(tip_idx:int,pip_idx:int)->int:
            tip_y = landmarks[tip_idx][1]
            pip_y = landmarks[pip_idx][1]
            return 1 if tip_y < pip_y else 0
        
        states["index"] = finger_up(self.INDEX_TIP,self.INDEX_PIP)
        states["middle"] = finger_up(self.MIDDLE_TIP,self.MIDDLE_PIP)
        states["ring"]= finger_up(self.RING_TIP,self.RING_PIP)
        states["pinky"] = finger_up(self.PINKY_TIP,self.PINKY_PIP)

        return states



