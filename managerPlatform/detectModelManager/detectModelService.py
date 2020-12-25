import json

from flask import session

from managerPlatform.bean.detectModel import detectModelVersion
from managerPlatform.bean.detectModel.detectModelBean import detectModelBean
from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class detectModelService:

    def addDetectModel(self, dataLabelIns):

        dataLabelIns.save()

        return resultPackerUtils.save_success()

    def getDetectModelsPages(self, pageItem, dmName):

        selfQuery = {}
        if dmName != None:
            selfQuery['dmName'] = {'$regex': dmName}


        totalCount = detectModelBean.objects(__raw__=selfQuery, state=ConstantUtils.DATA_STATUS_ACTIVE,
                                            userId=session['userId']).count()

        modelList = detectModelBean.objects(__raw__=selfQuery, state=ConstantUtils.DATA_STATUS_ACTIVE,
                                            userId=session['userId']) \
            .order_by('-create_date').exclude("create_date","state").skip(pageItem.skipIndex).limit(pageItem.pageSize)

        modelJsonList=json.loads(modelList.to_json().replace("_id","dmId"))


        # 查询模型的最新版本
        modelVersonIdList = []
        for item in modelList:
            if item['latestVersionId'] is not None:
                modelVersonIdList.append(item['latestVersionId'])


        if len(modelVersonIdList)>0:
            trainVersionList = detectModelTrainVersion.objects(dmtvid__in=modelVersonIdList,
                                                           state=ConstantUtils.DATA_STATUS_ACTIVE).exclude("create_date","state")

            modelVersionJsonList=json.loads(trainVersionList.to_json().replace("_id","dmtvid"))

            #找出所有的数据集id
            allDataSetId=[]
            for versionItem in modelVersionJsonList:
                for item in versionItem['ds_dl_list']:
                    if not allDataSetId.__contains__(item['dsId']):
                        allDataSetId.append(item['dsId'])

            datasetIdNames=datasetsBean.objects(dsId__in=allDataSetId,state=ConstantUtils.DATA_STATUS_ACTIVE).only("dsId","dsName")
            datasetMap={}
            for item in datasetIdNames:
                datasetMap[item['dsId']]=item['dsName']


            for modelItem in modelJsonList:
                if modelItem.keys().__contains__('cvTaskType'):
                    modelItem['cvTaskTypeName']=ConstantUtils.getCVTaskTypaName(modelItem['cvTaskType'])
                for versionItem in modelVersionJsonList:
                    if modelItem.keys().__contains__("latestVersionId"):
                        if modelItem['latestVersionId'] == versionItem['dmtvid']:
                            versionItem['trainState']=ConstantUtils.getModelVersionTrainState(versionItem['trainState'])
                            versionItem['inferencePlatformValue']=ConstantUtils.getModelPlatform(versionItem['inferencePlatform'])
                            versionItem['dmPrecisionValue']=ConstantUtils.getModelPrisision(versionItem['dmPrecision'])
                            datasetNames=[]
                            for item in versionItem['ds_dl_list']:
                                if datasetMap.keys().__contains__("item['dsId']"):
                                    datasetNames.append(datasetMap[item['dsId']])
                            versionItem['datasetNames']=datasetNames
                            modelItem["latestVersionItem"] = [versionItem]
                            break

        pageItem.set_totalCount(totalCount)

        pageItem.set_numpy_dataList(modelJsonList)

        return resultPackerUtils.packPageResult(pageItem);

    def updateDetectModel(self, data):

        detecModeltIns = detectModelBean.objects(dmId=data['dmId'])

        print(data['updateClolumn'])
        detecModeltIns.update(**data['updateClolumn'])

        return resultPackerUtils.update_success()

    def getDetectModelDetail(self, dmId):
        detectModel = detectModelBean.objects(dmId=dmId, state=1).exclude("state", "userId").first()
        detectModel.cvTaskTypeName=ConstantUtils.getCVTaskTypaName(detectModel['cvTaskType'])
        return resultPackerUtils.packDataListResults(detectModel.to_json())

    def delDetectModelDetail(self, dmId):
        detectModelItem = detectModelBean.objects(dmId=dmId)
        detectModelItem.update(state=ConstantUtils.DATA_STATUS_DELETED)
        return resultPackerUtils.update_success()


    def getAllDetectModels(self):
        detectModels=detectModelBean.objects(state=ConstantUtils.DATA_STATUS_ACTIVE,
                                userId=session['userId']).only("dmId","dmName")

        return resultPackerUtils.packDataListResults(detectModels.to_json(),"dmId")

