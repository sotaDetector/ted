from managerPlatform.bean.serviceCallerBeans.detectRecord import detectRecord
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.yoloService.yoloDetectService import yoloDetectService

yoloDetect = yoloDetectService()

class videoDetectService:

    def getVideoDetectResult(self, serviceSessionId, threshold, detectVideo):

        FileNewName = fileUtils.getRandomName(detectVideo.filename)
        savedPath = ConstantUtils.videoDetectSource + FileNewName
        loggerUtils.info("视频保存路径：" + savedPath)
        # 保存图片
        detectVideo.save(savedPath)

        # 获取当前的模型
        detectServiceIns=yoloDetect.getDetectServiceInstance(serviceSessionId)
        if detectServiceIns is not None:
            loggerUtils.info("找到相关检测模型...")
            detectConfig = detectConfigUtils.getBasicDetectConfig(source=savedPath,
                                                                  outPath=ConstantUtils.videoDetectOut)
            detectServiceIns.detect(detectConfig)

            detectRecordItem=detectRecord(videoSavedPath=ConstantUtils.videoDetectOut+FileNewName)
            detectRecordItem.save()

            result = {
                ConstantUtils.videoPlayUrl:ConstantUtils.videoPlayPrefix+str(detectRecordItem.dereid)
            }

            return resultPackerUtils.packCusResult(result)
        else:

            return resultPackerUtils.packErrorMsg(resultPackerUtils.EC_NO_EVALUATE_SESSION)




