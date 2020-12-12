import os

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils


class imageDetectService:

    def getSingleImageDetectResult(self,dmId,threshold,imgData):
        singleDetectBasePath=ConstantUtils.singleImgDetect
        if not os.path.exists(singleDetectBasePath):
            os.mkdir(singleDetectBasePath)
        savedPath=singleDetectBasePath+fileUtils.getRandomName(imgData.filename)
        print(savedPath)

        imgData.save(savedPath)











