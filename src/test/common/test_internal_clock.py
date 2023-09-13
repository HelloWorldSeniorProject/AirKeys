from common.time.internal_clock import InternalClock
from common.types import *
from test.swte import large_banner, small_banner
from time import sleep


def test_internal_clock_singleton():
    large_banner("Test Internal Clock Singleton: Tests Internal Clock's singleton inheritence")

    ic1 = InternalClock()
    ic2 = InternalClock()
    assert ic1 is ic2

    ic3 = InternalClock()
    assert ic1 is ic2 is ic3


def test_get_time():
    large_banner("Test Get Time: Tests Internal Clock's time tracking functions")

    ic = InternalClock()

    # second format
    small_banner("Sleep for 5 seconds")
    time1 = ic.get_time()
    small_banner(f"Start time : {time1}")
    sleep(5)
    time2 = ic.get_time()
    small_banner(f"End time : {time2}")
    # may be more than exactly 10 seconds due to thread locking
    assert (time2 - time1) >= 5

    # millisecond format
    small_banner("Sleep for 5 seconds")
    time1 = ic.get_time_ms()
    small_banner(f"Start time : {time1}")
    sleep(5)
    time2 = ic.get_time_ms()
    small_banner(f"End time : {time2}")

    assert (time2 - time1) >= 5000


def test_create_timer():
    large_banner("Test Create Timer: Tests Internal Clock's timer creation functions")
    ic = InternalClock()

    # create time using seconds. Observe
    timer1 = ic.create_timer(4, lambda: small_banner("Timer 1 rang!"))
    small_banner("Sleep for 5 seconds")
    sleep(5)
    small_banner("Timer 1 task should run before this line")
    timer2 = ic.create_timer_ms(4000, lambda: small_banner("Timer 2 rang!"))
    small_banner("Sleep for 5 seconds")
    sleep(5)
    small_banner("Timer 2 task should run before this line")


def test_timer_remaining_time():
    large_banner("Test Create Timer: Tests Timer's remaining timing function")

    # relies on visual confirmation
    ic = InternalClock()
    timer = ic.create_timer(5, lambda: small_banner("Timer rang!"))

    for i in range(5):
        small_banner(f"Remaining time : {timer.get_remaining_time()}")
        sleep(1)
