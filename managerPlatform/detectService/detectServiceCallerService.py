from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.serviceCaller.detValServiceImpl import detectThreadMap


class detectServiceCallerService:


    def detectImage(self,dtsServiceKey,dtsSecret,threshold,imgData):
        FileNewName = fileUtils.getRandomName(imgData.filename)
        savedPath = ConstantUtils.singleImgDetectSource + FileNewName
        print("图片保存路径：" + savedPath)
        # 保存图片
        imgData.save(savedPath)

        # 获取当前的模型
        if detectThreadMap.keys().__contains__(dtsServiceKey):
            print("找到相关检测模型...")
            detectThread = detectThreadMap[dtsServiceKey]
            detectConfig = detectConfigUtils.getBasicDetectConfig(source=savedPath,
                                                                  outPath=ConstantUtils.singleImgDetectOut)
            detectResult = detectThread.detect(detectConfig)

            result = {
                "imagePath": ConstantUtils.imageItemPrefix + "singleImgDetectOut_" + FileNewName,
                "detectResult": detectResult
            }

            return resultPackerUtils.packCusResult(result)


