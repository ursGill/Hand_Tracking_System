from collections import deque

class GestureBuffer:
    """
    Stabilizes gestures by requiring consistency across frames. 
    """

    def __init__(self,buffer_size:int=5):
        self.buffer = deque(maxlen=buffer_size)
    
    def update(self,gesture:str)->str:
        self.buffer.append(gesture)

        # Better sensitivity: use majority vote instead of requiring 100% identical frames
        from collections import Counter
        most_common, count = Counter(self.buffer).most_common(1)[0]
        
        # If the gesture appears in at least >50% of the buffer, accept it
        if count >= len(self.buffer) // 2 + 1:
            return most_common
        return "NONE"