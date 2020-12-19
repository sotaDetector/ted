from flask import session

from managerPlatform.bean.detectModel.detectModelBean import detectModelBean
from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.bean.detectService.detectServiceBean import detectServiceBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
import json

class detectServiceImpl:

    def addDetectService(self,jsonData):
        dtsServiceKey=randomUtils.getRandomStr()
        serviceSecret=randomUtils.getRandomStr()
        jsonData["dtsServiceKey"]=dtsServiceKey
        jsonData["dtsSecret"]=serviceSecret
        jsonData["dmBean"]=detectModelBean.objects(dmId=jsonData["dmId"],state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        jsonData['dmtvBean']=detectModelTrainVersion.objects(dmtvid=jsonData["dmtvId"],state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        detectService = detectServiceBean.convertToBean(jsonData, session)

        detectService.save()

        #开启服务
        if jsonData['dtsSwitch']==ConstantUtils.SERVICE_SWITCH_ON:
            pass

        return resultPackerUtils.save_success()

    def updateDetectService(self,jsonData):

        detectServiceIns = detectServiceBean.objects(dtsid=jsonData['dtsid'], state=ConstantUtils.DATA_STATUS_ACTIVE)
        updateMap=jsonData['updateClolumn']

        updateMap["dmBean"] = detectModelBean.objects(dmId=jsonData["updateClolumn"]['dmId'], state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        updateMap['dmtvBean'] =detectModelTrainVersion.objects(dmtvid=jsonData["updateClolumn"]["dmtvId"], state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        detectServiceIns.update(**jsonData['updateClolumn'])

        return resultPackerUtils.update_success()



    def getDetectServicePageList(self,pageItem):

        totalCount=detectServiceBean.objects(userId=session.get("userId"),state=ConstantUtils.DATA_STATUS_ACTIVE).count()

        #select_related()

        collection=detectServiceBean._get_collection()

        resultList=collection.aggregate([
                {
                    '$lookup':
                        {
                            "from": "detect_model_bean",
                            "localField": "dmBean",
                            "foreignField": "_id",
                            "as": "model"
                        },
                },{
                    '$lookup':
                        {
                            "from": "detect_model_train_version",
                            "localField": "dmtvBean",
                            "foreignField": "_id",
                            "as": "modelVersion"
                        },
                },
                {
                    '$match':
                    {
                         "userId":session.get("userId"),
                         "state":ConstantUtils.DATA_STATUS_ACTIVE

                    }
                },
                {

                    '$project':
                        {
                            'dtsName':1,
                            'dtsSwitch':1,
                            "dtsSecretKey":1,
                            "create_date":1,
                            'model.dmName':1,
                            'model.dmType':1,
                            'modelVersion.dmtvName':1,
                            'dmId': 1,
                            'dmtvId':1,
                            "dtsServiceKey":1,
                            "dtsSecret":1

                        },
                 },
                 {
                    "$sort":{"create_date":-1}
                 },
                 {
                    "$skip":pageItem.skipIndex
                 },
                 {
                    "$limit":pageItem.pageSize
                 }

            ])


        pageItem.set_totalCount(totalCount)

        print(type(resultList))

        pageItem.set_numpy_dataList(list(resultList))

        return resultPackerUtils.packPageResult(pageItem)

    def delDetectService(self,jsonData):

        detectServiceIns = detectServiceBean.objects(dtsid=jsonData['dtsid'])
        detectServiceIns.update(state=ConstantUtils.DATA_STATUS_DELETED)
        return resultPackerUtils.update_success()


    def getDetectServiceDetail(self,jsonData):

        detectService=detectServiceBean.objects(dtsid=jsonData['dtsid'],state=ConstantUtils.DATA_STATUS_ACTIVE).exclude("create_date","state")

        return resultPackerUtils.packDataItemResults(detectService.to_json(),"dtsid")


    def changeDtsSwitch(self,jsonData):

        detectServiceIns = detectServiceBean.objects(dtsid=jsonData['dtsid'])

        #更改数据库状态
        detectServiceIns.update(dtsSwitch=jsonData['dtsSwitch'])

        return resultPackerUtils.update_success()


