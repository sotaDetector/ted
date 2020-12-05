from detectCustom import detectCustom
from managerPlatform.common.commonUtils.ffmpegUtils import ffmpegUtils
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils

detectMap={}

class nativeCameraService:



    def getCameraDeviceList(self):
        return resultPackerUtils.packJsonListResults(ffmpegUtils.getCameraList())


    def startNativeCameraDetect(self,configData):

        configData["weights"]="weights/yolov5s.pt"
        #开启检测线程
        detectThread=detectCustom(configData)

        detectThread.start()

        #为每个检测线程分配sessionId
        sessionId=randomUtils.getRandomStr()

        detectMap[sessionId]=detectThread

        result={
            "sessionId":sessionId
        }

        return result

    def stopNativeCameraDetect(self,jsonData):

        sessionId=jsonData['sessionId']

        detectMap[sessionId].stopDetect()

        return {"rs":1}





    def gen_frames(self,sessionId):
        print("----------ew---------")
        print(sessionId)
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + detectMap[sessionId].getStreamQueue().get() + b'\r\n')




