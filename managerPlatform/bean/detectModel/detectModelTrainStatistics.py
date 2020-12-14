from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class detectModelTrainStatistics(baseBean):

    dmts = mongoSource.mdb.SequenceField(primary_key=True)

    #训练版本ID
    dmtvid=mongoSource.mdb.LongField(required=True)

    #轮次ID
    epoch=mongoSource.mdb.IntField(required=True)

    #mAP_0.5
    metrics_mAP_5=mongoSource.mdb.FloatField(required=True)

    # mAP_0.5:0.9
    metrics_mAP = mongoSource.mdb.FloatField(required=True)

    #精准率
    metrics_precision=mongoSource.mdb.FloatField(required=True)
    #召回率
    metrics_recall=mongoSource.mdb.FloatField(required=True)

    #模型训练相关统计
    train_box_loss=mongoSource.mdb.FloatField(required=True)

    train_cls_loss=mongoSource.mdb.FloatField(required=True)

    train_obj_loss=mongoSource.mdb.FloatField(required=True)

    # 模型校验相关统计
    val_box_loss = mongoSource.mdb.FloatField(required=True)

    val_cls_loss = mongoSource.mdb.FloatField(required=True)

    val_obj_loss = mongoSource.mdb.FloatField(required=True)

    #学习相关
    x_lr0=mongoSource.mdb.FloatField(required=True)
    x_lr1 = mongoSource.mdb.FloatField(required=True)
    x_lr2 = mongoSource.mdb.FloatField(required=True)