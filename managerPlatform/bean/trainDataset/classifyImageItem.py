from managerPlatform.common.baseBean.imageBaseBean import imageBaseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class classifyImageItem(imageBaseBean):

    clsimgid = mongoSource.mdb.SequenceField(primary_key=True)

    # 标签ID
    classifyLabel = mongoSource.mdb.IntField(required=True)


