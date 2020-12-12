import os

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.serviceCaller.detectServiceImpl import detectThreadMap


class imageDetectService:

    def getSingleImageDetectResult(self,serviceSessionId,threshold,imgData):

        FileNewName=fileUtils.getRandomName(imgData.filename)
        savedPath=ConstantUtils.singleImgDetectSource+FileNewName
        print("图片保存路径："+savedPath)
        #保存图片
        imgData.save(savedPath)

        #获取当前的模型
        if detectThreadMap.keys().__contains__(serviceSessionId):
            print("找到相关检测模型...")
            detectThread=detectThreadMap[serviceSessionId]
            detectConfig=detectConfigUtils.getBasicDetectConfig(source=savedPath,outPath=ConstantUtils.singleImgDetectOut)
            detectThread.detect(detectConfig)

            result={
                "imagePath":ConstantUtils.imageItemPrefix+"singleImgDetectOut_"+FileNewName
            }

            return resultPackerUtils.packCusResult(result)
















