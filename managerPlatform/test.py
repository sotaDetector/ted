import threading
import time


def showMsg():

    while(True):
        print("...................\r\n")
        time.sleep(1)

t1=threading.Thread(target=showMsg)
t1.setDaemon(True)
t1.start()
print("-----")
t1.join(timeout=10)
print("finish")

