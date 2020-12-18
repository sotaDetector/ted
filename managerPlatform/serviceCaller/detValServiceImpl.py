from detectServiceThread import detectServiceThread
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.modelsManager.detectModelTrainService import detectModelTrainService

detectThreadMap={}

modelVersionSeervice=detectModelTrainService()

class detValServiceImpl:

    #加载模型
    def launchDetectService(self,data):

        #根据版本ID获取模型地址

        dmVersionBean=modelVersionSeervice.getDMVersionBean(data['dmtvid'])[0]

        #从
        modelConfig = {}
        modelConfig["weights"] =dmVersionBean['ckptModelSavePath']
        modelConfig["device"] = ''

        detectS = detectServiceThread(modelConfig)

        serviceSessionId=randomUtils.getRandomStr()
        detectThreadMap[serviceSessionId]=detectS

        result={
            "serviceSessionId":serviceSessionId
        }
        print("the size of detectThreadMap:"+str(detectThreadMap.keys().__len__()))
        return resultPackerUtils.packCusResult(result)




