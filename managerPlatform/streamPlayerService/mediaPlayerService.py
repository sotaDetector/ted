import time

import cv2

from managerPlatform.bean.serviceCallerBeans.detectRecord import detectRecord
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.yoloService.yoloDetectService import yoloDetectThreadMap


class mediaPlayerService:

    def genFramesFromLiveStream(self, sessionId):
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + yoloDetectThreadMap[sessionId].getStreamQueue().get() + b'\r\n')



    def genFramesFromVideo(self, videoPlayId):

        recordItem=detectRecord.objects(dereid=videoPlayId,state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        cap = cv2.VideoCapture(recordItem['videoSavedPath'])
        fps=cap.get(cv2.CAP_PROP_FPS)
        print("fps:"+str(fps))
        while cap.isOpened():
            time.sleep(1/(fps+24))
            ret, frame = cap.read()
            if frame is None:
                break
            ret, imageData = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + imageData.tobytes() + b'\r\n')

        cap.release()