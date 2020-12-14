from detectServiceThread import detectServiceThread
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.ffmpegUtils import ffmpegUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.common.dataManager.redisSource import redisClient
from managerPlatform.common.keyGen.keyGenarator import keyGenarator
from managerPlatform.serviceCaller.detectServiceImpl import detectThreadMap

detectMap = {}


class cameraStreamService:

    def getCameraDeviceList(self):
        return resultPackerUtils.packJsonListResults(ffmpegUtils.getCameraList())

    def startNativeCameraDetect(self,config):

        #加载模型
        # modelConfig = {}
        # modelConfig["weights"] = "weights/yolov5s.pt"
        # modelConfig["device"]=''
        # # 创建检测对象
        # detectThread = detectServiceThread(modelConfig)
        if not detectThreadMap.keys().__contains__(config['serviceSessionId']):
            return resultPackerUtils.packErrorMsg(resultPackerUtils.EC_NO_EVALUATE_SESSION)
        detectThread = detectThreadMap[config['serviceSessionId']]

        #加载检测参数
        detectConfig=detectConfigUtils.getBasicDetectConfig(str(config['source']),outPath=ConstantUtils.videoDetectOut+config['serviceSessionId'])

        detectThread.setDetectConfig(detectConfig)

        #开始线程
        detectThread.start()

        # 为每个检测线程分配sessionId
        sessionId = randomUtils.getRandomStr()

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
