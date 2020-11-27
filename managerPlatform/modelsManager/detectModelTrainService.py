import threading

from managerPlatform.bean.detectModelTrainConfig import detectModelTrainConfig
from managerPlatform.bean.detectModelVersion import detectModelTrainVersion
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.datasetsManager.datasetsService import datasetsService
from trainCustom import trainYolo

datasetService = datasetsService()

modelSavedBasePath=configUtils.getConfigProperties("model","modelSavePath")



class detectModelTrainService:


    def detectModelVersionTrain(self, jsonData):
        # 1.保存训练版本bean
        modelTrainVersion = detectModelTrainVersion.convertToBean(jsonData)
        modelTrainVersion.save()

        # 2.训练
        # 2.1. 准备数据
        datasetDict = datasetService.loadTrainData(modelTrainVersion['ds_dl_list'])
        # 2.2 组装，保存 训练参数
        trainConfig=jsonData["advancedSet"]
        modelDir=randomUtils.getRandomStr()
        trainConfig=detectModelTrainConfig.getDetectModelTrainConfig(
            dmtvid=modelTrainVersion.dmtvid,
            weights=ConstantUtils.getModelWeightsPath(modelTrainVersion.dmPrecision),
            epochs=trainConfig['epochs'],
            batch_size=trainConfig['batch_size'],
            project=modelSavedBasePath,
            name=modelDir
        )
        trainConfig.save()
        # #2.3 开启训练线程
        self.startTrainThread(datasetDict,trainConfig)

        return resultPackerUtils.save_success()


    def startTrainThread(self,datasetDict, trainConfig):
        loggerUtils.info("start detect model train thread [start]")
        t1 = threading.Thread(target=trainYolo, args=(datasetDict, trainConfig))
        t1.setDaemon(True)
        t1.start()
        loggerUtils.info("start detect model train thread [end]")