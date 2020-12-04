from detectCustom import startDetectThread, q, trheadCAapMap, capTrueState
from managerPlatform.common.commonUtils.ffmpegUtils import ffmpegUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class nativeCameraService:

    def getCameraDeviceList(self):
        return resultPackerUtils.packJsonListResults(ffmpegUtils.getCameraList())


    def startNativeCameraDetect(self,configData):

        configData["weights"]="weights/yolov5s.pt"
        #开启检测线程
        sessionId=startDetectThread(configData)

        result={
            "sessionId":sessionId
        }

        return result

    def stopNativeCameraDetect(self,jsonData):
        sessionId=jsonData['sessionId']
        trheadCAapMap[sessionId].release()
        capTrueState[sessionId]=False
        return {"rs":1}




    def gen_frames(self):
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + q.get() + b'\r\n')




