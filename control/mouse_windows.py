import pyautogui as pg
from typing import Tuple

class WindowsMouseController:
    """
    Controls mouse actions on Windows using gesture input 
    """

    def __init__(self,smoothing:float=0.2)->None:
        self.screen_width,self.screen_height=pg.size()
        self.prev_x,self.prev_y =0,0
        self.smoothing = smoothing
        self.dragging = False

        pg.FAILSAFE =False # Prevent crash if cursor hits corner

    def _smooth(self,new_x:float,new_y:float)->Tuple[int,int]:
        smooth_x = self.prev_x+(new_x-self.prev_x)*self.smoothing
        smooth_y = self.prev_y +(new_y - self.prev_y)*self.smoothing

        self.prev_x,self.prev_y = smooth_x,smooth_y
        return int(smooth_x), int(smooth_y)
    
    def move_cursor(self,norm_x:float,norm_y:float)->None:
        """
        Move cursor using normalized coordinates(0-1).
        """

        target_x = norm_x*self.screen_width
        target_y = norm_y* self.screen_height
        x,y =self._smooth(target_x,target_y)
        pg.moveTo(x,y)

    def left_click(self)->None:
        pg.click()

    def start_drag(self)->None:
        if not self.dragging:
            pg.mouseDown()
            self.dragging =True
        
    def end_drag(self)->None:
        if self.dragging:
            pg.mouseUp()
            self.dragging= False