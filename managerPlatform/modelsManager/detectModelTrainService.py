import threading

from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.datasetsManager.datasetsService import datasetsService
from trainCustom import trainYolo

datasetService = datasetsService()



class detectModelTrainService:


    def detectModelVersionTrain(self, modelTrainVersion):
        # 1.保存训练版本bean
        # modelTrainVersion.save()

        # 2.训练
        # 2.1. 准备数据
        datasetDict = datasetService.loadTrainData(modelTrainVersion['ds_dl_list'])
        # 2.2 开启训练线程
        configMap = {
            "weights": "/Volumes/study/objectDetection/ted/weights/yolov5s.pt",
            "data":"/Volumes/study/objectDetection/ted/data/coco128.yaml"
        }
        t1 = threading.Thread(target=trainYolo, args=(datasetDict,configMap))
        t1.setDaemon(True)
        t1.start()

        return resultPackerUtils.save_success()
