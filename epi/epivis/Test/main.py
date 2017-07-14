import time
from module import cal1
#cal1()
#cal1()
#print(cal1())
#cal1()
def a():
    time.sleep(3)
#    from module import cal1
    print("I'm in!")
    time.sleep(1)
    cal1()

import threading
t = threading.Thread(target=a)
s = threading.Thread(target=a)
t.start()
s.start()
t.join()
s.join()

