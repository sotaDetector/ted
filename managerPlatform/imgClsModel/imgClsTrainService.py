from managerPlatform.bean.clsModel.clsModelVersion import clsModelVersion
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class imgClsTrainService:

    def imgClsModelTrain(self,jsonData):
        clsModel=clsModelVersion.convertToBean(jsonData)
        clsModel.save()

        return resultPackerUtils.save_success()

