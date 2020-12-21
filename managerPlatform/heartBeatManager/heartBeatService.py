from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.watcherMangaer.detectThreadWatcher import detectThreadWatcher


class heartBeatService:


    def sendDetectHeartbeat(self,jsonData):

        for sessionItem in jsonData['sessionIds'].split(","):
            if sessionItem != "":
                detectThreadWatcher.updateDetectSessionTime(sessionItem)

        return resultPackerUtils.save_success()




