import threading

from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.datasetsManager.datasetsService import datasetsService

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
            "weights": "/Volumes/study/objectDetection/ODS/objectDetection/yolov5/weights/yolov5s.pt",
            "data":"/Volumes/study/objectDetection/ODS/objectDetection/yolov5/data/coco128.yaml"
        }
        # t1 = threading.Thread(target=custom_train, args=(datasetDict,configMap))
        # t1.setDaemon(True)
        # t1.start()

        # custom_train(datasetDict,configMap)

        return resultPackerUtils.save_success()
