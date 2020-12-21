import threading
import time

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.yoloService.yoloDetectService import yoloDetectThreadMap,yoloDetectService

yoloDetectService=yoloDetectService()



class detectThreadWatcher(threading.Thread):


    @classmethod
    def releaseDetectSession(cls,serviceSessionId):
        #释放线程
        if yoloDetectThreadMap.keys().__contains__(serviceSessionId):
            if yoloDetectService.releaseYoloDetectThread(serviceSessionId):
                #从map中移除
                ConstantUtils.detectSessionMap.pop(serviceSessionId)
        else:
            ConstantUtils.detectSessionMap.pop(serviceSessionId)


    def __init__(self):
        threading.Thread.__init__(self)
        loggerUtils.info("detect thread资源监控线程已开启....")

    def run(self):
        while(True):
            time.sleep(10)
            sessionMap=ConstantUtils.detectSessionMap
            nowTimeStamp=dateUtils.getTimeStamp()
            loggerUtils.info("detect session thread map:"+str(sessionMap))
            for sessionKey in list(sessionMap.keys()):
                if nowTimeStamp-(10*1000)>int(sessionMap[sessionKey]):
                    detectThreadWatcher.releaseDetectSession(sessionKey)


