from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.yoloService.yoloDetectService import yoloDetectService

yoloDetectServiceImpl=yoloDetectService()


class detectServiceCallerService:


    def detectImage(self,dtsServiceKey,dtsSecret,threshold,imgData):
        FileNewName = fileUtils.getRandomName(imgData.filename)
        savedPath = ConstantUtils.singleImgDetectSource + FileNewName
        print("图片保存路径：" + savedPath)
        # 保存图片
        imgData.save(savedPath)

        # 获取当前的模型
        detectIns=yoloDetectServiceImpl.getDetectServiceInstance(dtsServiceKey)
        if detectIns is not None:
            print("找到相关检测模型...")
            detectConfig = detectConfigUtils.getBasicDetectConfig(source=savedPath,
                                                                  outPath=ConstantUtils.singleImgDetectOut)
            detectResult = detectIns.detect(detectConfig)

            result = {
                "imagePath": ConstantUtils.imageItemPrefix + "singleImgDetectOut_" + FileNewName,
                "detectResult": detectResult
            }

            return resultPackerUtils.packCusResult(result)
        else:
            return resultPackerUtils.packErrorMsg(resultPackerUtils.EC_NO_EVALUATE_SESSION)




