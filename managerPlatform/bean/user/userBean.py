from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class userBean(baseBean):
    uid = mongoSource.mdb.SequenceField(primary_key=True)
    userName = mongoSource.mdb.StringField(required=True)
    userLoginAccount = mongoSource.mdb.StringField(required=True)
    userLoginPass = mongoSource.mdb.StringField(required=True)

    @staticmethod
    def convertToBean(jsonData):
        return userBean(
            userName=jsonData['userName'],
            userLoginAccount=jsonData['userLoginAccount'],
            userLoginPass=jsonData['userLoginPass']
        )






