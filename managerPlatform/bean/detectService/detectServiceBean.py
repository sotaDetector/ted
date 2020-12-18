from managerPlatform.bean.detectModel import detectModelVersion
from managerPlatform.bean.detectModel.detectModelBean import detectModelBean
from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class detectServiceBean(baseBean):

    #服务ID
    dtsid = mongoSource.mdb.SequenceField(primary_key=True)

    #服务名称
    dtsName = mongoSource.mdb.StringField(required=True)

    #模型ID
    dmId=mongoSource.mdb.LongField(required=True)
    dmBean=mongoSource.mdb.ReferenceField(detectModelBean)
    #模型版本ID
    dmtvId = mongoSource.mdb.LongField(required=True)

    dmtvBean=mongoSource.mdb.ReferenceField(detectModelTrainVersion)

    #服务开关
    dtsSwitch=mongoSource.mdb.IntField(required=True)

    #服务密钥
    dtsServiceKey=mongoSource.mdb.StringField(required=True)
    dtsSecret=mongoSource.mdb.StringField(required=True)

    @staticmethod
    def convertToBean(jsonData, session):
        return detectServiceBean(
            dtsName=jsonData['dtsName'],
            dmId=jsonData['dmId'],
            dmBean=jsonData['dmBean'],
            dmtvId=jsonData["dmtvId"],
            dtsSwitch=jsonData["dtsSwitch"],
            dtsServiceKey=jsonData["dtsServiceKey"],
            dtsSecret=jsonData["dtsSecret"],
            userId=session.get("userId"),
            dmtvBean=jsonData['dmtvBean']
        )