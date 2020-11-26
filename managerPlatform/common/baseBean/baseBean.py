from datetime import datetime

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.dataManager.mongoSource import mongoSource


class baseBean(mongoSource.mdb.Document):
    create_date = mongoSource.mdb.DateTimeField(default=datetime.now)
    update_date = mongoSource.mdb.DateTimeField(default=datetime.now)
    state=mongoSource.mdb.IntField(default=ConstantUtils.DATA_STATUS_ACTIVE)

    # meta = {'allow_inheritance': True}
    meta = {
        'abstract': True,
    }



