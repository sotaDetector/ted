from managerPlatform.yoloService.yoloDetectService import yoloDetectService

yoloDetectService=yoloDetectService()

class detValServiceImpl:

    def launchDetectService(self,jsonData):

        return yoloDetectService.launchYoloDetectService(dmtvid=jsonData['dmtvid'])