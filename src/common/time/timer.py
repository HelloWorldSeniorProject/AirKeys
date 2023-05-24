import threading

class Timer(threading.Timer):
    
    def __init__(self, limit: int, task: callable, start_time: int):
        super(Timer, self).__init__(interval=limit, function=task)
        self._start_time = start_time
        self._limit = limit
        self.start()
    
    def get_remaining_time(self) -> float:
        # get around circular import errors
        from common.time.internal_clock import InternalClock
        
        clock = InternalClock()
        elapsed_time = (clock.get_time_ms() - self._start_time ) / 1000
        remaining_time = round((self._limit - elapsed_time), 3)
        return remaining_time if remaining_time > 0 else 0
        

    
    
    