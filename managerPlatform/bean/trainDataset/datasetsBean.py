from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.common.baseBean.baseBean import baseBean


class datasetsBean(baseBean):

    dsId=mongoSource.mdb.SequenceField(primary_key=True)
    dsName=mongoSource.mdb.StringField()
    dsType=mongoSource.mdb.IntField()
    #数据集中图片总数量
    dsImageCount=mongoSource.mdb.IntField(required=True,default=0)
    #标注进度
    dsImgTagSP=mongoSource.mdb.FloatField(required=True,default=0.0)

    dataLabelsList=mongoSource.mdb.ListField()

    @staticmethod
    def convertToBean(jsonData,session):
        return datasetsBean(
            dsName=jsonData['dsName'],
            dsType=jsonData['dsType'],
            userId=session.get("userId")
        )


