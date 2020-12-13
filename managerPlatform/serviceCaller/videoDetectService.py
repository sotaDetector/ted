import time

from cv2 import cv2

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.detectConfigUtils import detectConfigUtils
from managerPlatform.serviceCaller.detectServiceImpl import detectThreadMap


class videoDetectService:

    def getVideoDetectResult(self, serviceSessionId, threshold, imgData):

        FileNewName = fileUtils.getRandomName(imgData.filename)
        savedPath = ConstantUtils.videoDetectSource + FileNewName
        print("视频保存路径：" + savedPath)
        # 保存图片
        imgData.save(savedPath)

        # 获取当前的模型
        if detectThreadMap.keys().__contains__(serviceSessionId):
            print("找到相关检测模型...")
            detectThread = detectThreadMap[serviceSessionId]
            detectConfig = detectConfigUtils.getBasicDetectConfig(source=savedPath,
                                                                  outPath=ConstantUtils.videoDetectOut)
            detectThread.detect(detectConfig)

            result = {
                "videoPath": ConstantUtils.imageItemPrefix + "videoDetectOut_" + FileNewName
            }

            return resultPackerUtils.packCusResult(result)

    def gen_frames(self, sessionId):

        cap = cv2.VideoCapture('/Volumes/study/objectDetection/ted/resources/809ce493-8b6f-4bf1-834b-f9d51d9657b8.mp4')
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
