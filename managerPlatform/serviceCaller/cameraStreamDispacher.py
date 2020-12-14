from flask import Blueprint, request, Response

from managerPlatform.serviceCaller.cameraStreamService import cameraStreamService

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


@nat_camera_blp.route("/video_feed")
def videoStreamService():
    sessionId=request.args.get("videoPlayId")
    return Response(natCameraService.gen_frames(sessionId), mimetype='multipart/x-mixed-replace; boundary=frame')

@nat_camera_blp.route("/stopNativeCameraDetect", methods=['POST'])
def stopNativeCameraDetect():
    jsonData = request.get_json()
    return natCameraService.stopNativeCameraDetect(jsonData)



@nat_camera_blp.route("/sendDetectHeartbeat", methods=['POST'])
def sendDetectHeartbeat():
    jsonData = request.get_json()
    return natCameraService.sendDetectHeartbeat(jsonData)