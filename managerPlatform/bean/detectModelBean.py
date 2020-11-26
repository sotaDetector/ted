from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.common.baseBean.baseBean import baseBean


class detectModelBean(baseBean):

    dmId = mongoSource.mdb.SequenceField(primary_key=True)
    #model name
    dmName = mongoSource.mdb.StringField()
    #mmodel type
    dmType=mongoSource.mdb.IntField(required=True)
    #model remark
    dmRemark=mongoSource.mdb.StringField()

    @staticmethod
    def convertToBean(jsonData):
        return detectModelBean(
            dmName=jsonData['dmName'],
            dmType=jsonData['dmType'],
            dmRemark=jsonData['dmRemark']
        )

