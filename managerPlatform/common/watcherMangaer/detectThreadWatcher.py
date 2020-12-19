import threading
import time

from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.dataManager import redisSource
from managerPlatform.common.keyGen.keyGenarator import keyGenarator
from managerPlatform.yoloService.yoloDetectService import yoloDetectThreadMap,yoloDetectService

yoloDetectService=yoloDetectService()

class detectThreadWatcher(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        loggerUtils.info("检测资源监控线程开启....")

    def run(self):
        while(True):
            time.sleep(10)
            sessMap=redisSource.redisClient.hgetall(keyGenarator.getDetectWatchKey())
            nowTimeStamp=dateUtils.getTimeStamp()
            loggerUtils.info("now sessions:"+str(sessMap))
            for i in sessMap:
                if nowTimeStamp-(10*1000)>int(sessMap[i]):
                    if not yoloDetectThreadMap.keys().__contains__(str(i,'utf-8')):
                        print("delete session id"+str(i))
                        redisSource.redisClient.hdel(keyGenarator.getDetectWatchKey(),i)
                    else:
                        yoloDetectService.releaseYoloDetectThread(str(i,'utf-8'))


