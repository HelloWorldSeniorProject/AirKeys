from util.internal_clock import InternalClock
from util.test import Test
from threading import Thread

def main():
    ic = InternalClock()
    test = Test()
    
    t1 = Thread(target=test.run)
    t2 = Thread(target=ic.run)
    
    t1.start()
    t2.start()
    
if __name__ == "__main__":
    main()