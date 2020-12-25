import json
from datetime import datetime

from managerPlatform.bean.trainDataset.classifyImageItem import classifyImageItem
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.dataLabel.dataLabelService import dataLabelService

labelService = dataLabelService()

class clssifyDatasetsService:

    def upClassifyImageItem(self, data):
        classifyImageData = classifyImageItem.objects(clsimgid=data["clsimgid"],
                                                      state=ConstantUtils.DATA_STATUS_ACTIVE).first()

        classifyImageData.update(classifyLabel=data["classifyLabel"], isLabeled=1,
                                 update_date=datetime.now)

        # 更新标注进度
        self.updateDataSetStatisData(data["dsId"])

        return resultPackerUtils.update_success()

    def updateDataSetStatisData(self, dsId):
        dsItem = datasetsBean.objects(dsId=dsId, state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        # 更新总数量
        totalCount = classifyImageItem.objects(dsId=dsId, state=1).count()

        labledCount = classifyImageItem.objects(dsId=dsId, isLabeled=1, state=1).count()

        dsItem.update(dsImageCount=totalCount, dsImgTagSP=labledCount)

    def getClsImgItemList(self, pageItem, data):
        totalCount = classifyImageItem.objects(__raw__={'dsId': data['dsId']},
                                               state=ConstantUtils.DATA_STATUS_ACTIVE,
                                               isLabeled=data["isLabeled"]).count()

        dataList = classifyImageItem.objects(__raw__={'dsId': data['dsId']}, state=ConstantUtils.DATA_STATUS_ACTIVE,
                                             isLabeled=data["isLabeled"]) \
            .skip(pageItem.skipIndex).limit(pageItem.pageSize)

        pageItem.set_totalCount(totalCount)


        labelMap, nameList = labelService.getLabelsBylids(data['dsId'])
        # 获取该数据集下所有的标签
        jsonArray=json.loads(dataList.to_json())
        for item in jsonArray:
            item["ditFilePath"]=ConstantUtils.imageItemPrefix +item["ditFilePath"].replace("/","_")
            if item.keys().__contains__('classifyLabel'):
                if labelMap !=None and labelMap.keys().__contains__(item['classifyLabel']):
                    item["classifyLabelName"]=labelMap[item['classifyLabel']]


        pageItem.set_numpy_dataList(jsonArray)

        return resultPackerUtils.packPageResult(pageItem)

    def getClsImgDetail(self, queryData):
        classImageItem = classifyImageItem.objects(clsimgid=queryData['clsimgid'],
                                                   state=ConstantUtils.DATA_STATUS_ACTIVE).first()

        labelItem=labelService.getLabelBylid(classImageItem['classifyLabel'])

        classImageItem.classifyLabelName=labelItem['dlName']
        classImageItem.imgPath=ConstantUtils.imageItemPrefix +"_"+classImageItem['ditFilePath'].replace("/","_")

        return resultPackerUtils.packDataListResults(classImageItem.to_json())

    def delClsImgItem(self,queryData):
        classImageItem = classifyImageItem.objects(clsimgid=queryData['clsimgid'],
                                                   state=ConstantUtils.DATA_STATUS_ACTIVE).first()

        classImageItem.update(state=ConstantUtils.DATA_STATUS_DELETED)

        self.updateDataSetStatisData(classImageItem.dsId)

        return resultPackerUtils.update_success()
