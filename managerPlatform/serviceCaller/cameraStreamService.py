from detectCustom import detectCustom
from managerPlatform.common.commonUtils.dateUtils import dateUtils
from managerPlatform.common.commonUtils.ffmpegUtils import ffmpegUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.dataManager.redisSource import redisClient
from managerPlatform.common.keyGen.keyGenarator import keyGenarator

detectMap = {}


class cameraStreamService:

    def getCameraDeviceList(self):
        return resultPackerUtils.packJsonListResults(ffmpegUtils.getCameraList())

    def startNativeCameraDetect(self,config):


        # 创建检测对象
        detectThread = detectCustom()

        #加载模型
        modelConfig = {}
        modelConfig["weights"] = "weights/yolov5s.pt"
        modelConfig["device"]=''
        detectThread.loadModel(modelConfig)

        #加载检测参数
        detectConfig={
            "source":config['source']
        }
        detectThread.setDetectConfig(detectConfig)

        #开始线程
        detectThread.start()

        # 为每个检测线程分配sessionId
        sessionId = randomUtils.getRandomStr()

        detectMap[sessionId] = detectThread

        result = {
            "sessionId": sessionId
        }

        return result

    def stopNativeCameraDetect(self, jsonData):

        sessionId = jsonData['sessionId']

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
