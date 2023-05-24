import threading

class Timer(threading.Timer):
    """A mechanism for executing a set of instructions after waiting a specified amount of time.
    
    The timer class is a child class of the threading.Timer class with minor added functionality.
    With every new object, a new thread is created, ensuring the specified task will execute regarldless of
    the main system thread.
    """
    
    def __init__(self, limit: int, task: callable, start_time: int):
        """Initializes the instance and saves the initialization time. 
        
        Args:
            limit : the amount of time, in seconds, before the task should execute.
            task : a callable function or instructions to run once the time limit has been reached.
            start_time : the system time the object was created.
        """
        super(Timer, self).__init__(interval=limit, function=task)
        self._start_time = start_time
        self._limit = limit
        self.start()
    
    def get_remaining_time(self) -> float:
        """Fetches remaining time on timer. 
        
        Returns:
            A float representing the remaining time, in seconds, the timer will wait before 
            executing task.
        """
        # get around circular import errors
        from common.time.internal_clock import InternalClock
        
        clock = InternalClock()
        elapsed_time = (clock.get_time_ms() - self._start_time ) / 1000
        remaining_time = round((self._limit - elapsed_time), 3)
        return remaining_time if remaining_time > 0 else 0
        

    
    
    