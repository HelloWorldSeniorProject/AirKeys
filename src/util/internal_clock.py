import time

class InternalClock:
    
    def __init__(self):
        self.start_time = time.process_time()
        
    
    def run(self):
        print(self.start_time)
        for i in range(10):
            print("Curr CPU TIME", time.process_time())
            time.sleep(1)
        print(self.start_time)
        