import threading
import time

from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.dataManager import redisSource
from managerPlatform.common.keyGen.keyGenarator import keyGenarator
from managerPlatform.serviceCaller.cameraStreamService import detectMap


class detectThreadWatcher(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print("检测线程开启....")

    def run(self):
        while(True):
            time.sleep(5)
            print("-------------")
            sessMap=redisSource.redisPool.hgetall(keyGenarator.getDetectWatchKey())
            nowTimeStamp=dateUtils.getTimeStamp()
            for i in sessMap:
                if nowTimeStamp-(10*1000)>int(sessMap[i]):
                    print(i)
                    if not detectMap.keys().__contains__(str(i,'utf-8')):
                        redisSource.redisPool.hdel(keyGenarator.getDetectWatchKey(),i)
                    else:
                        detectMap[str(i,'utf-8')].stopDetect()


