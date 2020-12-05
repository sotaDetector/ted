from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class detectSetting(baseBean):

    sessionId=mongoSource.mdb.StringField(required=True)





