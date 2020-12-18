from flask import session
from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.common.baseBean.baseBean import baseBean


class detectModelBean(baseBean):

    dmId = mongoSource.mdb.SequenceField(primary_key=True)
    #detectModel name
    dmName = mongoSource.mdb.StringField()
    #mmodel type
    dmType=mongoSource.mdb.IntField(required=True)
    #detectModel remark
    dmRemark=mongoSource.mdb.StringField()

    #最新版本ID
    latestVersionId=mongoSource.mdb.LongField()

    latestVersionItem=mongoSource.mdb.ReferenceField(detectModelTrainVersion)


    @staticmethod
    def convertToBean(jsonData):
        return detectModelBean(
            dmName=jsonData['dmName'],
            dmType=jsonData['dmType'],
            dmRemark=jsonData['dmRemark'],
            userId=session.get("userId")
        )

