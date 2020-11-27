class ConstantUtils:

    DATA_STATUS_ACTIVE=1

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


    @classmethod
    def getModelWeightsPath(cls,weightType):
       return "weights/"+cls.WEIGHT_MAP[weightType]

