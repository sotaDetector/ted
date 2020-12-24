from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class imageBaseBean(baseBean):
    # 图片原名
    imgFileName = mongoSource.mdb.StringField(required=True)
    # 存储路径
    imgPath = mongoSource.mdb.StringField(required=True)

    # 图片宽
    imgWidth = mongoSource.mdb.IntField(required=True)

    # 图片高
    imgHeight = mongoSource.mdb.IntField(required=True)

    # 数据集ID
    dsId = mongoSource.mdb.LongField(required=True)
    # 是否被标注过
    isLabeled = mongoSource.mdb.IntField(required=True, default=0)

    meta = {
        'abstract': True,
    }
