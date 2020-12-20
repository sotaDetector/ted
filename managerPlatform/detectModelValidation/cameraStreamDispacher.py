from flask import Blueprint, request, Response

from managerPlatform.detectModelValidation.cameraStreamService import cameraStreamService

camera_stream_val_blp = Blueprint("cameraStreamValDispacher", __name__, url_prefix="/cameraStreamVal")

natCameraService=cameraStreamService()

@camera_stream_val_blp.route('/getCameraDeviceList', methods=['POST'])
def getCameraDeviceList():

    return natCameraService.getCameraDeviceList()


@camera_stream_val_blp.route('/startNativeCameraDetect', methods=['POST'])
def startNativeCameraDetect():

    jsonData = request.get_json()

    print("接收到数据："+str(jsonData))

    return natCameraService.startNativeCameraDetect(jsonData)


@camera_stream_val_blp.route('/startLiveStreamDetect', methods=['POST'])
def startLiveStreamDetect():


    jsonData = request.get_json()

    print("接收到数据："+str(jsonData))

    return natCameraService.startLiveStreamDetect(jsonData)


@camera_stream_val_blp.route('/getSampleStreamUrl', methods=['POST'])
def getSampleStreamUrl():



    return natCameraService.getSampleStreamUrl()



@camera_stream_val_blp.route("/stopDetectService", methods=['POST'])
def stopNativeCameraDetect():
    jsonData = request.get_json()
    return natCameraService.stopNativeCameraDetect(jsonData)

