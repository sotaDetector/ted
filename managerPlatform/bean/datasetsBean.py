from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.bean.baseBean import baseBean


class datasetsBean(baseBean):

    dsId=mongoSource.mdb.SequenceField(primary_key=True)
    dsName=mongoSource.mdb.StringField()
    dsType=mongoSource.mdb.IntField()

    @staticmethod
    def convertToBean(jsonData):
        return datasetsBean(
            dsName=jsonData['dsName'],
            dsType=jsonData['dsType']
        )


