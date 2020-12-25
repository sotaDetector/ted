from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.config.configUtils import configUtils


class ConstantUtils:

    DATA_STATUS_ACTIVE=1
    DATA_STATUS_DELETED = 0


    TRUE_TAG=True
    FALSE_TAG=False



    dataBasePath = configUtils.getConfigProperties("file", "compreImgPackPath")

    singleImgDetectSource = dataBasePath + "SingleImgDetectSource/"
    fileUtils.detectPath(singleImgDetectSource)
    singleImgDetectOut = dataBasePath + "singleImgDetectOut/"
    fileUtils.detectPath(singleImgDetectOut)

    videoDetectSource=dataBasePath+"videoDetectSource/"
    fileUtils.detectPath(videoDetectSource)
    videoDetectOut=dataBasePath+"videoDetectOut/"
    fileUtils.detectPath(videoDetectOut)

    modelBasePath = configUtils.getConfigProperties("model", "modelSavePath")
    fileUtils.detectPath(videoDetectOut)

    imageItemPrefix = configUtils.getConfigProperties("file", "imageItemPrefix")+"dsc/imageItem/"

    videoPlayPrefix = configUtils.getConfigProperties("video", "videoPlayPrefix")
    streamPlayPrefix = configUtils.getConfigProperties("video", "streamPlayPrefix")

    serviceSessionId="serviceSessionId"
    videoPlayUrl="videoPlayUrl"

    UP_FILE_TYPE_COMPRESSFILE="1"
    UP_FILE_TYPE_IMAGEFILE = "2"

    #未训练
    model_version_train_state_untrain=0
    #训练中
    model_version_train_state_training=1
    #训练成功
    model_version_train_state_success = 2
    #训练失败
    model_version_train_state_failed = 3

    modelVersionMap={
        model_version_train_state_untrain:"未训练",
        model_version_train_state_training:"训练中",
        model_version_train_state_success:"训练成功",
        model_version_train_state_failed:"训练失败"
    }

    @classmethod
    def getModelVersionTrainState(cls,id):
        return cls.modelVersionMap[id]

    MODEL_WEIGHT_S = 1
    MODEL_WEIGHT_M = 2
    MODEL_WEIGHT_L = 3
    MODEL_WEIGHT_X = 4

    WEIGHT_MAP={
        MODEL_WEIGHT_S:"yolov5s.pt",
        MODEL_WEIGHT_M:"yolov5m.pt",
        MODEL_WEIGHT_L:"yolov5l.pt",
        MODEL_WEIGHT_X:"yolov5x.pt"
    }

    CFG_MAP={
        MODEL_WEIGHT_S: "yolov5s.yaml",
        MODEL_WEIGHT_M: "yolov5m.yaml",
        MODEL_WEIGHT_L: "yolov5l.yaml",
        MODEL_WEIGHT_X: "yolov5x.yaml"
    }

    MODEL_PRICISION_MAP = {
        MODEL_WEIGHT_S: "小",
        MODEL_WEIGHT_M: "中",
        MODEL_WEIGHT_L: "大",
        MODEL_WEIGHT_X: "超大"

    }

    SERVICE_SWITCH_ON=1
    SERVICE_SWITCH_CLOSE=2



    @classmethod
    def getModelPrisision(cls,pricisionIndex):
        return cls.MODEL_PRICISION_MAP[pricisionIndex]


    MODEL_PLATFORM_SERVER=1
    MODEL_PLATFORM_LITE = 2

    MODEL_PLATFORM_MAP={
        MODEL_PLATFORM_SERVER:"云端",
        MODEL_PLATFORM_LITE:"移动端"
    }


    @classmethod
    def getModelPlatform(cls,platformIndex):
        return cls.MODEL_PLATFORM_MAP[platformIndex]


    @classmethod
    def getModelWeightsPath(cls,isUsePreTraindModel,modelType):
        #如果是不设置预制weights
        if isUsePreTraindModel == cls.FALSE_TAG:
            return ''
        return "weights/"+cls.WEIGHT_MAP[modelType]

    @classmethod
    def getModelCfgPath(cls,isUsePreTraindModel,modelType):
        if isUsePreTraindModel == cls.TRUE_TAG:
            return None
        else:
            return "models/"+cls.CFG_MAP[modelType]


    detectSessionMap = {}

    @classmethod
    def updateDetectSessionTime(cls, serviceSessionId):
        loggerUtils.info("update session:"+serviceSessionId+"/"+str(dateUtils.getTimeStamp()))
        cls.detectSessionMap[serviceSessionId] = dateUtils.getTimeStamp()



    CV_TASK_TYPE_CLASSIFY=1
    CV_TASK_TYPE_DETECT = 2

    CV_TASK_TYPE_NAME_MAP={
        CV_TASK_TYPE_CLASSIFY:"图像分类",
        CV_TASK_TYPE_DETECT:"目标检测"
    }


    @classmethod
    def getCVTaskTypaName(cls,cvTaskType):
        if cls.CV_TASK_TYPE_NAME_MAP.keys().__contains__(cvTaskType):
            return cls.CV_TASK_TYPE_NAME_MAP[cvTaskType]



    #图片已标注
    IMAGE_LBALED=1
    #图片为标注
    IMAGE_UNLABEL = 2
