import threading

# a lock that allows only one thread to access the resource it "locks".
thread_lock = threading.Lock()

class Singleton(type):
    """A thread-safe implementation of Sinlgeton pattern for 'shared' resources.
    
    Typical usage will be as a parent class using polymorphism and Python's support for 
    passing variables via the \*args and \*\*kwargs special keywords. Utilizes threading
    standard package to prevent the edge case where multiple threads attempt to create the same
    singleton object at the same time(race condition).
    
    Args:
        _instances: A dictionary of instances with the Singleton class as its parent class.
    """
    
    _instances = {}
    
    
    def __call__(cls, *args, **kwargs):
        """Initializes or returns available singleton objects.
        
        Args:
            \*args: any amount of arguments of any type that are non-named.
            \*\*kwargs: any amount of arguments of any type that are named.
            
        Note: Utilizes the double-checked locking method.
        """
        if cls not in cls._instances:   # check for object before locking.
            with thread_lock:   # lock Singleton class / prevent concurrent access
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs) # create instance and store in dict
        
        return cls._instances[cls]  # return instance if available/once created