from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.dataManager.redisSource import redisClient
from managerPlatform.common.keyGen.keyGenarator import keyGenarator


class heartBeatService:


    def sendDetectHeartbeat(self,jsonData):

        for i in jsonData['sessionIds'].split(","):
            if i != "":
                redisClient.hset(keyGenarator.getDetectWatchKey(), i, str(dateUtils.getTimeStamp()))

        return resultPackerUtils.save_success()




