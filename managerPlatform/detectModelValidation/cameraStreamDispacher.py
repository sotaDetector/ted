from flask import Blueprint, request, Response

from managerPlatform.detectModelValidation.cameraStreamService import cameraStreamService

nat_camera_blp = Blueprint("nativeCameraDispacher", __name__, url_prefix="/natCamera")

natCameraService=cameraStreamService()

@nat_camera_blp.route('/getCameraDeviceList', methods=['POST'])
def getCameraDeviceList():

    return natCameraService.getCameraDeviceList()


@nat_camera_blp.route('/startNativeCameraDetect', methods=['POST'])
def startNativeCameraDetect():

    jsonData = request.get_json()

    print("接收到数据："+str(jsonData))

    return natCameraService.startNativeCameraDetect(jsonData)


@nat_camera_blp.route('/startLiveStreamDetect', methods=['POST'])
def startLiveStreamDetect():


    jsonData = request.get_json()

    print("接收到数据："+str(jsonData))

    return natCameraService.startLiveStreamDetect(jsonData)



@nat_camera_blp.route("/stopNativeCameraDetect", methods=['POST'])
def stopNativeCameraDetect():
    jsonData = request.get_json()
    return natCameraService.stopNativeCameraDetect(jsonData)

