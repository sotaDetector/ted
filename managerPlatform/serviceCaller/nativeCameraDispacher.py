from flask import Blueprint, request

from managerPlatform.serviceCaller.nativeCameraService import nativeCameraService

nat_camera_blp = Blueprint("nativeCameraDispacher", __name__, url_prefix="/natCamera")

natCameraService=nativeCameraService()

@nat_camera_blp.route('/getCameraDeviceList', methods=['POST'])
def getCameraDeviceList():


    return natCameraService.getCameraDeviceList()