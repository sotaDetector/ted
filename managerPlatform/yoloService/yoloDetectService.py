from detectServiceThread import detectServiceThread
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.common.keyGen.keyGenarator import keyGenarator
from managerPlatform.detectModelManager.detectModelTrainService import detectModelTrainService
from managerPlatform.common.dataManager.redisSource import redisClient


modelVersionService=detectModelTrainService()
yoloDetectThreadMap = {}
sessionDmtvMap={}

class yoloDetectService:

    # 加载yolo模型
    def launchYoloDetectService(self,sessionId=None,dmtvid=None):
        #如果模型版本为空 直接返回
        if dmtvid is None:
            return None
        #判断是不是重复加载
        if sessionDmtvMap.keys().__contains__(sessionId):
            if sessionDmtvMap[sessionId]==dmtvid:
                return
        # 根据版本ID获取模型地址
        dmVersionBean = modelVersionService.getDMVersionBean(dmtvid)[0]

        modelConfig = {}
        modelConfig["weights"] = dmVersionBean['ckptModelSavePath']
        modelConfig["device"] = ''

        detectSerIns = detectServiceThread(modelConfig)

        if sessionId is None:
            sessionId = randomUtils.getRandomStr()

        yoloDetectThreadMap[sessionId] = detectSerIns
        sessionDmtvMap[sessionId]=dmtvid

        loggerUtils.info("模型启动完毕...." + sessionId)
        loggerUtils.info("sessions of detectThreadMap:" + str(yoloDetectThreadMap.keys()))

        resultMap={
            ConstantUtils.serviceSessionId: sessionId
        }

        return resultMap

    # 释放yolo模型
    def releaseYoloDetectService(self, serviceSessionId):
        if yoloDetectThreadMap.keys().__contains__(serviceSessionId):
            yoloDetectThreadMap.pop(serviceSessionId)
            sessionDmtvMap.pop(serviceSessionId)

            loggerUtils.info("release model:" + str(serviceSessionId))
            loggerUtils.info("sessions of detectThreadMap:" + str(yoloDetectThreadMap.keys()))
        else:
            loggerUtils.info("sessions not in detectThreadMap:" + str(serviceSessionId))

    def createYoloDetectThread(self,config):

        # 为每个检测线程分配sessionId
        sessionId = randomUtils.getRandomStr()
        # 加载模型
        dmVersionBean = modelVersionService.getDMVersionBean(config['dmtvid'])[0]
        modelConfig = {}
        modelConfig["weights"] = dmVersionBean['ckptModelSavePath']
        modelConfig["device"] = ''
        # 创建检测对象
        detectThread = detectServiceThread(modelConfig)

        # 加载检测参数
        detectConfig = detectConfigUtils.getBasicDetectConfig(str(config['source']),
                                                              outPath=ConstantUtils.videoDetectOut + sessionId)

        detectThread.setDetectConfig(detectConfig)

        # 开始线程
        detectThread.start()

        yoloDetectThreadMap[sessionId] = detectThread

        #把sessionId放入到redis中供监控线程监控
        redisClient.hset(keyGenarator.getDetectWatchKey(),sessionId,str(dateUtils.getTimeStamp()))

        result = {
            ConstantUtils.serviceSessionId:sessionId,
            ConstantUtils.videoPlayUrl:ConstantUtils.streamPlayPrefix+sessionId
        }

        return result


    def getDetectServiceInstance(self,serviceSessionId):

        if yoloDetectThreadMap.keys().__contains__(serviceSessionId):
            return yoloDetectThreadMap[serviceSessionId]

        else:
            return None


    #释放检测线程
    def releaseYoloDetectThread(self,sessionId):

        loggerUtils.info("stop session :" + str(sessionId))

        yoloDetectThreadMap[sessionId].stopDetect()

        yoloDetectThreadMap[sessionId].join()








