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
            return cls.getCamerasForMacOS()
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
                cameraList.append(cameraDevice.getCameraDevice(deviceIndex=tempStr[0], deviceName=tempStr[1]))

        return cameraList


print(ffmpegUtils.getCameraList())

print(subprocess.getstatusoutput("system_profiler SPCameraDataType"))