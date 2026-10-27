import pyautogui as pg
from typing import Tuple
import time

class WindowsMouseController:
    """
    Controls mouse actions on Windows using gesture input 
    """

    def __init__(self,smoothing:float=0.2)->None:
        self.screen_width,self.screen_height=pg.size()
        self.prev_x,self.prev_y =0,0
        self.smoothing = smoothing
        self.dragging = False
        self.last_vol_time = 0.0
        self.last_click_time = 0.0
        self.last_play_time = 0.0

        pg.FAILSAFE =False # Prevent crash if cursor hits corner

    def _smooth(self, new_x: float, new_y: float):
        dx = abs(new_x - self.prev_x)
        dy = abs(new_y - self.prev_y)
        movement = dx + dy
    
    # Enhanced Non-linear adaptive smoothing (Tuned for lower sensitivity/more stability)
        if movement < 5:
            alpha = 0.05    # Extreme smoothing for sniper-like micro-accuracy
        elif movement < 20:
            alpha = 0.1     # Smooth regular tracking
        elif movement < 50:
            alpha = 0.25    # Responsive tracking
        else:
            alpha = 0.4     # Max sensitivity for fast flicks (capped to prevent wild jumps)

        smooth_x = self.prev_x + (new_x - self.prev_x) * alpha
        smooth_y = self.prev_y + (new_y - self.prev_y) * alpha

        self.prev_x, self.prev_y = smooth_x, smooth_y
        return int(smooth_x), int(smooth_y)
    
    def move_cursor(self,norm_x:float,norm_y:float)->None:
        """
        Move cursor using normalized coordinates(0-1).
        Maps an inner active region to the full screen for wide-area ease of use.
        """
        # Reduced margin to 0.15 to lower sensitivity. 
        # Maps the inner 70% of the camera directly to 100% of the screen.
        margin_x = 0.15
        margin_y = 0.15

        mapped_x = max(0, min(1, (norm_x - margin_x) / (1 - 2 * margin_x)))
        mapped_y = max(0, min(1, (norm_y - margin_y) / (1 - 2 * margin_y)))

        target_x = mapped_x * self.screen_width
        target_y = mapped_y * self.screen_height
        x,y =self._smooth(target_x,target_y)
        pg.moveTo(x,y)

    def left_click(self)->None:
        if time.time() - self.last_click_time > 0.6:
            pg.click()
            self.last_click_time = time.time()

    def start_drag(self)->None:
        if not self.dragging:
            pg.mouseDown()
            self.dragging =True
        
    def end_drag(self)->None:
        if self.dragging:
            pg.mouseUp()
            self.dragging= False

    def media_play_pause(self)->None:
        if time.time() - self.last_play_time > 1.0:
            # 'k' is the universal play/pause shortcut for YouTube, works regardless of focus!
            pg.press("k")
            self.last_play_time = time.time()

    def volume_up(self)->None:
        if time.time() - self.last_vol_time > 0.1:
            pg.press("volumeup")
            self.last_vol_time = time.time()

    def volume_down(self)->None:
        if time.time() - self.last_vol_time > 0.1:
            pg.press("volumedown")
            self.last_vol_time = time.time()