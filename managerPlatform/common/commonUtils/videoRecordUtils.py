import time
import cv2

class videoRecordUtils:


    @classmethod
    def createVideoWriter(cls,cap):
        #
        vw = cv2.VideoWriter()

        sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = 30
        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  #cap stream
        # fourcc = cv2.VideoWriter_fourcc('M','J','P','G')  #images
        fourcc = 'mp4v'

        vw.open("out.mp4", cv2.VideoWriter_fourcc(*fourcc), fps, sz, True)
        print("create video writer....")

        return vw

    @classmethod
    def closeVideoWrite(cls,vw):
        print("关闭录制。。。")
        vw.release()


# cap=cv2.VideoCapture(0)



# s=time.time()


# while True:
#     now=time.time()
#     if (now-s)>10:
#         break
#     ret,frame=cap.read()
#     vw.write(frame)
#
#
#
#
# cap.release()






