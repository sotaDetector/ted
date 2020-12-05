from flask import Blueprint, request, Response

from managerPlatform.serviceCaller.nativeCameraService import nativeCameraService

nat_camera_blp = Blueprint("nativeCameraDispacher", __name__, url_prefix="/natCamera")

natCameraService=nativeCameraService()

@nat_camera_blp.route('/getCameraDeviceList', methods=['POST'])
def getCameraDeviceList():


    return natCameraService.getCameraDeviceList()


@nat_camera_blp.route('/startNativeCameraDetect', methods=['POST'])
def startNativeCameraDetect():

    jsonData = request.get_json()

    return natCameraService.startNativeCameraDetect(jsonData)


@nat_camera_blp.route("/video_feed")
def videoStreamService():
    sessionId=request.args.get("sessionId")
    return Response(natCameraService.gen_frames(sessionId), mimetype='multipart/x-mixed-replace; boundary=frame')

@nat_camera_blp.route("/stopNativeCameraDetect", methods=['POST'])
def stopNativeCameraDetect():
    jsonData = request.get_json()
    return natCameraService.stopNativeCameraDetect(jsonData)