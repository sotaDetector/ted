from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class detectModelTrainConfig(baseBean):

    dmtvid = mongoSource.mdb.SequenceField(primary_key=True)
    #训练版本ID
    dmtvid = mongoSource.mdb.LongField(required=True)
    #模型权重路径
    weights=mongoSource.mdb.StringField(required=True)
    #模型结构文件 --cfg yolov5s.yaml
    cfg=mongoSource.mdb.StringField(required=True,default='')
    #超参数文件
    hyp=mongoSource.mdb.StringField(required=True,default="data/hyp.scratch.yaml")
    #训练轮次
    epochs=mongoSource.mdb.IntField(required=True,default=300)
    #batch size 批大小
    batch_size=mongoSource.mdb.IntField(required=True,default=16)
    #图片大小
    img_size=mongoSource.mdb.ListField(required=True,default=[640, 640])
    #rectangular training  https://blog.csdn.net/zicai_jiayou/article/details/109623578
    rect=mongoSource.mdb.BooleanField(default=False)
    #是否继续最后一次训练 resume most recent training
    resume=mongoSource.mdb.BooleanField(default=False)
    #only save final checkpoint
    nosave=mongoSource.mdb.BooleanField(default=False)
    #only test final epoch
    notest=mongoSource.mdb.BooleanField(default=False)
    #disable autoanchor check
    noautoanchor=mongoSource.mdb.BooleanField(default=False)
    #evolve hyperparameters 是否调整超参数
    evolve=mongoSource.mdb.BooleanField(default=False)
    #gsutil bucket
    bucket=mongoSource.mdb.StringField(default='')
    #cache images for faster training
    cache_images=mongoSource.mdb.BooleanField(default=False)
    #use weighted image selection for training
    image_weights=mongoSource.mdb.BooleanField(default=False)
    #设备类型 cuda device, i.e. 0 or 0,1,2,3 or cpu
    device=mongoSource.mdb.StringField(default='')
    #vary img-size +/- 50%%
    multi_scale=mongoSource.mdb.BooleanField(default=False)
    #train as single-class trainDataset
    single_cls=mongoSource.mdb.BooleanField(default=False)
    #use torch.optim.Adam() optimizer
    adam=mongoSource.mdb.BooleanField(default=False)
    #use SyncBatchNorm, only available in DDP mode
    sync_bn=mongoSource.mdb.BooleanField(default=False)
    #DDP parameter, do not modify
    local_rank=mongoSource.mdb.IntField(default=-1)
    #number of images for W&B logging, max 100
    log_imgs=mongoSource.mdb.IntField(default=16)
    #maximum number of dataloader workers
    workers=mongoSource.mdb.IntField(default=0)
    #工程名称 每个模型需指定一个唯一名称 default='runs/train' save to project/name
    project=mongoSource.mdb.StringField(required=True)
    #文件夹名称 default='exp', help='save to project/name'
    name=mongoSource.mdb.StringField(required=True)
    #是否覆盖文件 existing project/name ok, do not increment
    exist_ok=mongoSource.mdb.BooleanField(default=False)

    @classmethod
    def getDetectModelTrainConfig(cls,dmtvid,cfg,weights,epochs,batch_size,project,name):

        return detectModelTrainConfig(
            dmtvid=dmtvid,
            cfg=cfg,
            weights=weights,
            epochs=epochs,
            batch_size=batch_size,
            project=project,
            name=name
        )







