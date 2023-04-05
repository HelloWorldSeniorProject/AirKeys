import threading

class Singleton(type):
    """ A thread-safe implementation of Sinlgeton pattern for 'shared' resources.
    
    
    """
    
    __instances = {}
    __thread_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        