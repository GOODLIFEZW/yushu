import time

from werkzeug.local import LocalStack
import threading
ls = LocalStack()
ls.push(1)

def worker():
    print('thread1 before push', ls.top)
    ls.push(2)
    print('thread1 after push', ls.top)

thread1 = threading.Thread(target=worker)
thread1.start()
time.sleep(1)
print('main', ls.top)


