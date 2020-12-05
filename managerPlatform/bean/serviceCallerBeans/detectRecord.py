from managerPlatform.common.baseBean.baseBean import baseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class detectRecord(baseBean):
    dereid=mongoSource.mdb.SequenceField(primary_key=True)
