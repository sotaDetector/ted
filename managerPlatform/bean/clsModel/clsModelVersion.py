from managerPlatform.common.baseBean.modelVersionBaseBean import modelVersionBaseBean
from managerPlatform.common.dataManager.mongoSource import mongoSource


class clsModelVersion(modelVersionBaseBean):

    cmvid=mongoSource.mdb.SequenceField(primary_key=True)

    @staticmethod
    def convertToBean(jsonData):
        return clsModelVersion(
            dmid=jsonData['dmid'],
            dmtvName=jsonData['dmtvName'],
            dmPrecision=jsonData['dmPrecision'],
            inferencePlatform=jsonData['inferencePlatform'],
            dataEnhanceType=jsonData['dataEnhanceType'],
            ds_dl_list=jsonData['ds_dl_list']
        )













