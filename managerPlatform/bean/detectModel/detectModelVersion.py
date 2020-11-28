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



