from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class detectModelConfig(baseBean):
    dmtvid = mongoSource.mdb.SequenceField(primary_key=True)
    #模型权重路径
    weights=mongoSource.mdb.StringField(required=True)
    #模型结构文件 --cfg yolov5s.yaml
    cfg=mongoSource.mdb.StringField(required=True)
    #超参数文件
    hyp=mongoSource.mdb.StringField(required=True)
