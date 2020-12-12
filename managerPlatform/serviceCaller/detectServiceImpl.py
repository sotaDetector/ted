from detectServiceThread import detectServiceThread
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils

detectThreadMap={}

class detectServiceImpl:

    #加载模型
    def launchDetectService(self,data):


        #从
        modelConfig = {}
        modelConfig["weights"] = "weights/yolov5s.pt"
        modelConfig["device"] = ''

        detectS = detectServiceThread(modelConfig)

        serviceSessionId=randomUtils.getRandomStr()
        detectThreadMap[serviceSessionId]=detectS

        result={
            "serviceSessionId":serviceSessionId
        }
        print("the size of detectThreadMap:"+str(detectThreadMap.keys().__len__()))
        return resultPackerUtils.packCusResult(result)




