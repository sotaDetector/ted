import time

from cv2 import cv2

from managerPlatform.bean.serviceCallerBeans.detectRecord import detectRecord
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.detectModelValidation.detValServiceImpl import detectThreadMap

videoPlayPrefix=configUtils.getConfigProperties("video", "videoPlayPrefix")


class videoDetectService:

    def getVideoDetectResult(self, serviceSessionId, threshold, detectVideo):

        FileNewName = fileUtils.getRandomName(detectVideo.filename)
        savedPath = ConstantUtils.videoDetectSource + FileNewName
        print("视频保存路径：" + savedPath)
        # 保存图片
        detectVideo.save(savedPath)

        # 获取当前的模型
        if detectThreadMap.keys().__contains__(serviceSessionId):
            print("找到相关检测模型...")
            detectThread = detectThreadMap[serviceSessionId]
            detectConfig = detectConfigUtils.getBasicDetectConfig(source=savedPath,
                                                                  outPath=ConstantUtils.videoDetectOut)
            detectThread.detect(detectConfig)

            detectRecordItem=detectRecord(videoSavedPath=ConstantUtils.videoDetectOut+FileNewName)
            detectRecordItem.save()

            result = {
                "videoPlayUrl":videoPlayPrefix+str(detectRecordItem.dereid)
            }

            return resultPackerUtils.packCusResult(result)
        else:

            return resultPackerUtils.packErrorMsg(resultPackerUtils.EC_NO_EVALUATE_SESSION)



    def gen_frames(self, videoPlayId):

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
