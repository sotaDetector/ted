import threading

from managerPlatform.bean.detectModel.detectModelTrainConfig import detectModelTrainConfig
from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.datasetsManager.datasetsService import datasetsService
from trainModelThread import trainModelThread

datasetService = datasetsService()

modelSavedBasePath=configUtils.getConfigProperties("model","modelSavePath")



class detectModelTrainService:


    def detectModelVersionTrain(self, jsonData):
        # 1.保存训练版本bean
        modelTrainVersion = detectModelTrainVersion.convertToBean(jsonData)
        modelTrainVersion.save()

        # 2.训练
        # 2.1. 准备数据
        trainDataDict,valDataDict = datasetService.loadTrainData(modelTrainVersion['ds_dl_list'])
        # 2.2 组装，保存 训练参数
        trainConfig=jsonData["advancedSet"]
        isUsePreTraindModel=trainConfig["isUsePreTraindModel"]
        modelDir=randomUtils.getRandomStr()
        modelTrainConfig=detectModelTrainConfig.getDetectModelTrainConfig(
            dmtvid=modelTrainVersion.dmtvid,
            cfg=ConstantUtils.getModelCfgPath(isUsePreTraindModel,modelTrainVersion.dmPrecision),
            weights=ConstantUtils.getModelWeightsPath(isUsePreTraindModel,modelTrainVersion.dmPrecision),
            epochs=trainConfig['epochs'],
            batch_size=trainConfig['batch_size'],
            project=modelSavedBasePath,
            name=modelDir
        )
        modelTrainConfig.save()
        # #2.3 开启训练线程
        trainModelTH=trainModelThread(trainDataDict,valDataDict,modelTrainConfig)
        trainModelTH.start()

        loggerUtils.info("start detect detectModel train thread [end]")
        return resultPackerUtils.save_success()


