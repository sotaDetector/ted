from detectServiceThread import detectServiceThread
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.ffmpegUtils import ffmpegUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.common.dataManager.redisSource import redisClient
from managerPlatform.common.keyGen.keyGenarator import keyGenarator
from managerPlatform.detectModelValidation.detValServiceImpl import modelVersionSeervice

detectMap = {}


class cameraStreamService:

    def getCameraDeviceList(self):
        return resultPackerUtils.packJsonListResults(ffmpegUtils.getCameraList())

    def startNativeCameraDetect(self,config):



        return self.startStreamDetect(config)


    def startLiveStreamDetect(self,config):


        return self.startStreamDetect(config)

    def startStreamDetect(self,config):
        # 为每个检测线程分配sessionId
        sessionId = randomUtils.getRandomStr()
        # 加载模型
        dmVersionBean = modelVersionSeervice.getDMVersionBean(config['dmtvid'])[0]
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

        detectMap[sessionId] = detectThread

        result = {
            "videoPlayId": sessionId
        }

        return result

    def stopNativeCameraDetect(self, jsonData):

        sessionId = jsonData['videoPlayId']

        detectMap[sessionId].stopDetect()

        detectMap[sessionId].join()

        return {"rs": 1}

    def gen_frames(self, sessionId):
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + detectMap[sessionId].getStreamQueue().get() + b'\r\n')

    def sendDetectHeartbeat(self, data):

        for i in data['sessionIds'].split(","):
            if i != "":
                redisClient.hset(keyGenarator.getDetectWatchKey(), i, str(dateUtils.getTimeStamp()))

        return resultPackerUtils.save_success()
