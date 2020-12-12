import os

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.serviceCaller.detectServiceImpl import detectThreadMap


class imageDetectService:

    def getSingleImageDetectResult(self,serviceSessionId,threshold,imgData):
        singleDetectBasePath=ConstantUtils.singleImgDetect
        if not os.path.exists(singleDetectBasePath):
            os.mkdir(singleDetectBasePath)
        savedPath=singleDetectBasePath+fileUtils.getRandomName(imgData.filename)

        #获取当前的模型
        if detectThreadMap.keys().__contains__(serviceSessionId):
            detectThread=detectThreadMap[serviceSessionId]
            detectConfig={}
            detectThread.detect(detectConfig)

        imgData.save(savedPath)











