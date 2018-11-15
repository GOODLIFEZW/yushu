import threading
import time


def worker():
    t1obj = threading.current_thread()
    time.sleep(1000)
    print(t1obj.getName())


t1 = threading.Thread(target=worker)
t1.start()

t = threading.current_thread()
print(t.getName())
