import os
import subprocess

from managerPlatform.common.commonBean.cameraDevice import cameraDevice
from managerPlatform.common.commonUtils.systemUtils import systemUtils

'''
 https://trac.ffmpeg.org/wiki/Capture/Webcam
 http://www.voidcn.com/article/p-hosigwtp-bqc.html
'''
class ffmpegUtils:

    @classmethod
    def getCameraList(cls):
        systemType = systemUtils.getSystemType()
        if systemUtils.SYSTEM_TYPE_LINUX == systemType:
            return cls.getCamerasForLinux()
        elif systemUtils.SYSTEM_TYPE_WINDOWS == systemType:
            return cls.getCamerasForMacOS()
        elif systemUtils.SYSTEM_TYPE_MACOS == systemType:
            return cls.getCamerasForMacOS()
        else:
            return None

    @classmethod
    def getCamerasForMacOS(cls):
        ffmIns = "ffmpeg -f avfoundation -list_devices true -i ''"
        result = subprocess.getstatusoutput(ffmIns)
        cameraList = []
        for item in result[1].split("\n"):
            if item.__contains__("Camera"):
                tempStr = item[item.index("] [") + 1:].replace("[", "").split("]")
                cameraList.append(cameraDevice.getCameraDevice(deviceIndex=tempStr[0], deviceName=tempStr[1],deviceUID=""))

        return cameraList

    @classmethod
    def getCamerasForLinux(cls):
        #ls /dev/video*
        #https://blog.csdn.net/lei19880402/article/details/106478386
        #v4l2-ctl --list-devices
        #udevadm info --query=all --name=/dev/video0
        getCameraIns = "ls /dev/video*"
        result = subprocess.getstatusoutput(getCameraIns)
        cameraList = []
        for item in result[1].split("\n"):
            #get detail msg
            cameraIndex=item.replace("/dev/video","")
            getDetailInfoIns = "udevadm info --query=all --name="+item
            detailInfoResult = subprocess.getstatusoutput(getDetailInfoIns)
            deviceName,deviceUID=None,None
            for item in detailInfoResult[1].split("\n"):
                if item.__contains__("ID_MODEL="):
                    deviceName=item.split("=")[1]
                elif item.__contains__("ID_SERIAL="):
                    deviceUID=item.split("=")[1]
            cameraList.append(cameraDevice.getCameraDevice(deviceIndex=cameraIndex, deviceName=deviceName,deviceUID=deviceUID))



        return cameraList


print(ffmpegUtils.getCameraList())

# print(subprocess.getstatusoutput("system_profiler SPCameraDataType"))