from flask import session

from managerPlatform.bean.detectModel.detectModelBean import detectModelBean
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class detectModelService:

    def addDetectModel(self,dataLabelIns):

        dataLabelIns.save()

        return resultPackerUtils.save_success()


    def getDetectModelsPages(self,pageItem,dmName):

        totalCount=detectModelBean.objects().count()

        selfQuery={}
        if dmName!=None:
            selfQuery['dmName']={'$regex':dmName}

        dataList=detectModelBean.objects(__raw__=selfQuery,state=1,userId=session['userId']).order_by('-create_date').skip(pageItem.skipIndex).limit(pageItem.pageSize)

        pageItem.set_totalCount(totalCount)

        pageItem.set_dataList(dataList)

        return resultPackerUtils.packPageResult(pageItem);


    def updateDetectModel(self,data):

        detecModeltIns=detectModelBean.objects(dmId=data['dmId'])

        print(data['updateClolumn'])
        detecModeltIns.update(**data['updateClolumn'])

        return resultPackerUtils.update_success()


    def getDetectModelDetail(self,dmId):
        result=detectModelBean.objects(dmId=dmId, state=1).exclude("state", "userId").to_json()
        return resultPackerUtils.packDataItemResults(result)


