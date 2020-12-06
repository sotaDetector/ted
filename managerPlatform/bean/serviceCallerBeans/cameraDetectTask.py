from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class cameraDetectSetting(baseBean):

    cdsid = mongoSource.mdb.SequenceField(primary_key=True)

    #名称
    cdsName=mongoSource.mdb.StringField(required=True)

    #源类型  1本地摄像头 2直播视频流
    cdsSourceType=mongoSource.mdb.IntField(required=True)

    #源地址
    cdsSourceAddr=mongoSource.mdb.StringField(required=True)


    #检测模型
    #模型ID
    dmId=mongoSource.mdb.LongField(required=True)
    #模型版本ID
    dmtvid=mongoSource.mdb.LongField(required=True)

    #是否启用无人值守
    isUnattended=mongoSource.mdb.IntField(required=True)











