import json
import threading

from flask import session

from managerPlatform.bean.detectModel.detectModelBean import detectModelBean
from managerPlatform.bean.detectModel.detectModelTrainConfig import detectModelTrainConfig
from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.datasetsManager.datasetsService import datasetsService
from trainModelThread import trainModelThread

datasetService = datasetsService()





class detectModelTrainService:


    def detectModelVersionTrain(self, jsonData):
        # 1.保存训练版本bean
        modelTrainVersion = detectModelTrainVersion.convertToBean(jsonData)
        modelTrainVersion.save()

        # 更新该模型最新版本
        detectModelItem = detectModelBean.objects(dmId=jsonData['dmid'], state=ConstantUtils.DATA_STATUS_ACTIVE)
        detectModelItem.update(latestVersionId=modelTrainVersion.dmtvid)
        # 2.训练
        # 2.1. 准备数据
        trainDataDict,valDataDict = datasetService.loadTrainData(modelTrainVersion.dmtvid,modelTrainVersion['ds_dl_list'])
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
            project=ConstantUtils.modelBasePath,
            name=modelDir
        )
        modelTrainConfig.save()
        # #2.3 开启训练线程
        trainModelTH=trainModelThread(trainDataDict,valDataDict,modelTrainConfig)
        trainModelTH.start()

        #3.更新模型路径
        ckptModel,entireModel=fileUtils.getModelSavePath(ConstantUtils.modelBasePath,modelDir)
        modelTrainVersion.update(ckptModelSavePath=ckptModel,entireModelSavePath=entireModel)



        loggerUtils.info("start detect detectModel train thread [end]")
        return resultPackerUtils.save_success()


    def getDMVersionList(self,queryData):
        dataList = detectModelTrainVersion.objects(dmid=queryData['dmid'], state=ConstantUtils.DATA_STATUS_ACTIVE)\
            .exclude("state","create_date").order_by('-create_date')

        datasetIdNames = datasetsBean.objects(userId=session.get("userId"), state=ConstantUtils.DATA_STATUS_ACTIVE).only(
            "dsId", "dsName")
        datasetMap = {}
        for item in datasetIdNames:
            datasetMap[item['dsId']] = item['dsName']

        modelVersionJsonList = json.loads(dataList.to_json().replace("_id", "dmtvid"))
        for versionItem in modelVersionJsonList:
            versionItem['trainState'] = ConstantUtils.getModelVersionTrainState(versionItem['trainState'])
            versionItem['inferencePlatformValue'] = ConstantUtils.getModelPlatform(versionItem['inferencePlatform'])
            versionItem['dmPrecisionValue'] = ConstantUtils.getModelPrisision(versionItem['dmPrecision'])
            datasetNames = []
            for item in versionItem['ds_dl_list']:
                datasetNames.append(datasetMap[item['dsId']])
            versionItem['datasetNames'] = datasetNames

        return resultPackerUtils.packJsonListResults(modelVersionJsonList)


    def getDetectModelVersionNameList(self,queryData):
        dataList=detectModelTrainVersion.objects(dmid=queryData['dmid'],state=ConstantUtils.DATA_STATUS_ACTIVE).only("dmtvid","dmtvName")
        return resultPackerUtils.packDataListResults(dataList.to_json(),"dmtvid")



    def getDMVersionDetail(self,queryData):
        dataItem=detectModelTrainVersion.objects(dmtvid=queryData['dmtvid'],state=ConstantUtils.DATA_STATUS_ACTIVE).exclude("state","create_date")

        return resultPackerUtils.packDataItemResults(dataItem.to_json(),"dmtvid")


    def getDMVersionBean(self,dmtvid):
        dataItem=detectModelTrainVersion.objects(dmtvid=dmtvid,state=ConstantUtils.DATA_STATUS_ACTIVE).exclude("state","create_date")

        return dataItem



    def delDMVersion(self,queryData):
        modelVersion = detectModelTrainVersion.objects(dmtvid=queryData['dmtvid'])
        modelVersion.update(state=ConstantUtils.DATA_STATUS_DELETED)
        return resultPackerUtils.update_success()





