import time

class Clock:
    def __init__(self, start: bool = False):
        self.start_time = time.time() if start else None

    # difference between time_elapsed and time.sleep is that I can check if certain time has passed whereas sleep just pauses the code for this amount of time
    
    def time_elapsed(self, seconds: int = 0) -> bool:
        current_time = time.time()
        if self.start_time is None or current_time - self.start_time > seconds:
            self.start_time = current_time
            return True
        return False