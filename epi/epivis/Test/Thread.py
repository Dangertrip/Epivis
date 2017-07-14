import time
def a():
    print('HAHAHA')
    time.sleep(5)

import threading
t = threading.Thread(target=a)
print(t.is_alive())
t.start()
print(t.is_alive())
time.sleep(10)
print(t.is_alive())
t.join()
'''
False
HAHAHA
True
False
'''
