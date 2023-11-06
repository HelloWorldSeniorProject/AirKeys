from common.time.internal_clock import InternalClock
from common.types import *
from test.swte import *
from time import sleep


class Test_InternalClock:
    @requirements(2.1)
    def test_singleton(self):
        large_banner("Test Singleton: Tests singleton inheritence")

        exps_met = []

        ic1 = InternalClock()
        ic2 = InternalClock()
        exps_met.append(ic1 is ic2)

        ic3 = InternalClock()
        exps_met.append(ic1 is ic2 is ic3)

        assert all(exps_met)

    @requirements(2.2)
    def test_get_time(self):
        large_banner("Test Get Time: Tests time tracking functions")
        exps_met = []

        ic = InternalClock()

        # second format
        small_banner("Sleep for 5 seconds")
        time1 = ic.get_time()
        small_banner(f"Start time : {time1}")
        sleep(5)
        time2 = ic.get_time()
        small_banner(f"End time : {time2}")
        # may be more than exactly 10 seconds due to thread locking
        exps_met.append((time2 - time1) >= 5)

        # millisecond format
        small_banner("Sleep for 5 seconds")
        time1 = ic.get_time_ms()
        small_banner(f"Start time : {time1}")
        sleep(5)
        time2 = ic.get_time_ms()
        small_banner(f"End time : {time2}")

        exps_met.append((time2 - time1) >= 5000)
        assert all(exps_met)

    @conditional
    @requirements(12.1, 12.2)
    # Verify by inspection.
    def test_create_timer(self):
        large_banner("Test Create Timer: Tests timer creation functions")
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

    @requirements(12.3)
    def test_timer_remaining_time(self):
        large_banner("Test Timer Remaining Time: Tests Timer's remaining timing function")
        ic = InternalClock()
        timer = ic.create_timer(5, lambda: small_banner("Timer rang!"))
        exps_met = []

        small_banner("Verify timer returns expected remaining time at set intervals (1s)")
        for i in range(4):
            last_time = timer.get_remaining_time()
            sleep(1)

            # account for varying hardware speeds.
            exps_met.append(last_time >= timer.get_remaining_time() + 0.95)

        # ensure timer finished before test ends
        timer.join()

        assert all(exps_met)
