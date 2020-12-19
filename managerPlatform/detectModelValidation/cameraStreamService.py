from managerPlatform.common.commonUtils.ffmpegUtils import ffmpegUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.yoloService.yoloDetectService import yoloDetectService

yoloDetect=yoloDetectService()



class cameraStreamService:

    def getCameraDeviceList(self):
        return resultPackerUtils.packJsonListResults(ffmpegUtils.getCameraList())

    def startNativeCameraDetect(self,config):

        return yoloDetect.createYoloDetectThread(config)


    def startLiveStreamDetect(self,config):

        return yoloDetect.createYoloDetectThread(config)


    def stopNativeCameraDetect(self, jsonData):

        sessionId = jsonData['videoPlayId']

        yoloDetect.releaseYoloDetectThread(sessionId)

        return {"rs": 1}
