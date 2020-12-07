from managerPlatform.common.baseBean.baseBean import baseBean


class cameraDevice:


    @staticmethod
    def getCameraDevice(deviceIndex,deviceName,deviceUID):
        return {
            "deviceIndex": deviceIndex,
            "deviceName":deviceName,
            "deviceUID":deviceUID
        }





