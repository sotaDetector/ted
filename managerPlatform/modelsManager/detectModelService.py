from managerPlatform.bean.detectModelBean import detectModelBean
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class detectModelService:

    def addDetectModel(self,dataLabelIns):

        dataLabelIns.save()

        return resultPackerUtils.save_success()


    def getDetectModelsPages(self,pageItem,dmName):

        totalCount=detectModelBean.objects().count()

        dataList=detectModelBean.objects(__raw__={'dmName':{'$regex':dmName}}).order_by('-create_date').skip(pageItem.skipIndex).limit(pageItem.pageSize)

        pageItem.set_totalCount(totalCount)

        pageItem.set_dataList(dataList)

        return resultPackerUtils.packPageResult(pageItem);


    def updateDetectModel(self,data):

        detecModeltIns=detectModelBean.objects(dmId=data['dmId'])

        print(data['updateClolumn'])
        detecModeltIns.update(**data['updateClolumn'])

        return resultPackerUtils.update_success()
