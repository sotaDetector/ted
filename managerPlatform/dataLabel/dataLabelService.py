
from managerPlatform.bean.trainDataset.dataLabelBean import dataLabelBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class dataLabelService:

    def addDataLabel(self, dataLabelIns):

        dataLabelIns.save()

        return resultPackerUtils.save_success()

    def updateDataLabel(self,data):

        dataLabelIns = dataLabelBean.objects(dlid=data['dlid'])
        dataLabelIns.update(**data['updateClolumn'])

        return resultPackerUtils.update_success()

    def getAllDataLabelByDsid(self,queryData):
        data =dataLabelBean.objects(dsId=queryData['dsId'],state=ConstantUtils.DATA_STATUS_ACTIVE)
        return resultPackerUtils.packDataListResults(data.to_json())

    def delDataLabel(self,dlid):

        dataLabel=dataLabelBean.objects(dlid=dlid).first()

        dataLabel.update(state=0)

        return resultPackerUtils.update_success()

    def getLabelsBylids(self,dsId):
        # lids=[]
        # for item in idsMap:
        #     lids.append(item)
        # labelList=dataLabelBean.objects(dlid__in=lids)
        # labelMap={}
        # for item in labelList:
        #     labelMap[item['dlid']]=item['dlName']
        # return labelMap
        nameList=[]
        labelList = dataLabelBean.objects(dsId=dsId)
        labelMap = {}
        for item in labelList:
            labelMap[item['dlIndex']] = item['dlName']
            nameList.append(item['dlName'])
        return labelMap,nameList


