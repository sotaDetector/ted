from datetime import datetime

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.common.baseBean.baseBean import baseBean


class detectModelTrainVersion(baseBean):

    dmtvid=mongoSource.mdb.SequenceField(primary_key=True)
    # 模型id
    dmid = mongoSource.mdb.LongField(required=True)
    #版本名称
    dmtvName=mongoSource.mdb.StringField(required=True)
    # 模型大小 precision for detectModel 4xlarge 3large 2middle 1small
    dmPrecision = mongoSource.mdb.IntField(required=True)

    # 推断平台
    inferencePlatform = mongoSource.mdb.IntField(required=True)

    # 数据增强策略
    dataEnhanceType = mongoSource.mdb.IntField(required=True)

    # train trainDataset and label
    ds_dl_list = mongoSource.mdb.ListField()

    #check point model saved path
    ckptModelSavePath=mongoSource.mdb.StringField()

    #完整模型的保存路径
    entireModelSavePath=mongoSource.mdb.StringField()

    #训练状态
    trainState=mongoSource.mdb.IntField(required=True,default=ConstantUtils.model_version_train_state_training)

    trainStartDateTime=mongoSource.mdb.DateTimeField(default=datetime.now)
    trainEndDateTime = mongoSource.mdb.DateTimeField()

    metrics_mAP_5=mongoSource.mdb.FloatField()
    # 精准率
    metrics_precision = mongoSource.mdb.FloatField()
    # 召回率
    metrics_recall = mongoSource.mdb.FloatField()

    dl_id_index_map=mongoSource.mdb.DictField()

    @staticmethod
    def convertToBean(jsonData):
        return detectModelTrainVersion(
            dmid=jsonData['dmid'],
            dmtvName=jsonData['dmtvName'],
            dmPrecision=jsonData['dmPrecision'],
            inferencePlatform=jsonData['inferencePlatform'],
            dataEnhanceType=jsonData['dataEnhanceType'],
            ds_dl_list=jsonData['ds_dl_list']
        )



