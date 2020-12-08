class ConstantUtils:

    DATA_STATUS_ACTIVE=1


    TRUE_TAG="true"
    FALSE_TAG="false"

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



