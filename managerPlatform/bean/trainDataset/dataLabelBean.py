
from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class dataLabelBean(baseBean):

    dlid=mongoSource.mdb.SequenceField(primary_key=True)

    dlIndex=mongoSource.mdb.IntField()
    #标签名称
    dlName=mongoSource.mdb.StringField(required=True)
    #数据集id
    dsId=mongoSource.mdb.LongField(required=True)


    @staticmethod
    def convertToBean(jsonData):
        return dataLabelBean(
            dlName=jsonData['dlName'],
            dsId=jsonData['dsId']
        )