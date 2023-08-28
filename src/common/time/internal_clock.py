import threading
import time
from common.patterns.singleton import Singleton
from common.time.timer import Timer
from util.logger import get_logger

logger = get_logger("internal_clock.log")

thread_lock = threading.Lock()


class InternalClock(metaclass=Singleton):
    """A monotonic clock for use across the system.

    Internal Clock is a singleton class that functions for determining relational times
    throughout the system. Utilizes thread locks to prevent concurrent access to CPU
    hardware clocks.
    """

    def __init__(self):
        """Initializes the instance and saves the initialization time."""
        logger.info("Initializing internal clock.")
        with thread_lock:
            self._init_time = round(time.perf_counter(), 3)
        logger.info("Initialization complete.")

    def get_time(self) -> float:
        """Fetches the total time system time since boot.

        Returns:
            A float representing the system time in seconds rounded to the nearest ms.
        """
        time = self._get_sys_time()
        return time

    def get_time_ms(self) -> int:
        """Fetches the total time system time since boot.

        Returns:
            An integer representing the system time in ms.
        """

        time = int(self._get_sys_time() * 1000)
        return time


    def _get_sys_time(self) -> float:
        """Fetches the total time system time since boot.

        Note:
            See get_time() for external use.

        Returns:
            A float representing the system time in seconds rounded to the nearest ms.
        """
        try:
            with thread_lock:
                return round((time.perf_counter() - self._init_time), 3)
        except Exception as e:
            logger.error(f"Failed to get time. \n{e}")
            return float(0)


    def create_timer(self, limit: int, task: callable) -> Timer:
        """Creates an object that calls specified passed task after specified time duration, in
        seconds, has passed.

        Args:
            limit : the amount of time, in seconds, before the task should execute.
            task : a callable function or instructions to run once the time limit has been reached.

        Returns:
            A configured Timer object.
        """
        try:
            timer = Timer(limit=limit, task=task, start_time=self.get_time_ms())
            return timer
        except Exception as e:
            logger.error(f"Failed to create timer. \n{e}")
            return None

    def create_timer_ms(self, limit: int, task: callable) -> Timer:
        """Creates an object that calls specified passed task after specified time duration, in
        milliseconds, has passed.

        Args:
            limit : the amount of time, in milliseconds, before the task should execute.
            task : a callable function or instructions to run once the time limit has been reached.

        Returns:
            A configured Timer object.
        """
        return self.create_timer(limit=round((limit / 1000), 3), task=task)
